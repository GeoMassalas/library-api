
from rest_framework.authentication import TokenAuthentication
from rest_framework.viewsets import ModelViewSet
from core.models import Book
from core.permissions import IsManagerOrReadOnly
from .serializers import BookSerializer


class BooksViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsManagerOrReadOnly]
    authentication_classes = (TokenAuthentication,)
