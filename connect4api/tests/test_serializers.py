from connect4api.serializers import BoardSerializer

VALID_BOARD = [
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0],
    [0, 1, 2, 0, 0, 0, 0],
]


class TestBoardSerializerValidBoard:
    def test_valid_board(self):
        serializer = BoardSerializer(data={'board': VALID_BOARD})
        assert serializer.is_valid() is True


class TestBoardSerializerDimensions:
    def test_too_many_rows(self):
        board = VALID_BOARD + [[0, 0, 0, 0, 0, 0, 0]]
        serializer = BoardSerializer(data={'board': board})
        assert serializer.is_valid() is False

    def test_too_few_rows(self):
        board = VALID_BOARD[:-1]
        serializer = BoardSerializer(data={'board': board})
        assert serializer.is_valid() is False

    def test_too_many_cols(self):
        board = [row + [0] for row in VALID_BOARD]
        serializer = BoardSerializer(data={'board': board})
        assert serializer.is_valid() is False

    def test_too_few_cols(self):
        board = [row[:-1] for row in VALID_BOARD]
        serializer = BoardSerializer(data={'board': board})
        assert serializer.is_valid() is False


class TestBoardSerializerInvalidValues:
    def test_invalid_value(self):
        board = [row[:] for row in VALID_BOARD]
        board[5][6] = 3
        serializer = BoardSerializer(data={'board': board})
        assert serializer.is_valid() is False

    def test_negative_value(self):
        board = [row[:] for row in VALID_BOARD]
        board[5][6] = -1
        serializer = BoardSerializer(data={'board': board})
        assert serializer.is_valid() is False


class TestBoardSerializerGravity:
    def test_piece_above_empty_cell(self):
        board = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
        ]
        serializer = BoardSerializer(data={'board': board})
        assert serializer.is_valid() is False


class TestBoardSerializerPieceCount:
    def test_player2_has_more_pieces_than_player1(self):
        board = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [2, 2, 1, 0, 0, 0, 0],
        ]
        serializer = BoardSerializer(data={'board': board})
        assert serializer.is_valid() is False

    def test_player1_has_two_more_pieces_than_player2(self):
        board = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 2, 0, 0, 0],
        ]
        serializer = BoardSerializer(data={'board': board})
        assert serializer.is_valid() is False

    def test_equal_piece_count(self):
        board = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [1, 2, 0, 0, 0, 0, 0],
        ]
        serializer = BoardSerializer(data={'board': board})
        assert serializer.is_valid() is True
