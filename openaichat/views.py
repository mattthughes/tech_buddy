from openai import OpenAI
from dotenv import load_dotenv
from django.shortcuts import render
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ai_chat_view(request):
    user_message_text = None
    bot_message_text = None

    if request.method == "POST":
        user_message_text = request.POST.get("message").strip()
        category = request.POST.get("user_category")

        if user_message_text and category:
            if category == "child":
                tone = "Explain like I'm a 10-year-old."
            elif category == "non-tekkie":
                tone = "Explain simply and clearly for a non-technical adult."
            else:
                tone = "Explain in a professional and technically detailed way."

            full_prompt = f"{tone}\n\nUser message: {user_message_text}"
            try:
                bot_message = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": full_prompt},
                    ],
                )
                bot_message_text = bot_message.choices[0].message.content
            except Exception as e:
                bot_message_text = f"Error: {e}"

    return render(request, "openAIChat/aichat.html", {
        "user_message": user_message_text,
        "bot_message": bot_message_text,
        })



