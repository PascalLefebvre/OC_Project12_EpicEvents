from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions

from django.db.models import Q

from crm.permissions import IsSalesContact, IsClientSupportContact

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
    permission_classes = [
        IsAuthenticated
        & DjangoModelPermissions
        & (IsSalesContact | IsClientSupportContact)
    ]

    def get_queryset(self):
        auth_user = self.request.user
        return Client.objects.filter(
            Q(sales_contact=auth_user)
            | Q(contract__event__support_contact=auth_user)
        )

    def get_serializer_class(self):
        if self.action == "list":
            return self.serializer_class
        else:
            return self.detail_serializer_class


class ContractViewset(ModelViewSet):

    serializer_class = ContractListSerializer
    detail_serializer_class = ContractDetailSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

    def get_queryset(self):
        queryset = Contract.objects.all()
        amount = self.request.GET.get("amount")
        if amount:
            queryset = Contract.objects.filter(amount=amount)
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return self.serializer_class
        else:
            return self.detail_serializer_class


class EventViewset(ModelViewSet):

    serializer_class = EventListSerializer
    detail_serializer_class = EventDetailSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

    def get_queryset(self):
        return Event.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return self.serializer_class
        else:
            return self.detail_serializer_class
