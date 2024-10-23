from django.db.models import Q
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from mates.utils import MateSearchPagination
from users.models import User
from users.serializers.user_serializer import UserMateSerializer


class MateSearchAPIView(generics.ListAPIView):
    serializer_class = UserMateSerializer
    pagination_class = MateSearchPagination

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        if not queryset.exists():
            return Response({"message": "검색하신 사용자를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        page = self.paginate_queryset(queryset)

        if page is None:  # pagination이 disabled 됐을때
            return Response({"error": "페이지네이션에 실패했습니다."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def get_queryset(self):
        search = self.request.query_params.get("search", "")
        queryset = User.objects.filter(is_mate=True, nickname__icontains=search)

        return queryset
