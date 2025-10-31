# pgntofenpt2.py
import os
import io
import re
import chess
import chess.pgn

INPUT_PATH = "PGN2/lichess.pgn"
OUTPUT_PATH = "partidas/lichess.txt"

os.makedirs(os.path.dirname(OUTPUT_PATH) or ".", exist_ok=True)

def read_text_file(path):
    b = open(path, "rb").read()
    try:
        return b.decode("utf-8")
    except UnicodeDecodeError:
        return b.decode("latin-1", errors="ignore")

def looks_like_fen(line: str) -> bool:
    line = line.strip()
    if not line:
        return False
    parts = line.split()
    if len(parts) < 4:
        return False
    board = parts[0]
    if "/" not in board:
        return False
    if not re.fullmatch(r"[prnbqkPRNBQK1-8/]+", board):
        return False
    return True

text = read_text_file(INPUT_PATH)
pgn_io = io.StringIO(text)

fens_output = []
any_game = False
games_count = 0
fens_count = 0

while True:
    try:
        game = chess.pgn.read_game(pgn_io)
    except Exception:
        break
    if game is None:
        break
    any_game = True
    games_count += 1
    board = game.board()
    for mv in game.mainline_moves():
        board.push(mv)
        fens_output.append(board.fen())
        fens_count += 1
    fens_output.append("")

if not any_game:
    current_group_has_lines = False
    for raw in text.splitlines():
        s = raw.strip()
        if s == "":
            if current_group_has_lines:
                fens_output.append("")
                current_group_has_lines = False
            continue
        if looks_like_fen(s):
            fens_output.append(s)
            fens_count += 1
            current_group_has_lines = True
        else:
            continue

if fens_output and fens_output[-1] == "":
    fens_output = fens_output[:-1]

with open(OUTPUT_PATH, "w", encoding="utf-8") as out:
    out.write("\n".join(fens_output))

print(f"Gravado em: {OUTPUT_PATH}")
print(f"Partidas detectadas (approx): {games_count if any_game else 'não detectado como PGN'}")
print(f"FENs escritas: {fens_count}")
