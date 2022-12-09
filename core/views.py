import datetime
import requests
import uuid
import json
from rest_framework import viewsets, mixins, permissions, views
from rest_framework.response import Response
from rest_framework.decorators import action
from core.models import Order, Cart, Product
from core.serializers import (
    OrderCreateSerializer,
    CartRetrieveSerializer,
    ProductSerializer,
)
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
        uid = str(uuid.uuid4()).split("-")[0]
        doc_id = f"nav{cart_id}{uid}"
        cart.doc_id = doc_id
        cart.save()
        debt = {
            "docId": doc_id,
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

    @action(methods=["get"], detail=False, url_path="active", url_name="active")
    def get_active_cart(self, request):
        try:
            cart = self.queryset.get(status=Cart.ACTIVE)
        except Cart.DoesNotExist:
            return Response(data={"details": [], "total_price": 0}, status=200)
        serializer = CartRetrieveSerializer(instance=cart)
        return Response(serializer.data)


class ProductViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Product.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProductSerializer


class CallbackView(views.APIView):
    def post(self, request):
        pay_status = request.data.get("debt").get("payStatus", None)
        if pay_status:
            doc_id = request.data.get("debt").get("docId")
            cart = Cart.objects.get(doc_id=doc_id)
            if pay_status.get("status") == "paid":
                cart.status = Cart.PAID
            cart.raw_response = json.dumps(request.data)
            cart.save()
        return Response(
            {
                "status": "ok",
            },
            status=200,
        )
