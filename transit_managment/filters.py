import django_filters

from .models import Transaction


class TransactionFilter(django_filters.FilterSet):
    date_from = django_filters.DateFilter(field_name='date', lookup_expr='gte')
    date_to = django_filters.DateFilter(field_name='date', lookup_expr='lte')
    status = django_filters.NumberFilter(field_name='status_id')
    transaction_type = django_filters.NumberFilter(field_name='transaction_type_id')
    category = django_filters.NumberFilter(field_name='category_id')

    class Meta:
        model = Transaction
        fields = ['date_from', 'date_to', 'status', 'transaction_type', 'category']
