from collections import OrderedDict
from rest_framework.pagination import BasePagination, _positive_int
from rest_framework.settings import api_settings
from .response import JSONResponse


def _get_count(queryset):
    """计算 queryset 的总数"""
    return queryset.count()


class PageNumberOffsetPagination(BasePagination):
    display_page_controls = False
    page_query_param = 'page'
    offset_query_param = 'offset'
    page_size_query_param = 'page_size'
    show_count_query_param = 'show_count'
    show_all_query_param = 'show_all'

    page_size = api_settings.PAGE_SIZE
    show_count = True

    def get_page_size(self, request):
        """获取页面大小"""
        try:
            return _positive_int(
                request.query_params.get(self.page_size_query_param, self.page_size),
                strict=True,
            )
        except (KeyError, ValueError):
            return self.page_size

    def get_page(self, request):
        """获取当前页数"""
        try:
            return _positive_int(
                request.query_params.get(self.page_query_param, 1),
                strict=True,
            )
        except (KeyError, ValueError):
            return 1

    def get_offset(self, request):
        """获取偏移量"""
        try:
            return _positive_int(
                request.query_params.get(self.offset_query_param, 0),
                strict=True,
            )
        except (KeyError, ValueError):
            return 0

    def get_count(self, queryset, request):
        """获取总数，取决于 show_count 参数"""
        try:
            self.show_count = _positive_int(
                request.query_params.get(self.show_count_query_param, 1),
                strict=True,
            )
        except (KeyError, ValueError):
            self.show_count = True

        if self.show_count:
            return _get_count(queryset)
        else:
            return None

    def get_previous_link(self):
        """获取上一页链接"""
        if self.start > 0:
            return self.get_page_url(self.start - self.page_size)
        return None

    def get_next_link(self):
        """获取下一页链接"""
        if self.count and self.end < self.count:
            return self.get_page_url(self.end)
        return None

    def get_page_url(self, offset):
        """生成分页 URL"""
        url = self.request.build_absolute_uri()
        query_params = self.request.query_params.copy()
        query_params[self.page_query_param] = (offset // self.page_size) + 1
        return f"{url}?{query_params.urlencode()}"

    def paginate_queryset(self, queryset, request, view=None):
        """分页查询集"""
        self.page_size = self.get_page_size(request)
        self.count = self.get_count(queryset, request)

        try:
            show_all = _positive_int(request.query_params.get(self.show_all_query_param, 0), strict=True)
        except (KeyError, ValueError):
            show_all = False

        if show_all:
            # 检查 count，如果大于 1000，最大值设置为 1000
            self.start = 0
            if not self.count:
                self.count = _get_count(queryset)
            if self.count > 1000:
                self.end = 1000
            else:
                self.end = self.count
            return queryset[self.start:self.end]

        page = self.get_page(request) - 1
        if page > 0:
            self.start = page * self.page_size
        else:
            self.start = self.get_offset(request)
        self.end = self.start + self.page_size

        if self.count and self.end > self.count:
            self.end = self.count

        return queryset[self.start:self.end]

    def get_paginated_response(self, data):
        """生成分页响应"""
        ret = OrderedDict([
            ('page_size', self.page_size),
            ('results', data)
        ])
        if self.show_count:
            ret.update({'count': self.count})
        return JSONResponse(ret)

    def to_html(self):
        """生成 HTML 输出"""
        return None
