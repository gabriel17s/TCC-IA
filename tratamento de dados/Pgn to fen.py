#import chess.pgn
#import os
#import glob

#out_dir = os.path.join("xadrez", "partidas")
#os.makedirs(out_dir, exist_ok=True)

#arquivos_pgn = glob.glob#(r"C:\Users\gabri\OneDrive\Documentos\TCC\PGN2\Azmaiparashvili.txt")

#out_path = os.path.join(out_dir, "partidas2.txt")

#with open(out_path, "w") as out:
#    for arquivo in arquivos_pgn:
#        with open(arquivo) as f:
#            while True:
#                game = chess.pgn.read_game(f)
#                if game is None:
#                    break

 #               board = game.board()
  #              for move in game.mainline_moves():
   #                 board.push(move)
    #                out.write(board.fen() + "\n")

     #           out.write("\n")

import chess.pgn
import os
import sys

in_path = r"C:\Users\gabri\OneDrive\Documentos\TCC\PGN2\Spielmann.PGN"
out_dir = os.path.join("xadrez", "partidas")
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "partidas_spielmann.txt")

if not os.path.exists(in_path):
    print(f"Arquivo não encontrado: {in_path}", file=sys.stderr)
    sys.exit(1)

# Abra com encoding e erros substituídos para evitar crash por caracteres estranhos
with open(in_path, "r", encoding="utf-8", errors="replace") as fin, \
     open(out_path, "w", encoding="utf-8") as out:

    jogos = 0
    while True:
        game = chess.pgn.read_game(fin)
        if game is None:
            break
        jogos += 1

        board = game.board()
        moved = False
        for mv in game.mainline_moves():
            moved = True
            board.push(mv)
            out.write(board.fen() + "\n")

        # garante uma linha em branco entre partidas
        out.write("\n")

print(f"Concluído: {jogos} partidas processadas -> {out_path}")
