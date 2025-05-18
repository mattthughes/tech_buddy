from allauth.account.forms import SignupForm
from django import forms
from .models import TECH_LEVELS, UserProfile, Family


class CustomSignupForm(SignupForm):
    """
    Custom signup form for user registration.
    """
    username = forms.CharField(
        max_length=150,
        label="User Name",
        required=True
    )
    first_name = forms.CharField(
        max_length=30,
        label="First Name",
        required=True
    )
    last_name = forms.CharField(
        max_length=30,
        label="Last Name",
        required=True
    )
    family = forms.ModelChoiceField(
        queryset=Family.objects.all(),
        label="Family",
        empty_label="Select a family",
        required=True
    )
    tech_level = forms.ChoiceField(
        choices=TECH_LEVELS,
        label="Tech Level",
        required=True
    )
    date_of_birth = forms.DateField(
        label="Date of Birth",
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove the email field if present
        if 'email' in self.fields:
            del self.fields['email']

    def save(self, request):
        user = super().save(request)
        user.username = self.cleaned_data['username']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()

        profile, created = UserProfile.objects.get_or_create(user=user)
        profile.family = self.cleaned_data['family']
        profile.tech_level = self.cleaned_data['tech_level']
        profile.dob = self.cleaned_data['date_of_birth']
        profile.user_type = 'facilitator'
        profile.save()
        return user
