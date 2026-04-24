from connect4api.game import Board
from connect4api.tests.boards import (
    BOARD_1_FULL_COLUMN,
    EMPTY_BOARD,
    FULL_BOARD_WITHOUT_WINNER,
)


class TestGetValidColumns:
    def test_empty_board(self):
        board = Board(EMPTY_BOARD)
        assert board.valid_columns == [0, 1, 2, 3, 4, 5, 6]

    def test_full_board(self):
        board = Board(FULL_BOARD_WITHOUT_WINNER)
        assert board.valid_columns == []

    def test_partial_board(self):
        board = Board(BOARD_1_FULL_COLUMN)
        assert board.valid_columns == [0, 2, 3, 4, 5, 6]


class TestGetNextOpenRow:
    def test_empty_board(self):
        board = Board(EMPTY_BOARD)
        assert board.get_next_open_row(0) == 5

    def test_full_column(self):
        board = Board(FULL_BOARD_WITHOUT_WINNER)
        assert board.get_next_open_row(0) is None

    def test_partial_column(self):
        board = Board(
            [
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0, 0],
                [2, 0, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0, 0],
            ]
        )
        assert board.get_next_open_row(0) == 2


class TestCheckWinner:
    def test_no_winner(self):
        board = Board(EMPTY_BOARD)
        assert board.check_winner(1) is False

    def test_horizontal_winner(self):
        board = Board(
            [
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 1, 0, 0, 0],
            ]
        )
        assert board.check_winner(1) is True

    def test_vertical_winner(self):
        board = Board(
            [
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0, 0],
            ]
        )
        assert board.check_winner(1) is True

    def test_diagonal_top_left_to_bottom_right_winner(self):
        board = Board(
            [
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0, 0],
                [0, 1, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0],
            ]
        )
        assert board.check_winner(1) is True

    def test_diagonal_top_right_to_bottom_left_winner(self):
        board = Board(
            [
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0],
                [0, 1, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0, 0],
            ]
        )
        assert board.check_winner(1) is True

    def test_winner_player_2(self):
        board = Board(
            [
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [2, 2, 2, 2, 0, 0, 0],
            ]
        )
        assert board.check_winner(2) is True


class TestCurrentPlayer:
    def test_player1_starts(self):
        board = Board(EMPTY_BOARD)
        assert board.current_player == 1

    def test_player2_after_first_move(self):
        board = Board(
            [
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0, 0],
            ]
        )
        assert board.current_player == 2

    def test_player1_after_two_moves(self):
        board = Board(
            [
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [1, 2, 0, 0, 0, 0, 0],
            ]
        )
        assert board.current_player == 1


class TestDropPiece:
    def test_piece_lands_at_bottom_of_empty_column(self):
        board = Board(EMPTY_BOARD)
        board.drop_piece(0)
        assert board.grid[5][0] == 1

    def test_piece_lands_on_top_of_existing_pieces(self):
        board = Board(
            [
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0, 0],
                [2, 0, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0, 0],
            ]
        )
        board.drop_piece(0)
        assert board.grid[2][0] == 2


class TestGetAiMove:
    def test_returns_valid_column(self):
        board = Board(BOARD_1_FULL_COLUMN)
        move = board.get_ai_move()
        assert move in board.valid_columns

    def test_returns_none_on_full_board(self):
        board = Board(FULL_BOARD_WITHOUT_WINNER)
        assert board.get_ai_move() is None

    def test_returns_only_available_column(self):
        board = Board(
            [
                [1, 1, 1, 0, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1],
            ]
        )
        assert board.get_ai_move() == 3
