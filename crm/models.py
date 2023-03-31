from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


def get_sentinel_user():
    return User.objects.get_or_create(username="deleted")[0]


class Client(models.Model):
    company_name = models.CharField(max_length=250)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    mobile = models.CharField(max_length=20)
    sales_contact = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET(get_sentinel_user),
        related_name="client",
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.company_name} / {self.first_name} {self.last_name} / {self.sales_contact.username}"


class ContractStatus(models.Model):
    state = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = "Status contrat"

    def __str__(self):
        return self.state


class Contract(models.Model):
    client = models.ForeignKey(
        to=Client, on_delete=models.CASCADE, related_name="contract"
    )
    sales_contact = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET(get_sentinel_user),
        related_name="signed_contract",
    )
    status = models.ForeignKey(to=ContractStatus, on_delete=models.PROTECT)
    amount = models.FloatField()
    payment_due = models.DateTimeField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Contrats"

    def save(self, *args, **kwargs):
        self.sales_contact = self.client.sales_contact
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.client.company_name} / {self.sales_contact.username} / {self.id}"


class Event(models.Model):
    contract = models.ForeignKey(
        to=Contract, on_delete=models.CASCADE, related_name="event"
    )
    support_contact = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="organized_event",
    )
    event_date = models.DateTimeField()
    status = models.BooleanField(verbose_name="Statut")
    attendees = models.IntegerField()
    notes = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Evénements"

    def __str__(self):
        return f"{self.contract.client.company_name} / {self.support_contact.username} / {self.notes[:30]}"
