import pytest
from rest_framework.test import APIClient

from connect4api.tests.boards import (
    ai_winning_move_board,
    empty_board,
    full_board_without_winner,
    player1_win_board,
    player2_win_board,
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
        response = client.post(URL, {"board": empty_board}, format="json")
        assert response.status_code == 200

    def test_ongoing_game_returns_column(self, client):
        response = client.post(URL, {"board": empty_board}, format="json")
        assert response.data["status"] == "ongoing"
        assert response.data["column"] in range(7)
        assert "winner" not in response.data

    def test_player1_already_won(self, client):
        response = client.post(URL, {"board": player1_win_board}, format="json")
        assert response.data["status"] == "game_over"
        assert response.data["winner"] == 1
        assert "column" not in response.data

    def test_player2_already_won(self, client):
        response = client.post(URL, {"board": player2_win_board}, format="json")
        assert response.data["status"] == "game_over"
        assert response.data["winner"] == 2
        assert "column" not in response.data

    def test_ai_plays_winning_move(self, client):
        response = client.post(URL, {"board": ai_winning_move_board}, format="json")
        assert response.data["status"] == "game_over"
        assert response.data["column"] == 3
        assert response.data["winner"] == 2

    def test_full_board_returns_game_over(self, client):
        response = client.post(URL, {"board": full_board_without_winner}, format="json")
        assert response.data["status"] == "game_over"
        assert response.data["winner"] is None
        assert "column" not in response.data
