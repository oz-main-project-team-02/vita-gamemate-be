from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from games.models.game_model import Game
from games.serializers.game_serializers import GameSerializer


class GameListView(APIView):

    def get(self, request, *args, **kwargs):
        """게임 조회에 페이지네이션 같은 걸 하지 않는 이유는 게임 등록은 admin이 하고 한정 되어 있기 때문에 하지 않음"""
        try:
            games = Game.objects.all()
        except Exception:
            return Response({"error": "게임 조회에 실패하였습니다."}, status=status.HTTP_400_BAD_REQUEST)

        return Response(GameSerializer(games, many=True).data, status=status.HTTP_200_OK)


class GameDetailView(APIView):

    def get(self, request, game_id, *args, **kwargs):
        try:
            game = Game.objects.get(id=game_id)
            serializer = GameSerializer(game)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Game.DoesNotExist:
            return Response({"error": "해당하는 게임을 찾지 못했습니다."}, status=status.HTTP_404_NOT_FOUND)
