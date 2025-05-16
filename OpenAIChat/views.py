from openai import OpenAI
from django.shortcuts import render
from django.conf import settings
import os

def ai_chat_view(request):
    response_text = ""
    if request.method == "POST":
        user_message = request.POST.get("message")
        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ]
        )
        response_text = response.choices[0].message.content
    return render(request, "openAIChat/aichat.html", {"response": response_text})



