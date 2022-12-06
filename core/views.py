from django.shortcuts import render
from rest_framework import viewsets, mixins, permissions
from core.models import Order, Cart
from core.serializers import OrderCreateSerializer, CartRetrieveSerializer


class OrderViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Order.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderCreateSerializer


class CartViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Cart.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CartRetrieveSerializer

    def get_queryset(self):
        return Cart.objects.filter(profile=self.request.user.profile)
