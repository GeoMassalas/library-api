from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from core.models import Book
from .serializers import BookSerializer


class UserBookView(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]
