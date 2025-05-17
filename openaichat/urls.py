from django.urls import path
from . import views

urlpatterns = [
    path("", views.ai_chat_view, name="aichat"),
]
