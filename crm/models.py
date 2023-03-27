from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username="deleted")[0]


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


class Contract(models.Model):
    sales_contact = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET(get_sentinel_user),
        related_name="signed_contract",
    )
    client = models.ForeignKey(
        to=Client, on_delete=models.CASCADE, related_name="contract"
    )
    status = models.BooleanField()
    amount = models.FloatField()
    payment_due = models.DateTimeField
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)


class Event(models.Model):
    TO_ORGANIZE = "TO_ORGANIZE"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"

    STATUS_CHOICES = (
        (TO_ORGANIZE, "A organiser"),
        (IN_PROGRESS, "En cours"),
        (COMPLETED, "Terminé"),
    )

    contract = models.ForeignKey(
        to=Contract, on_delete=models.CASCADE, related_name="event"
    )
    support_contact = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="organized_event",
    )
    event_date = models.DateTimeField()
    status = models.CharField(
        max_length=30, choices=STATUS_CHOICES, verbose_name="Statut"
    )
    attendees = models.IntegerField()
    notes = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)
