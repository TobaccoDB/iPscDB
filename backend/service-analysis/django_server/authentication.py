import jwt
from django.contrib.auth import get_user_model
from django.utils.encoding import smart_str
from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions
from rest_framework.authentication import *
from rest_framework_jwt.settings import api_settings

from django_server.errors import *

jwt_decode_handler = api_settings.JWT_DECODE_HANDLER


class BaseJSONWebTokenAuthentication(BaseAuthentication):

    def authenticate(self, request):
        jwt_value = self.get_jwt_value(request)
        if jwt_value is None:
            return None
        try:
            payload = jwt_decode_handler(jwt_value)
        except jwt.ExpiredSignature:
            msg = _('Signature has expired.')
            raise exceptions.AuthenticationFailed(msg)
        except jwt.DecodeError:
            msg = _('Error decoding signature.')
            raise exceptions.AuthenticationFailed(msg)
        except jwt.InvalidTokenError:
            msg = _('Invalid token.')
            raise exceptions.AuthenticationFailed(msg)
        user = self.authenticate_credentials(payload)
        return user, jwt_value

    def authenticate_credentials(self, payload):
        User = get_user_model()
        user_id = payload.get('user_id', '')
        # version_number = payload.get('version_number', '')
        if not user_id:
            raise raise_authentication_error(msg='非法操作!')
        try:
            user = User.objects.get(id=user_id)
            # if user.version_number != version_number:
            #     raise raise_authentication_error(msg='token已过期')
        except User.DoesNotExist:
            raise raise_authentication_error(msg='非法操作!')
        return user


class JSONWebTokenAuthentication(BaseJSONWebTokenAuthentication):

    www_authenticate_realm = 'api'
    def get_jwt_value(self, request):
        auth = get_authorization_header(request).split()
        auth_header_prefix = api_settings.JWT_AUTH_HEADER_PREFIX.lower()
        if not auth or smart_str(auth[0].lower()) != auth_header_prefix:
            return None
        if len(auth) == 1:
            msg = _('Invalid Authorization header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Invalid Authorization header. Credentials string '
                    'should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)
        return auth[1]

    def authenticate_header(self, request):
        return '{0} realm="{1}"'.format(api_settings.JWT_AUTH_HEADER_PREFIX, self.www_authenticate_realm)
