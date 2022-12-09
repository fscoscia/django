from rest_framework import serializers
from core.models import Cart
from users.models import UserProfile
from django.contrib.auth.models import User


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150)
    first_name = serializers.CharField(max_length=150, min_length=2)
    last_name = serializers.CharField(max_length=150, min_length=2)
    role = serializers.SerializerMethodField()
    active_cart = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "role", "active_cart")

    def get_active_cart(self, obj):
        return obj.profile.carts.filter(status=Cart.ACTIVE).exists()

    def get_role(self, obj):
        return obj.profile.get_role_display()
