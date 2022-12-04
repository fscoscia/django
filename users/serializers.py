from rest_framework import serializers
from core.models import Cart
from users.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    active_cart = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = "__all__"

    def get_active_cart(self, obj):
        return obj.carts.filter(status=Cart.ACTIVE).exists()
