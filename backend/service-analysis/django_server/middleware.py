import json

from django.utils.deprecation import MiddlewareMixin


class GenericQueryParserMiddleware(MiddlewareMixin):
    page_query_param = 'page'
    offset_query_param = 'offset'
    page_size_query_param = 'page_size'
    show_count_query_param = 'show_count'
    show_all_query_param = 'show_all'

    def process_request(self, request):

        if request.method == 'GET':
            data = request.GET
        else:
            try:
                data = json.loads(request.body.decode(), encoding='utf-8')
            except:
                data = {}

        request.pagination = {}
        if self.page_query_param in data:
            request.pagination[self.page_query_param] = data.get(
                self.page_query_param)
        if self.offset_query_param in data:
            request.pagination[self.offset_query_param] = data.get(
                self.offset_query_param)
        if self.page_size_query_param in data:
            request.pagination[self.page_size_query_param] = data.get(
                self.page_size_query_param)
        if self.show_count_query_param in data:
            request.pagination[self.show_count_query_param] = data.get(
                self.show_count_query_param)
        if self.show_count_query_param in data:
            request.pagination[self.show_count_query_param] = data.get(
                self.show_count_query_param)
        if self.show_all_query_param in data:
            request.pagination[self.show_all_query_param] = data.get(
                self.show_all_query_param)
    #
    # def process_response(self, request, response):
    #     return response

