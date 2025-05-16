from django.db import models
from django.contrib.auth.models import User
from datetime import date

# Choices for tech level
TECH_LEVELS = [
    ("High", "High"),
    ("Medium", "Medium"),
    ("Low", "Low"),
]

class Family(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    family = models.ForeignKey(Family, on_delete=models.SET_NULL, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    tech_level = models.CharField(max_length=10, choices=TECH_LEVELS)

    def __str__(self):
        return self.user.username

    @property
    def age(self):
        if not self.dob:
            return None
        today = date.today()
        return today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
