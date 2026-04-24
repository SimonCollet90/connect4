import copy
import random


class Board:
    """
    Represents a Connect 4 board.

    Convention: board[row][col], row 0 is the top row.
    Values: 0 = empty, 1 = first player, 2 = second player.
    """

    def __init__(self, grid: list[list[int]]) -> None:
        self.grid = copy.deepcopy(grid)
        self.rows = len(grid)
        self.cols = len(grid[0]) if grid else 0

    @staticmethod
    def cell_str(player: int) -> str:
        if player == 1:
            return "X"
        elif player == 2:
            return "O"
        else:
            return "."

    def __str__(self) -> str:
        return "\n".join(
            ["".join([self.cell_str(cell) for cell in row]) for row in self.grid]
        )

    @property
    def valid_columns(self) -> list[int]:
        """
        Return the list of columns that are not full.
        A column is valid if its top cell (row 0) is empty.
        """
        return [col for col in range(self.cols) if self.grid[0][col] == 0]

    @property
    def next_states(self) -> dict[int, Board]:
        """
        Return a dict mapping each valid column to the resulting Board after dropping a
        piece there.
        """
        next_states = dict()
        for col in self.valid_columns:
            new_board = Board(self.grid)
            new_board.drop_piece(col)
            next_states[col] = new_board
        return next_states

    @property
    def current_player(self) -> int:
        flat = [cell for row in self.grid for cell in row]
        return 2 if flat.count(1) > flat.count(2) else 1

    def get_next_open_row(self, col: int) -> int | None:
        """
        Return the lowest empty row in a given column.
        Returns None if the column is full.
        """
        for row in range(self.rows - 1, -1, -1):
            if self.grid[row][col] == 0:
                return row
        return None

    def check_winner(self, player: int) -> bool:
        """
        Check if the given player has won.
        Checks all directions: horizontal, vertical, and both diagonals.
        """
        # Horizontal
        for row in range(self.rows):
            for col in range(self.cols - 3):
                if all(self.grid[row][col + i] == player for i in range(4)):
                    return True

        # Vertical
        for col in range(self.cols):
            for row in range(self.rows - 3):
                if all(self.grid[row + i][col] == player for i in range(4)):
                    return True

        # Diagonal top-left to bottom-right
        for row in range(self.rows - 3):
            for col in range(self.cols - 3):
                if all(self.grid[row + i][col + i] == player for i in range(4)):
                    return True

        # Diagonal top-right to bottom-left
        for row in range(self.rows - 3):
            for col in range(3, self.cols):
                if all(self.grid[row + i][col - i] == player for i in range(4)):
                    return True

        return False

    def drop_piece(self, col: int) -> bool:
        """
        Place a piece for the current player in the given column.
        Returns True if the operation was successful, False otherwise.
        """
        row = self.get_next_open_row(col)
        if row is None:
            return False
        self.grid[row][col] = self.current_player
        return True

    def minimax(self, depth: int) -> tuple[float, list[int]]:
        """
        Return (score, best_columns) using negamax convention.
        Score is from the perspective of the current player:
        +1 = win,
        -1 = loss,
         0 = draw/unknown.
        """
        player = self.current_player
        opponent = 3 - player
        if self.check_winner(opponent):
            return -1.0, []
        next_states = self.next_states
        if not next_states or depth == 0:
            return 0.0, self.valid_columns

        best_score = float("-inf")
        best_cols: list[int] = []
        for col, board in next_states.items():
            score, _ = board.minimax(depth - 1)
            score = -score
            if score > best_score:
                best_score, best_cols = score, [col]
            elif score == best_score:
                best_cols.append(col)

        return best_score, best_cols

    def get_ai_move(self, depth: int = 4) -> int | None:
        """
        Return the best column for the AI to play using minimax at the given depth.
        Returns None if no valid column is available (board is full).
        """
        _, best_cols = self.minimax(depth)
        if not best_cols:
            return None
        return random.choice(best_cols)
