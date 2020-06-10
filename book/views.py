from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.mixins import ListModelMixin
from core.models import Book
from core.permissions import IsEmployee
from .serializers import BookSerializer


class UserBookView(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]


class EmployeeBookView(ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsEmployee]
    authentication_classes = (TokenAuthentication,)


class EmployeeBookDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsEmployee]
    authentication_classes = (TokenAuthentication,)

