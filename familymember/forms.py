from django import forms
from django.contrib.auth.models import User
from userprofile.models import UserProfile  # noqa: F401


class FamilyMemberSignupForm(forms.ModelForm):
    # User model fields
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput
    )

    # UserProfile fields
    dob = forms.DateField(
        label="Date of Birth",
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    TECH_LEVEL_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    )
    tech_level = forms.ChoiceField(choices=TECH_LEVEL_CHOICES)

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'password1',
            'password2'
        ]

    def clean(self):
        cleaned_data = super().clean()
        pw1 = cleaned_data.get("password1")
        pw2 = cleaned_data.get("password2")

        if pw1 and pw2 and pw1 != pw2:
            self.add_error('password2', "Passwords do not match")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            # UserProfile will be handled in the view
        return user
