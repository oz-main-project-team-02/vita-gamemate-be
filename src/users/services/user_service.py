from rest_framework.exceptions import APIException
from rest_framework_simplejwt.tokens import AccessToken

from users.exceptions import (
    InvalidAuthorizationHeader,
    MissingAuthorizationHeader,
    TokenMissing,
    UserNotFound,
)
from users.models.user_model import User


class UserService:
    @staticmethod
    def get_user_from_token(authorization_header):
        if not authorization_header:
            raise MissingAuthorizationHeader

        try:
            access_token = authorization_header.split(" ")[1]
        except IndexError:
            raise InvalidAuthorizationHeader

        if not access_token:
            raise TokenMissing

        try:
            token = AccessToken(access_token)
            user_id = token.get("user_id")

            user = User.objects.get_user_by_id(user_id)

            if not user:
                raise UserNotFound

            return user

        except UserNotFound:
            raise UserNotFound

        except Exception as e:
            raise APIException(str(e))
