from openai import OpenAI
from dotenv import load_dotenv
from django.shortcuts import render, redirect
from .models import Conversation, Message
from userprofile.models import UserProfile
from django.utils.text import Truncator
from django.contrib.auth.decorators import login_required
from django.db.models import Max
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


@login_required
def ai_chat_view(request):
    print(f"DEBUG| SESSION: {request.session.get('conversation_id')}")
    print(f"DEBUG| METHOD: {request.method}")

    user_message_text = None
    bot_message_text = None
    conversation = None

    # Get UserProfile or redirect to home with a message
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        # add a message here like: messages.warning(...)
        return redirect("home")  # Fallback instead of 'profile_setup'

    conversations = Conversation.objects.filter(user_profile=user_profile) \
        .annotate(last_message_time=Max("messages__timestamp")) \
        .order_by('-last_message_time')

    # Handle "end chat" action
    if request.method == "POST" and request.GET.get("end_chat") == "true":
        print("DEBUG| Ending conversation and clearing session.")
        request.session.pop("conversation_id", None)
        return redirect("aichat")

    requested_convo_id = request.GET.get("conversation_id")
    if requested_convo_id:
        try:
            conversation = Conversation.objects.get(
                id=requested_convo_id,
                user_profile=user_profile
            )
            request.session["conversation_id"] = conversation.id
        except Conversation.DoesNotExist:
            conversation = None
            request.session.pop("conversation_id", None)

        return redirect("aichat")

    else:
        # Retrieve existing conversation
        conversation_id = request.session.get("conversation_id")
        if conversation_id:
            try:
                conversation = Conversation.objects.get(
                    id=conversation_id,
                    user_profile=user_profile
                )
                request.session["conversation_id"] = conversation.id
            except Conversation.DoesNotExist:
                conversation = None

    # Handle the POST request (user submits a message)
    if request.method == "POST":
        user_message_text = request.POST.get("message", "").strip()
        print(f"DEBUG| user_message_text: {repr(user_message_text)}")

        if not user_message_text:
            print("DEBUG| Empty user message. Skipping processing.")
            bot_message_text = "Please enter a message to send."
            return redirect("aichat")

        # If no conversation exists, create a new one with a title
        if not conversation:
            print("DEBUG| Creating new conversation...")
            title_prompt = (
                "Give a short, descriptive title (max 8 words) for "
                f"this question: '{user_message_text}'"
            )
            try:
                title_response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are an assistant that creates "
                                "short titles for user questions."
                            )
                        },
                        {"role": "user", "content": title_prompt}
                    ]
                )
                title = title_response.choices[0].message.content.strip()
            except Exception:
                title = Truncator(user_message_text).chars(50)  # fallback

            conversation = Conversation.objects.create(
                user_profile=user_profile,
                title=title,
            )
            request.session["conversation_id"] = conversation.id

        print(f"DEBUG| Processing message in Conversation {conversation.id}")

        # Determine the tone of AI's answers
        if user_profile.age is not None and user_profile.age < 16:
            tone = f"Explain like I'm a {user_profile.age}-year-old."
        else:
            tech_level = user_profile.tech_level
            if tech_level == "low":
                tone = "Explain simply and clearly for a non-technical adult."
            elif tech_level == "medium":
                tone = "Explain with moderate technical detail."
            else:  # high
                tone = ("Explain in a professional "
                        "and technically detailed way."
                        )

        # Build conversation history
        chat_history = [{
            "role": "system",
            "content": "You are a helpful assistant."
        }]
        for msg in conversation.messages.order_by("timestamp"):
            chat_history.append({"role": "user", "content": msg.user_message})
            chat_history.append({
                "role": "assistant",
                "content": msg.bot_message
            })

        chat_history.append({
            "role": "user",
            "content": f"{tone}\n\n{user_message_text}"
        })

        # 10. Call OpenAI and save result
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=chat_history
            )
            bot_message_text = response.choices[0].message.content
            print(f"DEBUG| OpenAI response: {bot_message_text}")

            Message.objects.create(
                conversation=conversation,
                user_profile=user_profile,
                tech_level=user_profile.tech_level,
                user_message=user_message_text,
                bot_message=bot_message_text
            )
            print("DEBUG| Message saved to DB.")
        except Exception as e:
            bot_message_text = f"Error: {e}"
            print(f"DEBUG| OpenAI API error: {e}")

        # Always redirect after POST
        return redirect("aichat")

    # 11. Render chat messages if GET
    chat_messages = (
        conversation.messages.order_by("timestamp")
        if conversation else []
    )

    return render(request, "openAIChat/aichat.html", {
        "chat_messages": chat_messages,
        "user_message": user_message_text,
        "bot_message": bot_message_text,
        "conversations": conversations,
        "current_conversation_id": conversation.id if conversation else None,
    })
