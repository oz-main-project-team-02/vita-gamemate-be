import base64
import os

import requests
from django.conf import settings
from rest_framework import generics, status
from rest_framework.response import Response

from users.exceptions import (
    InvalidAuthorizationHeader,
    MissingAuthorizationHeader,
    TokenMissing,
    UserNotFound,
)
from users.services.user_service import UserService

from .models import Payment
from .serializers import PaymentSerializer


class TossPaymentView(generics.GenericAPIView):
    serializer_class = PaymentSerializer

    def post(self, request):
        authorization_header = self.request.headers.get("Authorization")

        try:
            user = UserService.get_user_from_token(authorization_header)
        except (MissingAuthorizationHeader, InvalidAuthorizationHeader, TokenMissing, UserNotFound) as e:
            return Response({"message": str(e)}, status=e.status_code)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # 유효한 데이터 가져오기
            payment_key = serializer.validated_data["payment_key"]
            order_id = serializer.validated_data["order_id"]
            amount = serializer.validated_data["amount"]

            secret_key = os.environ.get("TOSS_TEST_SECRET_KEY")

            # Toss API 요청
            url = f"https://api.tosspayments.com/v1/payments/{payment_key}"
            headers = {
                "Authorization": "Basic " + base64.b64encode(f"{secret_key}:".encode()).decode(),
                "Content-Type": "application/json",
            }
            data = {
                "orderId": order_id,
                "amount": amount,
            }

            try:
                response = requests.post(url, json=data, headers=headers)
                response.raise_for_status()

                # 결제 정보 저장
                Payment.objects.create(
                    user=user,
                    payment_key=payment_key,
                    order_id=order_id,
                    amount=amount,
                )

                return Response(
                    {
                        "title": "결제 성공",
                        "body": response.json(),
                    },
                    status=status.HTTP_200_OK,
                )

            except requests.exceptions.RequestException as e:
                print(f"Toss 결제 API 오류: {e}")
                return Response({"detail": "결제 실패"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserPaymentListView(generics.ListAPIView):
    serializer_class = PaymentSerializer

    def get_queryset(self):
        authorization_header = self.request.headers.get("Authorization")

        try:
            user = UserService.get_user_from_token(authorization_header)
        except (MissingAuthorizationHeader, InvalidAuthorizationHeader, TokenMissing, UserNotFound) as e:
            return Response({"message": str(e)}, status=e.status_code)

        return Payment.objects.filter(user=user)
