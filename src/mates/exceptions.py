from rest_framework.exceptions import APIException


class InvalidLevelError(APIException):
    status_code = 400
    default_detail = "잘못된 레벨입니다."
