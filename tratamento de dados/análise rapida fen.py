import chess
import chess.engine

caminho_stockfish = "C:/Users/gabri/OneDrive/Documentos/stockfish/stockfish-windows-x86-64-avx2.exe"

engine = chess.engine.SimpleEngine.popen_uci(caminho_stockfish)

while True:
    fen = input("Escreva uma FEN (ou 'sair' para encerrar): ").strip()
    if fen.lower() == "sair":
        break

    try:
        board = chess.Board(fen)
    except ValueError:
        print("FEN inválida.\n")
        continue

    info = engine.analyse(board, chess.engine.Limit(depth=15))
    score = info["score"].white().score(mate_score=100000)

    print(f"Avaliação: {score}\n")

engine.quit()
print("Finalizado.")
