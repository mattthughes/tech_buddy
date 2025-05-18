from openai import OpenAI
from dotenv import load_dotenv
from django.shortcuts import render, redirect
from .models import Conversation, Message
from userprofile.models import UserProfile
from django.utils.text import Truncator
from django.contrib.auth.decorators import login_required
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


@login_required
def ai_chat_view(request):
    user_message_text = None
    bot_message_text = None
    conversation = None

    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        return redirect('profile_setup')

    if request.method == "POST" and request.GET.get("end_chat") == "true":
        if "conversation_id" in request.session:
            del request.session["conversation_id"]
        return redirect("aichat")

    if request.method == "POST":
        user_message_text = request.POST.get("message", "").strip()

        # Validate and get the UserProfile
        if user_profile.age is not None and user_profile.age < 16:
            tone = f"Explain like I'm a {user_profile.age}-year-old."
        else:
            tech_level = user_profile.tech_level
            if tech_level == "low":
                tone = "Explain simply and clearly for a non-technical adult."
            elif tech_level == "medium":
                tone = "Explain with moderate technical detail."
            else:  # high
                tone = "Explain in a professional and technically detailed way."  # noqa: E501

        # Get or create a conversation
        conversation_id = request.session.get("conversation_id")
        if conversation_id:
            try:
                conversation = Conversation.objects.get(
                    id=conversation_id,
                    user_profile=user_profile
                )
            except Conversation.DoesNotExist:
                conversation = None

        if not conversation and user_profile:
            # Request title from OpenAI
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
                            "content": "You are an assistant that creates "
                            "short titles for user questions."},
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

        # Build conversation history
        chat_history = [{
            "role": "system",
            "content": "You are a helpful assistant."
        }]
        for msg in conversation.messages.order_by("timestamp"):
            chat_history.append({
                "role": "user",
                "content": msg.user_message
            })
            chat_history.append({
                "role": "assistant",
                "content": msg.bot_message
            })

        chat_history.append({
            "role": "user",
            "content": f"{tone}\n\n{user_message_text}"
        })

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=chat_history
            )
            print("DEBUG| OpenAI response object:", response)
            bot_message_text = response.choices[0].message.content

            # Save message
            Message.objects.create(
                conversation=conversation,
                user_profile=user_profile,
                tech_level=user_profile.tech_level,
                user_message=user_message_text,
                bot_message=bot_message_text
            )
        except Exception as e:
            bot_message_text = f"Error: {e}"

    print("DEBUG| Final bot_message_text:", repr(bot_message_text))

    messages = []

    if conversation:
        messages = conversation.messages.order_by("timestamp")

    return render(request, "openAIChat/aichat.html", {
        "user_message": user_message_text,
        "bot_message": bot_message_text,
        "messages": messages,  # pass messages to template
    })
