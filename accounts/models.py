from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    class Meta:
        verbose_name_plural = "Utilisateurs"

    def __str__(self):
        return f"{self.username} / {self.first_name} {self.last_name}"
