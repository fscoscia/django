from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    CUSTOMER = 0
    ADMIN = 1
    ROLE_CHOICES = ((CUSTOMER, "Cliente"), (ADMIN, "Administrador"))
    user = models.OneToOneField(
        to=User,
        verbose_name="Usuario",
        on_delete=models.PROTECT,
        related_name="profile",
    )
    role = models.PositiveSmallIntegerField(
        verbose_name="Rol", choices=ROLE_CHOICES, default=CUSTOMER
    )

    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfiles"

    def __str__(self) -> str:
        return f"{self.full_name}"
