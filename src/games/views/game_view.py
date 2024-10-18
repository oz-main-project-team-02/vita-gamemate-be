from drf_spectacular.utils import OpenApiExample, OpenApiParameter, extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

import games
from games.models.game_model import Game
from games.serializers.game_serializers import GameSerializer
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404


class GameListView(APIView):
    @extend_schema(
        methods=["GET"],
        summary="게임 전체 조회",
        description="게임 목록을 조회하는 API입니다. 쿼리 파라미터를 사용하여 제한 수를 설정할 수 있습니다.",
        parameters=[
            OpenApiParameter(name="limit", type=int, required=False, description="가져올 게임의 최대 수"),
        ],
        responses={
            status.HTTP_200_OK: GameSerializer(many=True),  # 여러 게임 데이터를 반환
            status.HTTP_400_BAD_REQUEST: OpenApiExample(
                "게임 조회 실패 예시",
                value={"error": "게임 조회에 실패하였습니다."},
                response_only=True,
                status_codes=[400],
            )
        },
        examples=[
            OpenApiExample(
                "게임 목록 조회 예시",
                value=[
                    {
                        "id": 1,
                        "name": "Game 1",
                        "image": "image1.png",
                    },
                    {
                        "id": 2,
                        "name": "Game 2",
                        "image": "image2.png",
                    },
                ],
                response_only=True,
                status_codes=[200],
            )
        ],
    )

    def get(self, request, *args, **kwargs):
        try:
            serializer = GameSerializer(games, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (ValueError, ValidationError, TypeError) as e:
        # 요청이 유효하지 않거나 데이터 조회에 실패한 경우
            return Response({"error": "게임 조회에 실패하였습니다."}, status=status.HTTP_400_BAD_REQUEST)

class GameDetailView(APIView):
    @extend_schema(
        methods=["GET"],
        summary="특정 게임 조회",
        description="특정 게임 목록을 조회하는 API 입니다.",
        responses={
            status.HTTP_200_OK: GameSerializer(many=True),  # 여러 게임 데이터를 반환
            status.HTTP_400_BAD_REQUEST: OpenApiExample(
                "특정 게임 조회 실패 예시",
                value={"error": "해당하는 게임을 찾지 못했습니다."},
                response_only=True,
                status_codes=[400],
            )
        },
        examples=[
            OpenApiExample(
                "특정 게임 조회 예시",
                value=[
                    {
                    "id": 1,
                    "name": "Game 1",
                    "image": "Image2.png"
                    }
                ],
                response_only=True,
                status_codes=[200],
            )
        ],
    )

    def get(self, request, game_id, *args, **kwargs):
        try:
            # game_id에 해당하는 게임을 가져옴
            game = Game.objects.get(id=game_id) # 수동으로 객체 검색
            serializer = GameSerializer(game)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Game.DoesNotExist:
            # 게임이 존재하지 않는 경우, 400 응답 반환
            return Response({"error": "해당하는 게임을 찾지 못했습니다."}, status=status.HTTP_400_BAD_REQUEST)

