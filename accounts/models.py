from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    MANAGEMENT = "MANAGEMENT"
    SALES = "SALES"
    SUPPORT = "SUPPORT"

    TEAM_CHOICES = (
        (MANAGEMENT, "Gestion"),
        (SALES, "Vente"),
        (SUPPORT, "Support"),
    )
    team = models.CharField(max_length=30, choices=TEAM_CHOICES, verbose_name="Equipe")
