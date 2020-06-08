from django.urls import path
from .views import LoginView, ProfileView, CreateUserView


urlpatterns = [
    path('', ProfileView.as_view(), name="Profile"),
    path('login/', LoginView.as_view(), name="Login"),
    # Temporary register
    path('register/', CreateUserView.as_view(), name="Register")
]
