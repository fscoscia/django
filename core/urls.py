from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import OrderViewSet, CartViewSet

router = DefaultRouter()
router.register("orders", OrderViewSet)
router.register("carts", CartViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
