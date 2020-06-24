from django.urls import path
from .views import LoginView, ProfileView, ManageUserDetailView, ManageUserView, \
    DeleteUserView, reset_password, change_password


urlpatterns = [
    path('', ProfileView.as_view(), name="Profile"),
    path('login/', LoginView.as_view(), name="Login"),
    path('manage/', ManageUserView.as_view(), name="Manage Users"),
    path('manage/<str:pk>/', ManageUserDetailView.as_view(), name="Manage Users Detail"),
    path('manage/<str:pk>/delete/', DeleteUserView.as_view(), name="Delete User"),
    path('manage/<str:pk>/reset_password/', reset_password, name='Reset Password'),
    path('manage/<str:pk>/change_password/', change_password, name='Reset Password')
]
