from datetime import datetime
import logging

from django.db.models import Q
from django.http import Http404

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework import status
from rest_framework.response import Response

from crm.models import Client, Contract, ContractStatus, Event
from crm.serializers import (
    ClientListSerializer,
    ClientDetailSerializer,
    ContractListSerializer,
    ContractDetailSerializer,
    EventListSerializer,
    EventDetailSerializer,
)
from crm.permissions_sales import IsClientSalesContact, IsEventSalesContact
from crm.permissions_support import (
    IsClientSupportContact,
    IsEventSupportContact,
)
from crm.api_exceptions import (
    InvalidDateFormatException,
    UnsignedContractException,
)

logging.basicConfig(
    filename="log/crm.log", encoding="utf-8", level=logging.WARNING
)


class ClientViewset(ModelViewSet):
    serializer_class = ClientListSerializer
    detail_serializer_class = ClientDetailSerializer
    permission_classes = [
        IsAuthenticated
        & (IsClientSalesContact | IsClientSupportContact)
        & DjangoModelPermissions
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
        IsClientSalesContact,
        DjangoModelPermissions,
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
            try:
                datetime_start = datetime.strptime(
                    contract_date + " 00:00:00", "%Y-%m-%d %H:%M:%S"
                )
                datetime_end = datetime.strptime(
                    contract_date + " 23:59:59", "%Y-%m-%d %H:%M:%S"
                )
                queryset = queryset.filter(
                    date_created__range=(datetime_start, datetime_end)
                )
            except ValueError:
                logging.error(
                    f"Invalid date format in the contracts search request : {contract_date}"
                )
                raise InvalidDateFormatException()
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
        & (IsEventSalesContact | IsEventSupportContact)
        & DjangoModelPermissions
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
            try:
                datetime_start = datetime.strptime(
                    event_date + " 00:00:00", "%Y-%m-%d %H:%M:%S"
                )
                datetime_end = datetime.strptime(
                    event_date + " 23:59:59", "%Y-%m-%d %H:%M:%S"
                )
                queryset = queryset.filter(
                    event_date__range=(datetime_start, datetime_end)
                )
            except ValueError:
                logging.error(
                    f"Invalid date format in the events search request : {event_date}"
                )
                raise InvalidDateFormatException()

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return self.serializer_class
        else:
            return self.detail_serializer_class

    def create(self, request, *args, **kwargs):
        # The contract must be signed before the event is created.
        contract_id = request.data.get("contract")
        contract = Contract.objects.get(id=contract_id)
        signed_status = ContractStatus.objects.get(state="signed")
        if contract.status != signed_status:
            logging.error(
                f"Status of contract number {contract_id} must be set to 'signed' before creating the event."
            )
            raise UnsignedContractException()

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
