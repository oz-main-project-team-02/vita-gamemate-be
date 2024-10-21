from rest_framework.pagination import PageNumberPagination


class GameRequestPagination(PageNumberPagination):
    page_size = 10
