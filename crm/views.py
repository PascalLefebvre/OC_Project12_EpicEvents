from datetime import datetime

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


def convert_date(date):
    """Convert French date format to the English one."""
    list_date = date.split("-")
    if len(list_date) == 2:
        date = list_date[1] + "-" + list_date[0]
    if len(list_date) == 3:
        date = list_date[2] + "-" + list_date[1] + "-" + list_date[0]
    return date


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
        queryset = Client.objects.filter(
            Q(sales_contact=auth_user)
            | Q(contract__event__support_contact=auth_user)
        ).distinct()
        company = self.request.query_params.get("company")
        if company:
            queryset = queryset.filter(company_name__icontains=company)
        email = self.request.query_params.get("email")
        if email:
            queryset = queryset.filter(email__icontains=email)
        return queryset

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
        company = self.request.query_params.get("company")
        if company:
            queryset = queryset.filter(client__company_name__icontains=company)
        email = self.request.query_params.get("email")
        if email:
            queryset = queryset.filter(client__email__icontains=email)
        contract_date = self.request.query_params.get("date")
        if contract_date:
            contract_date = convert_date(contract_date)
            queryset = queryset.filter(date_created__contains=contract_date)
        amount = self.request.query_params.get("amount")
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
        company = self.request.query_params.get("company")
        if company:
            queryset = queryset.filter(
                contract__client__company_name__icontains=company
            )
        email = self.request.query_params.get("email")
        if email:
            queryset = queryset.filter(
                contract__client__email__icontains=email
            )
        event_date = self.request.query_params.get("date")
        if event_date:
            event_date = convert_date(event_date)
            queryset = queryset.filter(event_date__contains=event_date)
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return self.serializer_class
        else:
            return self.detail_serializer_class
