from django_filters import rest_framework as filters
from core.models import Transaction


class TransactionFilter(filters.FilterSet):
    min_date = filters.DateFilter(field_name="date", lookup_expr='gte')
    max_date = filters.DateFilter(field_name="date", lookup_expr='lte')

    class Meta:
        model = Transaction
        fields = ['min_date', 'max_date', 'user', 'book', 'is_active', 'book__id']
