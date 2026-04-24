from connect4api.game import Board
from connect4api.tests.boards import (
    board_column_1_full,
    empty_board,
    full_board_without_winner,
    player1_win_board,
    player1_wins_in_one,
    player2_wins_in_two,
)


class TestGetValidColumns:
    def test_empty_board(self):
        board = Board(empty_board)
        assert board.valid_columns == [0, 1, 2, 3, 4, 5, 6]

    def test_full_board(self):
        board = Board(full_board_without_winner)
        assert board.valid_columns == []

    def test_partial_board(self):
        board = Board(board_column_1_full)
        assert board.valid_columns == [0, 2, 3, 4, 5, 6]


class TestGetNextOpenRow:
    def test_empty_board(self):
        board = Board(empty_board)
        assert board.get_next_open_row(0) == 5

    def test_full_column(self):
        board = Board(full_board_without_winner)
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
        board = Board(empty_board)
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
        board = Board(empty_board)
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
        board = Board(empty_board)
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


class TestGetNextStates:
    def test_full_board_returns_empty_dict(self):
        board = Board(full_board_without_winner)
        assert board.next_states == {}

    def test_number_of_states_equals_valid_columns(self):
        board = Board(board_column_1_full)
        assert set(board.next_states.keys()) == set(board.valid_columns)

    def test_original_board_not_mutated(self):
        board = Board(empty_board)
        board.next_states
        assert board.grid[5][0] == 0

    def test_piece_is_placed_in_resulting_board(self):
        board = Board(empty_board)
        next_board = board.next_states[0]
        assert next_board.grid[5][0] == 1


class TestMinimax:
    def test_returns_zero_at_depth_zero(self):
        board = Board(empty_board)
        score, cols = board.minimax(0)
        assert score == 0.0
        assert cols == board.valid_columns

    def test_current_player_loses_immediately(self):
        # Player 1 already won; it's player 2's turn → current player loses
        board = Board(player1_win_board)
        score, cols = board.minimax(5)
        assert score == -1.0
        assert cols == []

    def test_best_cols_is_non_empty_on_open_board(self):
        board = Board(empty_board)
        _, cols = board.minimax(1)
        assert len(cols) > 0

    def test_depth_1(self):
        # Player 1 can win by playing column 3
        board = Board(player1_wins_in_one)
        score, cols = board.minimax(1)
        assert score == 1.0
        assert cols == [3]

    def test_depth_2(self):
        # Player 1 cannot prevent player 2's win
        board = Board(player2_wins_in_two)
        score, cols = board.minimax(2)
        assert score == -1.0
        assert cols == [0, 1, 2, 3, 4, 5, 6]


class TestGetAiMove:
    def test_returns_valid_column(self):
        board = Board(board_column_1_full)
        move = board.get_ai_move()
        assert move in board.valid_columns

    def test_returns_none_on_full_board(self):
        board = Board(full_board_without_winner)
        assert board.get_ai_move() is None

    def test_plays_winning_move(self):
        board = Board(player1_wins_in_one)
        assert board.get_ai_move(depth=1) == 3
