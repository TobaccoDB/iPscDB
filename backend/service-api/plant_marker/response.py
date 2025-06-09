from django.utils import six
from rest_framework import status
from rest_framework.response import Response

from plant_marker.errors import ERROR_CODE_SUCCESS

from .renderers import JSONRenderer


class JSONResponse(Response):
    def __init__(self,
                 data=None,
                 status=None,
                 template_name=None,
                 headers=None,
                 exception=False,
                 content_type=None,
                 code=None):
        super(JSONResponse, self).__init__(data, status, template_name, headers, exception, content_type)
        
        self.code = code

    @property
    def rendered_content(self):
        renderer = getattr(self, 'accepted_renderer', None)
        media_type = getattr(self, 'accepted_media_type', None)
        context = getattr(self, 'renderer_context', None)

        assert renderer, ".accepted_renderer not set on Response"
        assert media_type, ".accepted_media_type not set on Response"
        assert context, ".renderer_context not set on Response"
        context['response'] = self

        charset = renderer.charset
        content_type = self.content_type

        if content_type is None and charset is not None:
            content_type = "{0}; charset={1}".format(media_type, charset)
        elif content_type is None:
            content_type = media_type
        self['Content-Type'] = content_type

        if self.code is None:
            if self.status_code is not None:
                if self.status_code >= status.HTTP_400_BAD_REQUEST:
                    self.code = self.status_code
                else:
                    self.code = ERROR_CODE_SUCCESS
            else:
                self.code = ERROR_CODE_SUCCESS

        if isinstance(renderer, JSONRenderer):
            ret = renderer.render(self.data, media_type, context, self.code)
        else:

            payload = {'code': self.code, 'data': self.data}
            ret = renderer.render(payload, media_type, context)


        if isinstance(ret, six.text_type):
            assert charset, ('renderer returned unicode, and did not specify a charset value.')
            return bytes(ret.encode(charset))

        if not ret:
            del self['Content-Type']

        return ret
