from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination,
    )

class ItemLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 10


class ItemPageNumberPagination(PageNumberPagination):
    page_size = 20