from rest_framework.serializers import ModelSerializer

from crm.models import Client, Contract, Event


class ClientListSerializer(ModelSerializer):
    class Meta:
        model = Client
        fields = ["id", "company_name", "sales_contact"]


class ClientDetailSerializer(ModelSerializer):
    class Meta:
        model = Client
        fields = [
            "id",
            "company_name",
            "first_name",
            "last_name",
            "email",
            "phone",
            "mobile",
            "sales_contact",
            "date_created",
            "date_updated",
        ]


class ContractListSerializer(ModelSerializer):
    class Meta:
        model = Contract
        fields = ["id", "client", "status", "date_created"]


class ContractDetailSerializer(ModelSerializer):
    class Meta:
        model = Contract
        fields = [
            "id",
            "client",
            "sales_contact",
            "status",
            "amount",
            "payment_due",
            "date_created",
            "date_updated",
        ]


class EventListSerializer(ModelSerializer):
    class Meta:
        model = Event
        fields = ["id", "support_contact", "event_date", "status"]


class EventDetailSerializer(ModelSerializer):
    class Meta:
        model = Event
        fields = [
            "id",
            "contract",
            "support_contact",
            "event_date",
            "status",
            "attendees",
            "notes",
            "date_created",
            "date_updated",
        ]
