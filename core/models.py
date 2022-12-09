from django.db import models
from users.models import UserProfile


class Product(models.Model):
    title = models.CharField(verbose_name="Título", max_length=100)
    description = models.TextField(verbose_name="Descripción", null=True, default="")
    price = models.IntegerField(verbose_name="Precio")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self) -> str:
        return f"{self.title}"


class Cart(models.Model):
    INACTIVE = 0
    ACTIVE = 1
    PAID = 2
    STATUS_CHOICES = ((INACTIVE, "Inactivo"), (ACTIVE, "Activo"), (PAID, "Pagado"))
    profile = models.ForeignKey(
        to=UserProfile,
        verbose_name="Perfil",
        on_delete=models.PROTECT,
        related_name="carts",
    )
    status = models.PositiveSmallIntegerField(
        verbose_name="Estado", choices=STATUS_CHOICES
    )
    doc_id = models.CharField(max_length=15, blank=True, default="", editable=False)
    raw_response = models.JSONField(editable=False, default=dict)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Carrito"
        verbose_name_plural = "Carritos"

    def __str__(self) -> str:
        return f"{self.profile.full_name} {self.status}"


class Order(models.Model):
    product = models.ForeignKey(
        to=Product, verbose_name="Producto", on_delete=models.PROTECT, related_name="+"
    )
    quantity = models.IntegerField(verbose_name="Cantidad")
    cart = models.ForeignKey(
        to=Cart, verbose_name="Carrito", on_delete=models.CASCADE, related_name="orders"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Orden"
        verbose_name_plural = "Ordenes"

    def __str__(self) -> str:
        return f"{self.cart} {self.product.title} {self.quantity}"
