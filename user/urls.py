from django.urls import path
from .views import LoginView, ProfileView


urlpatterns = [
    path('', ProfileView.as_view(), name="Profile"),
    path('login/', LoginView.as_view(), name="Login")
]
