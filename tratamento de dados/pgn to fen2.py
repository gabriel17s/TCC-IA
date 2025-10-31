import os
import io
import re
import csv
import chess.pgn

INPUT_DIR = "PGN2"
OUTPUT_DIR = "partidas"
CSV_OUT = os.path.join(OUTPUT_DIR, "brancas_below_1200_fens.csv")
PGN_OUT = os.path.join(OUTPUT_DIR, "brancas_below_1200.pgn")

os.makedirs(OUTPUT_DIR, exist_ok=True)

def parse_int_safe(value):
    if value is None:
        return None
    m = re.search(r'\d+', str(value))
    return int(m.group(0)) if m else None

def read_text_from_file(path):
    try:
        b = open(path, "rb").read()
    except Exception:
        return None
    try:
        text = b.decode("utf-8")
    except UnicodeDecodeError:
        try:
            text = b.decode("latin-1")
        except Exception:
            return None
    if "[" not in text or "1." not in text:
        if re.search(r'\[Event\s+"', text):
            return text
        return None
    return text

games_found = 0
filtered_games = []
rows = []

for fname in os.listdir(INPUT_DIR) if os.path.isdir(INPUT_DIR) else []:
    fpath = os.path.join(INPUT_DIR, fname)
    if not os.path.isfile(fpath):
        continue
    if not any(fname.lower().endswith(ext) for ext in (".pgn", ".txt", ".pgn.gz", ".gz", ".png")):
        continue

    text = read_text_from_file(fpath)
    if not text:
        continue

    pgn_io = io.StringIO(text)
    while True:
        try:
            game = chess.pgn.read_game(pgn_io)
        except Exception:
            break
        if game is None:
            break
        games_found += 1

        headers = game.headers
        white_elo = parse_int_safe(headers.get("WhiteElo"))
        if white_elo is None:
            white_elo = parse_int_safe(headers.get("WhiteRating"))
        if white_elo is None:
            continue

        if white_elo < 1000:
            board = game.board()
            for mv in game.mainline_moves():
                board.push(mv)
            final_fen = board.fen()

            site = headers.get("Site", "")
            event = headers.get("Event", "")
            white = headers.get("White", "")
            black = headers.get("Black", "")
            result = headers.get("Result", "")
            date = headers.get("UTCDate", headers.get("Date", ""))
            time = headers.get("UTCTime", headers.get("Time", ""))

            rows.append({
                "file": fname,
                "Event": event,
                "Site": site,
                "White": white,
                "Black": black,
                "WhiteElo": white_elo,
                "BlackElo": parse_int_safe(headers.get("BlackElo")),
                "Result": result,
                "Date": date,
                "Time": time,
                "FEN_final": final_fen
            })

            filtered_games.append(game)

with open(CSV_OUT, "w", newline="", encoding="utf-8") as csvf:
    fieldnames = ["file","Event","Site","White","Black","WhiteElo","BlackElo","Result","Date","Time","FEN_final"]
    writer = csv.DictWriter(csvf, fieldnames=fieldnames)
    writer.writeheader()
    for r in rows:
        writer.writerow(r)

with open(PGN_OUT, "w", encoding="utf-8") as pgnf:
    for g in filtered_games:
        exporter = chess.pgn.FileExporter(pgnf)
        g.accept(exporter)
        pgnf.write("\n")

print(f"Processados {games_found} jogos lidos. Encontradas {len(filtered_games)} partidas com WhiteElo < 1200.")
print(f"CSV salvo em: {CSV_OUT}")
print(f"PGN salvo em: {PGN_OUT}")
