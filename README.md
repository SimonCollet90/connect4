# connect4

REST API for playing Connect 4 against a computer.

## Installation

```bash
git clone <repo-url>
cd connect4
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Endpoints

### `POST /api/next_move/`

Submit the current board state and receive the AI's next move.

#### Request body

```json
{
  "board": [
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0],
    [0, 0, 2, 1, 0, 0, 0]
  ]
}
```

The board is a list of 6 rows of 7 columns, from top to bottom. Each cell is:
- `0` — empty
- `1` — player 1
- `2` — player 2

**Validation rules:**
- The board must respect gravity: no piece can float above an empty cell in the same column.
- Player 1 must have the same number of pieces as player 2, or exactly one more (player 1 always goes first).

#### Responses

**Game ongoing** — the AI plays in column `column` (0-indexed):

```json
{"status": "ongoing", "column": 3}
```

**Game over** — the AI plays a winning move:

```json
{"status": "game_over", "column": 3, "winner": 2}
```

**Game over** — a player had already won before the call:

```json
{"status": "game_over", "winner": 1}
```

**Game over** — board is full, draw:

```json
{"status": "game_over", "winner": null}
```

**Invalid request** (HTTP 400):

```json
{"board": ["Invalid board: piece found above an empty cell in column 3."]}
```

#### Example with curl

```bash
curl -X POST http://localhost:8000/api/next_move/ \
  -H "Content-Type: application/json" \
  -d '{
    "board": [
      [0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 1, 0, 0, 0],
      [0, 0, 2, 1, 0, 0, 0]
    ]
  }'
```