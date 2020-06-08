from rest_framework import serializers
from core.models import Transaction


class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ('id', 'book', 'user', 'date', 'is_active', 'due_date', 'renewals')

    # TODO: Validation