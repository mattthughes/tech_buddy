from django.contrib import admin
from .models import Family, UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'tech_level', 'family', 'dob')
    list_filter = ('tech_level', 'family')
    search_fields = ('user__username',)


admin.site.register(UserProfile, UserProfileAdmin)

admin.site.register(Family)
