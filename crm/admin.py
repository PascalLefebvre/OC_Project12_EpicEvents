from django.contrib import admin

from .models import Client, ContractStatus, Contract, Event

admin.site.register(Client)
admin.site.register(ContractStatus)
admin.site.register(Contract)
admin.site.register(Event)
