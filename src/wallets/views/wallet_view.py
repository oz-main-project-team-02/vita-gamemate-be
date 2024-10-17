from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.services.user_service import UserService
from wallets.models.wallets_model import Wallet
from wallets.serializers.wallets_serializers import WalletRechargeSerializer


class WalletBalanceView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="지갑 잔액 조회",
        description="사용자의 지갑에 있는 현재 코인 잔액을 조회하는 API입니다.",
        parameters=[
            OpenApiParameter(name="user_id", description="사용자 ID (유저 PK)", required=True, type=int, location=OpenApiParameter.PATH),
        ],
        responses={
            200: OpenApiResponse(
                response={
                    "type": "object",
                    "properties": {"user_id": {"type": "integer", "example": 1}, "coin_balance": {"type": "integer", "example": 100}},
                },
                description="Successful Balance Query",
            ),
            404: OpenApiResponse(
                response={"type": "object", "properties": {"error": {"type": "string", "example": "지갑을 찾을 수 없습니다."}}},
                description="Wallet Not Found",
            ),
        },
    )
    def get(self, request, *args, **kwargs):
        user, error_response = UserService.get_user_from_token(request.headers.get("Authorization"))
        if error_response:
            return error_response

        try:
            wallet = Wallet.objects.get(user_id=user.id)
            return Response({"user_id": user.id, "coin_balance": wallet.coin}, status=status.HTTP_200_OK)
        except Wallet.DoesNotExist:
            return Response({"error": "지갑을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)


class WalletRechargeView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WalletRechargeSerializer

    @extend_schema(
        summary="지갑 코인 충전",
        description="사용자의 지갑에 코인을 충전하는 API입니다. 쿼리 파라미터로 충전할 코인 수를 전달해야 합니다.",
        parameters=[
            OpenApiParameter(name="coin", description="충전할 코인 수", required=True, type=int, location=OpenApiParameter.QUERY),
            OpenApiParameter(name="user_id", description="사용자 ID (유저 PK)", required=True, type=int, location=OpenApiParameter.PATH),
        ],
        responses={
            200: OpenApiResponse(
                response={
                    "type": "object",
                    "properties": {
                        "message": {"type": "string", "example": "코인이 성공적으로 충전되었습니다."},
                        "new_balance": {"type": "integer", "example": 150},
                    },
                },
                description="Successful Coin Recharge",
            ),
            404: OpenApiResponse(
                response={"type": "object", "properties": {"error": {"type": "string", "example": "지갑을 찾을 수 없습니다."}}},
                description="Wallet Not Found",
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        user, error_response = UserService.get_user_from_token(request.headers.get("Authorization"))
        if error_response:
            return error_response

        serializer = self.serializer_class(data={"coin": request.query_params.get("coin")})
        serializer.is_valid(raise_exception=True)
        coin_amount = serializer.validated_data["coin"]


        try:
            wallet = Wallet.objects.get(user_id=user.id)
        except Wallet.DoesNotExist:
            return Response({"error": "지갑을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        wallet.coin += coin_amount
        wallet.save()

        return Response({"message": "코인이 성공적으로 충전되었습니다.", "new_balance": wallet.coin}, status=status.HTTP_200_OK)
