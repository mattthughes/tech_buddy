from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from userprofile.models import UserProfile
from .forms import FamilyMemberSignupForm


@login_required
def signup_family_member(request):
    # Ensure only facilitators can access
    try:
        facilitator_profile = UserProfile.objects.get(user=request.user)
        if facilitator_profile.user_type != 'facilitator':
            messages.error(
                request,
                "Access denied. Only facilitators can add family members."
            )
            return redirect('home')  # Or some other safe page
    except UserProfile.DoesNotExist:
        messages.error(request, "User profile not found.")
        return redirect('home')

    if request.method == 'POST':
        form = FamilyMemberSignupForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)  # Save User, don't commit yet

            # Set password properly
            new_user.set_password(form.cleaned_data['password1'])
            new_user.save()

            # Now create or update UserProfile with extra info
            profile = new_user.userprofile
            profile.dob = form.cleaned_data['dob']
            profile.tech_level = form.cleaned_data['tech_level']
            profile.family = facilitator_profile.family
            profile.user_type = 'family_member'
            profile.save()

            messages.success(
                request,
                f"Family member '{new_user.username}' created successfully!")
            # Redirect back or somewhere else
            return redirect('familymember:signup_family_member')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = FamilyMemberSignupForm()

    return render(request, 'familymember/familysignup.html', {
        'form': form,
    })
