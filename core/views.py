import datetime
import requests
import json
from rest_framework import viewsets, mixins, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from core.models import Order, Cart
from core.serializers import OrderCreateSerializer, CartRetrieveSerializer
from django.conf import settings


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

    @action(methods=["post"], detail=False, url_path="checkout", url_name="checkout")
    def checkout(self, request):
        cart_id = request.data.get("cart")
        cart = Cart.objects.get(id=cart_id)
        serializer = self.serializer_class(instance=cart)
        apiKey = settings.APIKEY
        host = settings.HOST
        start_date = datetime.datetime.utcnow().replace()
        end_date = start_date + datetime.timedelta(hours=1)
        debt = {
            "docId": f"nav{cart_id}",
            "amount": {"currency": "PYG", "value": serializer.data.get("total_price")},
            "label": "Compra de regalos",
            "validPeriod": {
                "start": start_date.strftime("%Y-%m-%dT%H:%M:%S"),
                "end": end_date.strftime("%Y-%m-%dT%H:%M:%S"),
            },
        }
        post = {"debt": debt}
        headers = {
            "apikey": apiKey,
            "Content-Type": "application/json",
        }
        r = requests.post(f"{host}/debts", json=post, headers=headers)
        return Response(data=r.json(), status=r.status_code)
