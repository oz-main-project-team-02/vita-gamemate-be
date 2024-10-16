# services.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from users.models.user_model import User


class UserService:
    @staticmethod
    def get_user_from_token(authorization_header):
        if not authorization_header:
            return None, Response({"message": "Authorization 헤더가 누락되었습니다."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            access_token = authorization_header.split(" ")[1]

        except IndexError:
            return None, Response({"message": "유효하지 않은 Authorization 헤더입니다."}, status=status.HTTP_400_BAD_REQUEST)

        if not access_token:
            return None, Response({"message": "access_token을 가져오지 못했습니다."}, status=status.HTTP_404_NOT_FOUND)

        try:
            token = AccessToken(access_token)
            user_id = token.get("user_id")
            user = User.objects.get(pk=user_id)
            return user, None

        except User.DoesNotExist:
            return None, Response({"message": "사용자를 찾지 못했습니다."}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return None, Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
