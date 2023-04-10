from django.contrib import admin

from .models import Client, ContractStatus, Contract, Event

admin.site.register(Client)
admin.site.register(ContractStatus)
admin.site.register(Event)


@admin.register(Contract)
class Contract(admin.ModelAdmin):
    fields = [
        "client",
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
