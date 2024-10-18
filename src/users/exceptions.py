# exceptions.py
from rest_framework.exceptions import APIException


class MissingAuthorizationHeader(APIException):
    status_code = 401
    default_detail = "Authorization 헤더가 누락되었습니다."


class InvalidAuthorizationHeader(APIException):
    status_code = 401
    default_detail = "유효하지 않은 Authorization 헤더입니다."


class TokenMissing(APIException):
    status_code = 400
    default_detail = "access_token을 가져오지 못했습니다."


class UserNotFound(APIException):
    status_code = 404
    default_detail = "사용자를 찾지 못했습니다."
