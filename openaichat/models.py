from django.db import models
from django.contrib.auth.models import User
from userprofile.models import UserProfile

class Message(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    user_message = models.TextField()
    bot_message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_profile.user.username}: {self.user_message[:30]}"