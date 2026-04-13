import pytest
from rest_framework.test import APIClient

from connect4api.tests.boards import (
    AI_WINNING_MOVE_BOARD,
    EMPTY_BOARD,
    FULL_BOARD_WITHOUT_WINNER,
    PLAYER1_WIN_BOARD,
    PLAYER2_WIN_BOARD,
)

URL = "/api/next_move/"


@pytest.fixture
def client():
    return APIClient()


class TestNextMoveView:
    def test_get_method_not_allowed(self, client):
        response = client.get(URL)
        assert response.status_code == 405

    def test_invalid_board_returns_400(self, client):
        response = client.post(URL, {"board": "invalid"}, format="json")
        assert response.status_code == 400

    def test_valid_board_returns_200(self, client):
        response = client.post(URL, {"board": EMPTY_BOARD}, format="json")
        assert response.status_code == 200

    def test_ongoing_game_returns_column(self, client):
        response = client.post(URL, {"board": EMPTY_BOARD}, format="json")
        assert response.data["status"] == "ongoing"
        assert response.data["column"] in range(7)
        assert "winner" not in response.data

    def test_player1_already_won(self, client):
        response = client.post(URL, {"board": PLAYER1_WIN_BOARD}, format="json")
        assert response.data["status"] == "game_over"
        assert response.data["winner"] == 1
        assert "column" not in response.data

    def test_player2_already_won(self, client):
        response = client.post(URL, {"board": PLAYER2_WIN_BOARD}, format="json")
        assert response.data["status"] == "game_over"
        assert response.data["winner"] == 2
        assert "column" not in response.data

    def test_ai_plays_winning_move(self, client):
        response = client.post(URL, {"board": AI_WINNING_MOVE_BOARD}, format="json")
        assert response.data["status"] == "game_over"
        assert response.data["column"] == 3
        assert response.data["winner"] == 2

    def test_full_board_returns_game_over(self, client):
        response = client.post(URL, {"board": FULL_BOARD_WITHOUT_WINNER}, format="json")
        assert response.data["status"] == "game_over"
        assert response.data["winner"] is None
        assert "column" not in response.data
