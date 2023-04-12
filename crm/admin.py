from django.contrib import admin

from .models import Client, ContractStatus, Contract, Event


@admin.register(Client)
class Client(admin.ModelAdmin):
    fields = [
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
    readonly_fields = [
        "date_created",
        "date_updated",
    ]


admin.site.register(ContractStatus)


@admin.register(Contract)
class Contract(admin.ModelAdmin):
    fields = [
        "client",
        "sales_contact",
        "status",
        "amount",
        "payment_due",
        "date_created",
        "date_updated",
    ]
    readonly_fields = [
        "date_created",
        "date_updated",
    ]


@admin.register(Event)
class Event(admin.ModelAdmin):
    fields = [
        "contract",
        "support_contact",
        "event_date",
        "status",
        "attendees",
        "notes",
        "date_created",
        "date_updated",
    ]
    readonly_fields = [
        "date_created",
        "date_updated",
    ]
