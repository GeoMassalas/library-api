from rest_framework import serializers
from core.models import Book


class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'isbn', 'isbn13', 'description', 'category1', 'category2', 'category3')

    # TODO: Validation
    def validate(self, data):
        if 'isbn' in data:
            if (len(data['isbn']) != 10) | (not data['isbn'].isdigit()):
                raise serializers.ValidationError("ISBN should be 10 numbers")
        if 'isbn13' in data:
            if (len(data['isbn']) != 14) | (not data['isbn13'][:3].isdigit() & data['isbn13'][4:].isdigit()):
                raise serializers.ValidationError("ISBN format should be (3numbers)-(10numbers).")
        return data
