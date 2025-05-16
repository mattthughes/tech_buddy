from openai import OpenAI
from dotenv import load_dotenv
from django.shortcuts import render
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ai_chat_view(request):
    response_text = ""

    if request.method == "POST":
        message = request.POST.get("message")
        category = request.POST.get("user_category")

        if message and category:
            if category == "child":
                tone = "Explain like I'm a 10-year-old."
            elif category == "non-tekkie":
                tone = "Explain simply and clearly for a non-technical adult."
            else:
                tone = "Explain in a professional and technically detailed way."

            full_prompt = f"{tone}\n\nQuestion: {message}"
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": full_prompt},
                    ],
                )
                response_text = response.choices[0].message.content
            except Exception as e:
                response_text = f"Error: {e}"

    return render(request, "openAIChat/aichat.html", {"response": response_text})



