import chess
import chess.engine

class Avaliador:
    def avaliar_posicao(self, depth=15, engine_path="C:/Users/gabri/OneDrive/Documentos/stockfish/stockfish-windows-x86-64-avx2.exe"):
        fen = self.matriz_para_fen(self.matriz)
        board = chess.Board(fen)
        engine = chess.engine.SimpleEngine.popen_uci(engine_path)
        info = engine.analyse(board, chess.engine.Limit(depth=depth))
        engine.quit()
        return info["score"].white().score(mate_score=100000) / 100

