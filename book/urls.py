from django.urls import path
from .views import UserBookView


urlpatterns = [
    path('', UserBookView.as_view(), name="Books")
]