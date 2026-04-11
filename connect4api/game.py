import random


class Board:
    """
    Represents a Connect 4 board.

    Convention: board[row][col], row 0 is the top row.
    Values: 0 = empty, 1 = first player, 2 = second player.
    """

    def __init__(self, grid: list[list[int]]) -> None:
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0]) if grid else 0

    def get_valid_columns(self) -> list[int]:
        """
        Return the list of columns that are not full.
        A column is valid if its top cell (row 0) is empty.
        """
        return [col for col in range(self.cols) if self.grid[0][col] == 0]

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

    def current_player(self) -> int:
        flat = [cell for row in self.grid for cell in row]
        return 1 if flat.count(1) == flat.count(2) else 2

    def drop_piece(self, col: int) -> None:
        """
        Place a piece for the current player in the given column.
        """
        row = self.get_next_open_row(col)
        self.grid[row][col] = self.current_player()

    def get_ai_move(self) -> int | None:
        """
        Return a random valid column for the AI to play.
        Returns None if no valid column is available (board is full).
        """
        valid_columns = self.get_valid_columns()
        if not valid_columns:
            return None
        return random.choice(valid_columns)
