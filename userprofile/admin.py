from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib import admin
from .models import Family, UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'


class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'tech_level', 'family', 'dob')
    list_filter = ('tech_level', 'family')
    search_fields = ('user__username',)


admin.site.unregister(User)
admin.site.register(UserProfile, UserProfileAdmin)

admin.site.register(Family)
