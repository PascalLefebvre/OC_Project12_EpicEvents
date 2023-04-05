from django.contrib.auth.models import AbstractUser, Group

sales_group = Group.objects.get(name="vente")
support_group = Group.objects.get(name="support")


class CustomUser(AbstractUser):
    class Meta:
        verbose_name_plural = "Utilisateurs"

    def __str__(self):
        return f"{self.username} / {self.first_name} {self.last_name}"
