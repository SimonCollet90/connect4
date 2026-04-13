from rest_framework import serializers

ROWS = 6
COLS = 7


class BoardSerializer(serializers.Serializer):
    VALID_VALUES = {0, 1, 2}

    # Board is represented by a list of rows, starting from the top row.
    board = serializers.ListField(
        child=serializers.ListField(
            child=serializers.IntegerField(),
            min_length=COLS,
            max_length=COLS,
        ),
        min_length=ROWS,
        max_length=ROWS,
    )

    def validate_board(self, board: list[list[int]]) -> list[list[int]]:
        for row in board:
            for cell in row:
                if cell not in self.VALID_VALUES:
                    raise serializers.ValidationError(
                        "Each cell must be 0 (empty), 1 (first player) or 2 "
                        "(second player)."
                    )
        self._validate_gravity(board)
        self._validate_piece_count(board)
        return board

    @staticmethod
    def _validate_gravity(board: list[list[int]]) -> None:
        for col in range(COLS):
            found_disc = False
            for row in range(ROWS):
                cell = board[row][col]
                if cell != 0:
                    found_disc = True
                elif found_disc:
                    raise serializers.ValidationError(
                        f"Invalid board: piece found above an empty cell in "
                        f"column {col}."
                    )

    @staticmethod
    def _validate_piece_count(board: list[list[int]]) -> None:
        flat = [cell for row in board for cell in row]
        count1 = flat.count(1)
        count2 = flat.count(2)
        if count1 != count2 and count1 != count2 + 1:
            raise serializers.ValidationError(
                "Invalid board: player 1 must have equal or one more piece "
                "than player 2."
            )
