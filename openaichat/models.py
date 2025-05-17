from django.db import models
from userprofile.models import UserProfile


class Conversation(models.Model):
    user_profile = models.ForeignKey(
        "userprofile.UserProfile",
        on_delete=models.CASCADE
    )
    started_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Conversation {self.id} - {self.user_profile.user.username}"


class Message(models.Model):
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="messages",
        null=True,
        blank=True,
    )
    user_profile = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    # This needs to be a permanent snapshot
    tech_level = models.CharField(
        max_length=10,
        null=True,
        blank=True,
    )
    user_message = models.TextField()
    bot_message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_profile.user.username}: {self.user_message[:30]}"
