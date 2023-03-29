from rest_framework.viewsets import ModelViewSet

from crm.models import Client, Contract, Event
from crm.serializers import (
    ClientListSerializer,
    ClientDetailSerializer,
    ContractListSerializer,
    ContractDetailSerializer,
    EventListSerializer,
    EventDetailSerializer,
)


class ClientViewset(ModelViewSet):

    serializer_class = ClientListSerializer
    detail_serializer_class = ClientDetailSerializer

    def get_queryset(self):
        return Client.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return self.serializer_class
        else:
            return self.detail_serializer_class


class ContractViewset(ModelViewSet):

    serializer_class = ContractListSerializer
    detail_serializer_class = ContractDetailSerializer

    def get_queryset(self):
        queryset = Contract.objects.all()
        contract_status = self.request.GET.get("status")
        if contract_status:
            queryset = Contract.objects.filter(status=contract_status)
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return self.serializer_class
        else:
            return self.detail_serializer_class


class EventViewset(ModelViewSet):

    serializer_class = EventListSerializer
    detail_serializer_class = EventDetailSerializer

    def get_queryset(self):
        return Event.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return self.serializer_class
        else:
            return self.detail_serializer_class
