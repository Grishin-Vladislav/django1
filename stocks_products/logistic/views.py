from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet

from .models import Product, Stock
from .serializers import ProductSerializer, StockSerializer
from .filters import StockFilter


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter]
    search_fields = ['title', 'description']


class StockViewSet(ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    filterset_class = StockFilter

    def get_queryset(self):
        queryset = super().get_queryset()

        product_search = self.request.query_params.get('product_search')
        if product_search:
            queryset = queryset.filter(positions__product__title__icontains=product_search)

        return queryset