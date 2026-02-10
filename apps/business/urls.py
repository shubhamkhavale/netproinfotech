from django.urls import path
from .views import business_profile

app_name = 'business'

urlpatterns = [
    path("", business_profile, name="profile"),
    path("settings/", business_profile, name="settings"),
]
