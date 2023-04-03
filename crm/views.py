from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions

from django.db.models import Q

from crm.permissions_sales import IsClientSalesContact, IsEventSalesContact
from crm.permissions_support import (
    IsClientSupportContact,
    IsEventSupportContact,
)

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
        & (IsClientSalesContact | IsClientSupportContact)
    ]

    def get_queryset(self):
        auth_user = self.request.user
        return Client.objects.filter(
            Q(sales_contact=auth_user)
            | Q(contract__event__support_contact=auth_user)
        ).distinct()

    def get_serializer_class(self):
        if self.action == "list":
            return self.serializer_class
        else:
            return self.detail_serializer_class


class ContractViewset(ModelViewSet):

    serializer_class = ContractListSerializer
    detail_serializer_class = ContractDetailSerializer
    permission_classes = [
        IsAuthenticated,
        DjangoModelPermissions,
        IsClientSalesContact,
    ]

    def get_queryset(self):
        queryset = Contract.objects.filter(sales_contact=self.request.user)
        amount = self.request.GET.get("amount")
        if amount:
            queryset = queryset.filter(amount=amount)
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return self.serializer_class
        else:
            return self.detail_serializer_class


class EventViewset(ModelViewSet):

    serializer_class = EventListSerializer
    detail_serializer_class = EventDetailSerializer
    permission_classes = [
        IsAuthenticated
        & DjangoModelPermissions
        & (IsEventSalesContact | IsEventSupportContact)
    ]

    def get_queryset(self):
        queryset = Event.objects.filter(
            Q(support_contact=self.request.user)
            | Q(contract__sales_contact=self.request.user)
        ).distinct()
        event_date = self.request.GET.get("date")
        if event_date:
            queryset = queryset.filter(event_date__contains=event_date)
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return self.serializer_class
        else:
            return self.detail_serializer_class
