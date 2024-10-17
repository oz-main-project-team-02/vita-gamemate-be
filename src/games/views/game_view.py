from drf_spectacular.utils import OpenApiExample, OpenApiParameter, extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from games.models.game_model import Game
from games.serializers.game_serializers import GameSerializer


class GameListView(APIView):
    @extend_schema(
        methods=["GET"],
        tags=["아직 개발중입니다. 사용을 멈춰주세요!"],
        summary="게임 목록 조회",
        description="게임 목록을 조회하는 API입니다. 쿼리 파라미터를 사용하여 정렬 및 제한 수를 설정할 수 있습니다.",
        parameters=[
            OpenApiParameter(name="sort", type=str, required=False, description="정렬 기준 (created_at: 최신순, nav: 기본순)"),
            OpenApiParameter(name="limit", type=int, required=False, description="가져올 게임의 최대 수"),
        ],
        responses={
            status.HTTP_200_OK: GameSerializer(many=True),  # 여러 게임 데이터를 반환
        },
        examples=[
            OpenApiExample(
                "게임 목록 조회 예시",
                value=[
                    {
                        "id": 1,
                        "name": "Game 1",
                        "image": "image1.png",
                        "created_at": "2024-01-01T00:00:00Z",
                        "updated_at": "2024-01-02T00:00:00Z",
                    },
                    {
                        "id": 2,
                        "name": "Game 2",
                        "image": "image2.png",
                        "created_at": "2024-01-02T00:00:00Z",
                        "updated_at": "2024-01-03T00:00:00Z",
                    },
                ],
                response_only=True,
                status_codes=[200],
            )
        ],
    )
    def get(self, request, *args, **kwargs):
        limit = request.query_params.get("limit")
        sort = request.query_params.get("sort")
        games = Game.objects.all()

        if sort == "nav":
            games = games.order_by("name")  # 이름순으로 정렬 (네비게이션 용)
        elif sort == "best":  # 인기순 정렬 (임시로 'updated_at'으로 처리, 실제로는 인기 데이터를 기준으로)
            games = games.order_by("-updated_at")

        if limit is not None:
            games = games[: int(limit)]

        serializer = GameSerializer(games, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
