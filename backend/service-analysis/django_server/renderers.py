import json

import six
from rest_framework import renderers, status
from rest_framework.compat import *

from django_server.errors import ERROR_CODE_SUCCESS


class JSONRenderer(renderers.JSONRenderer):
    def render(self,
               data,
               accepted_media_type=None,
               renderer_context=None,
               code=None):
        """
        Render `data` into JSON, returning a bytestring.
        Override here.
        """
        if data is None:
            return bytes()

        renderer_context = renderer_context or {}
        indent = self.get_indent(accepted_media_type, renderer_context)

        if indent is None:
            separators = SHORT_SEPARATORS if self.compact else LONG_SEPARATORS
        else:
            separators = INDENT_SEPARATORS

        if 'code' in data:
            payload = data
        else:
            if code is None:
                if renderer_context:
                    status_code = renderer_context['response'].status_code
                    if status_code is not None and status_code >= status.HTTP_400_BAD_REQUEST:
                        code = status_code
                    else:
                        code = ERROR_CODE_SUCCESS
                else:
                    code = ERROR_CODE_SUCCESS
            payload = {'code': code, 'data': data}

        ret = json.dumps(
            payload,
            cls=self.encoder_class,
            indent=indent,
            ensure_ascii=self.ensure_ascii,
            separators=separators)

        # On python 2.x json.dumps() returns bytestrings if ensure_ascii=True,
        # but if ensure_ascii=False, the return type is underspecified,
        # and may (or may not) be unicode.
        # On python 3.x json.dumps() returns unicode strings.
        if isinstance(ret, six.text_type):
            # We always fully escape \u2028 and \u2029 to ensure we output JSON
            # that is a strict javascript subset. If bytes were returned
            # by json.dumps() then we don't have these characters in any case.
            # See: http://timelessrepo.com/json-isnt-a-javascript-subset
            ret = ret.replace('\u2028', '\\u2028').replace('\u2029', '\\u2029')
            return bytes(ret.encode('utf-8'))
        return ret
