from rest_framework import serializers
from core.models import Order, Cart, Product


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("id", "product", "quantity")

    def create(self, validated_data):
        user = self.context.get("request").user
        if user.profile.carts.filter(status=Cart.ACTIVE).exists():
            cart = user.profile.carts.get(status=Cart.ACTIVE)
        else:
            cart = Cart.objects.create(status=Cart.ACTIVE, profile=user.profile)

        order = Order.objects.create(**validated_data, cart=cart)
        return order


class CartRetrieveSerializer(serializers.ModelSerializer):
    details = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ("id", "status", "details", "total_price", "doc_id")

    def get_details(self, obj):
        data = []
        for order in obj.orders.all():
            data.append(
                {
                    "product": order.product.title,
                    "unit_price": order.product.price,
                    "quantity": order.quantity,
                    "total_price": order.product.price * order.quantity,
                }
            )
        return data

    def get_total_price(self, obj):
        total = 0
        for order in obj.orders.all():
            total += order.product.price * order.quantity
        return total


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ("created_at", "updated_at")
