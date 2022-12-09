from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import OrderViewSet, CartViewSet, ProductViewSet

router = DefaultRouter()
router.register("orders", OrderViewSet)
router.register("carts", CartViewSet)
router.register("products", ProductViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
