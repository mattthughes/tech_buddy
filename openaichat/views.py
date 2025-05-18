from openai import OpenAI
from dotenv import load_dotenv
from django.shortcuts import render
from .models import Conversation, Message
from userprofile.models import UserProfile
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def ai_chat_view(request):
    user_message_text = None
    bot_message_text = None
    conversation = None
    user_profile = None

    if request.method == "POST":
        dummy_user = request.POST.get("dummy_user")
        user_message_text = request.POST.get("message", "").strip()
        category = request.POST.get("user_category")

        # Validate and get the UserProfile
        if dummy_user:
            try:
                user_profile = UserProfile.objects.get(
                    user__username__iexact=dummy_user
                )
            except UserProfile.DoesNotExist:
                bot_message_text = f"No profile found for user '{dummy_user}'."
                return render(request, "openAIChat/aichat.html", {
                    "user_message": user_message_text,
                    "bot_message": bot_message_text,
                })

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
            conversation = Conversation.objects.create(
                user_profile=user_profile
            )
            request.session["conversation_id"] = conversation.id

        if user_message_text and category and user_profile:
            # Determine tone
            if category == "child":
                tone = "Explain like I'm a 10-year-old."
            elif category == "non-techie":
                tone = "Explain simply and clearly for a non-technical adult."
            else:
                tone = "Explain in a professional and technically detailed way."  # noqa: E501

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

    return render(request, "openAIChat/aichat.html", {
        "user_message": user_message_text,
        "bot_message": bot_message_text,
    })
