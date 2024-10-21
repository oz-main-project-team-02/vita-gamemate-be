from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

import games
from games.models.game_model import Game
from games.serializers.game_serializers import GameSerializer


class GameListView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            games = Game.objects.all()
            serializer = GameSerializer(games, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except (ValueError, ValidationError, TypeError) as e:
            # 요청이 유효하지 않거나 데이터 조회에 실패한 경우
            return Response({"error": "게임 조회에 실패하였습니다."}, status=status.HTTP_400_BAD_REQUEST)


class GameDetailView(APIView):
    def get(self, request, game_id, *args, **kwargs):
        try:
            # game_id에 해당하는 게임을 가져옴
            game = Game.objects.get(id=game_id)  # 수동으로 객체 검색
            serializer = GameSerializer(game)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Game.DoesNotExist:
            # 게임이 존재하지 않는 경우, 400 응답 반환
            return Response({"error": "해당하는 게임을 찾지 못했습니다."}, status=status.HTTP_400_BAD_REQUEST)


class PopularGameListView(APIView):
    def get(self, request):
        popular_games = Game.objects.order_by("-views")[:2]

        if not popular_games:
            return Response({"error": "인기 게임 조회에 실패하였습니다."}, status=status.HTTP_404_NOT_FOUND)

        serializer = GameSerializer(popular_games, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
