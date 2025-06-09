from django.utils.encoding import force_str
from rest_framework import status
from rest_framework.exceptions import APIException


class _ValidationError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST


class _PermissionError(APIException):
    status_code = status.HTTP_403_FORBIDDEN


class _ServerError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    def __init__(self, error_code=None, detail=None):
        if not error_code:
            self.error_code = self.status_code
        else:
            self.error_code = error_code
        if detail is not None:
            self.detail = force_str(detail)
        else:
            self.detail = force_str(self.default_detail)


class _AuthenticationError(_ServerError):
    status_code = status.HTTP_401_UNAUTHORIZED


class _RemoteServerError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST


def raise_validation_error(msg):
    raise _ValidationError(msg)


def raise_permission_error(msg):
    raise _PermissionError(msg)


def raise_authentication_error(msg, error_code=401):
    raise _AuthenticationError(error_code=error_code, detail=msg)


def raise_server_error(error_code, msg):
    raise _ServerError(error_code=error_code, detail=msg)


def raise_remote_server_error(msg):
    raise _RemoteServerError(msg)


# reserved
ERROR_CODE_FAIL = -1
ERROR_CODE_SUCCESS = 200
ERROR_CODE_INVALID_DATA = 100
ERROR_CODE_INVALID_ACTION = 101

ERROR_CODE_ACCOUNT_EXIST = 1000
ERROR_CODE_ACCOUNT_NOT_EXIST = 1001
ERROR_CODE_ACCOUNT_DISABLED = 1002
ERROR_CODE_ACCOUNT_PASSWORD_INCORRECT = 1003
ERROR_CODE_ACCOUNT_OLD_PASSWORD_INCORRECT = 1004

ERROR_CODE_ENTERPRISE_DISABLED = 1050
