from django.urls import path
from .views import UserBookView, EmployeeBookView, EmployeeBookDetailView

urlpatterns = [
    path('', UserBookView.as_view(), name="Books"),
    path('manage/', EmployeeBookView.as_view(), name="Manage Books"),
    path('manage/<str:pk>/', EmployeeBookDetailView.as_view(), name="Manage Book")
]