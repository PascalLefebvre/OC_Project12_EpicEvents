from rest_framework import status
from rest_framework.exceptions import APIException


class BaseCustomException(APIException):
    detail = None
    status_code = None

    def __init__(self, detail, code):
        super().__init__(detail, code)
        self.detail = detail
        self.status_code = code


class InvalidDateFormatException(BaseCustomException):
    def __init__(self):
        detail = "Invalid date format."
        super().__init__(detail, status.HTTP_400_BAD_REQUEST)


class UnsignedContractException(BaseCustomException):
    """Exception raised when an event ..."""

    def __init__(self):
        detail = "The contract must be signed before the event is created."
        super().__init__(detail, status.HTTP_409_CONFLICT)
