from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from connect4api.game import Board
from connect4api.serializers import BoardSerializer


class NextMoveView(APIView):
    def post(self, request: Request) -> Response:
        serializer = BoardSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        board = Board(serializer.validated_data["board"])

        if board.check_winner(1):
            return Response({"status": "game_over", "winner": 1})
        if board.check_winner(2):
            return Response({"status": "game_over", "winner": 2})

        col = board.get_ai_move()
        if col is None:
            return Response({"status": "game_over", "winner": None})

        player = board.current_player()  # get current player before the move
        board.drop_piece(col)

        if board.check_winner(player):  # check if it was a winning move
            return Response({"status": "game_over", "column": col, "winner": player})

        return Response({"status": "ongoing", "column": col})
