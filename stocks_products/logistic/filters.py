import django_filters

from .models import Stock


class StockFilter(django_filters.FilterSet):
    positions__product__title = django_filters.CharFilter(
        field_name='positions__product__title', lookup_expr='icontains',
        label='product_search'
    )

    class Meta:
        model = Stock
        fields = ['positions__product__title']
