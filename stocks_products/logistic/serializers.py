from rest_framework import serializers

from .models import Product, StockProduct, Stock


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']


class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['id', 'address', 'positions']

    def create(self, validated_data):
        positions = validated_data.pop('positions')

        stock = super().create(validated_data)

        for position in positions:
            new_stock_product = StockProduct(
                quantity=position['quantity'],
                price=position['price'],
                product=position['product'],
                stock=stock
            )
            new_stock_product.save()

        return stock

    def update(self, instance, validated_data):
        positions = validated_data.pop('positions')

        stock = super().update(instance, validated_data)

        for stock_product in stock.positions.all():
            product_id = stock_product.product_id
            for index, product in enumerate(positions):
                obj = product['product']
                if obj.id == product_id:
                    stock_product.quantity = product['quantity']
                    stock_product.price = product['price']
                    stock_product.save()
                    del positions[index]

        if positions:
            for product in positions:
                p = StockProduct(
                    quantity=product['quantity'],
                    price=product['price'],
                    product=product['product'],
                    stock=stock
                )
                p.save()

        return stock
