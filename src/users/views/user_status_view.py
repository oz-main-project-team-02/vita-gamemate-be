from django_redis import get_redis_connection
from rest_framework import status as resp_status
from rest_framework.response import Response
from rest_framework.views import APIView


class UserStatusAPIView(APIView):
    def get(self, request):
        user_id = request.query_params.get("user_id", None)

        if user_id is None:
            return Response({"error": "쿼리 파라미터로 user_id 를 보내주세요."}, status=resp_status.HTTP_400_BAD_REQUEST)
        redis_instance = get_redis_connection("default")

        is_online = redis_instance.get(f"user:{user_id}:is_online")

        if is_online:
            is_online = is_online.decode("utf-8").lower() == "true"
            return Response({"is_online": is_online})
        else:
            return Response({"error": "사용자에게 is_online값이 없습니다."}, status=resp_status.HTTP_400_BAD_REQUEST)
