from django.urls import path
from . import views

app_name = 'familymember'

urlpatterns = [
    path('signup/', views.signup_family_member, name='signup'),
]
