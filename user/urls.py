from django.urls import path
from .views import LoginView, ProfileView, ManageUserDetailView, ManageUserView, DeleteUserView


urlpatterns = [
    path('', ProfileView.as_view(), name="Profile"),
    path('login/', LoginView.as_view(), name="Login"),
    path('manage/', ManageUserView.as_view(), name="Manage Users"),
    path('manage/<str:pk>/', ManageUserDetailView.as_view(), name="Manage Users Detail"),
    path('manage/<str:pk>/delete/', DeleteUserView.as_view(), name="Delete User"),
]
