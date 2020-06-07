from rest_framework import serializers
from core.models import Book


class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'isbn', 'isbn13', 'description', 'category1', 'category2', 'category3')

    # TODO: Validation
