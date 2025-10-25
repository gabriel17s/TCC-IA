import time
import math
import numpy as np
import chess
from tensorflow.keras.models import load_model
from dataset import fen_to_planes

MODEL_PATH = "tratamento de dados/análises/chess_eval_tf.keras"
CLIP = 1000.0
QUIESCENCE_MAX_DEPTH = 6

def load_eval_model(path=MODEL_PATH):
    model = load_model(path, compile=False)
    return model

def evaluate_model(model, board: chess.Board, clip=CLIP):
    fen = board.fen()
    planes, extras = fen_to_planes(fen)
    Xp = np.expand_dims(planes, axis=0)
    Xe = np.expand_dims(extras, axis=0)
    v = model.predict([Xp, Xe], verbose=0)
    v0 = float(np.squeeze(v))
    return v0 * clip

class TranspositionTable:
    def __init__(self):
        self.table = {}
    def get(self, key):
        return self.table.get(key, None)
    def store(self, key, value, depth, flag):
        self.table[key] = (value, depth, flag)

def order_moves(board: chess.Board, moves):
    mvlist = list(moves)
    def key(m):
        score = 0
        if board.is_capture(m):
            score += 1000
        if m.promotion:
            score += 500
        return -score
    mvlist.sort(key=key)
    return mvlist

def quiescence(board: chess.Board, alpha, beta, model, max_depth=QUIESCENCE_MAX_DEPTH, depth=0):
    v_white = evaluate_model(model, board)
    v_to_move = v_white if board.turn == chess.WHITE else -v_white
    stand_pat = v_to_move
    if stand_pat >= beta:
        return beta
    if alpha < stand_pat:
        alpha = stand_pat
    if depth >= max_depth:
        return stand_pat
    for move in order_moves(board, board.legal_moves):
        if not board.is_capture(move) and not move.promotion:
            continue
        board.push(move)
        score = -quiescence(board, -beta, -alpha, model, max_depth, depth+1)
        board.pop()
        if score >= beta:
            return beta
        if score > alpha:
            alpha = score
    return alpha

def negamax(board: chess.Board, depth, alpha, beta, model, tt: TranspositionTable):
    key = board.fen()
    entry = tt.get(key)
    if entry is not None:
        val, edepth, flag = entry
        if edepth >= depth:
            if flag == "EXACT":
                return val
            elif flag == "LOWER" and val >= beta:
                return val
            elif flag == "UPPER" and val <= alpha:
                return val
    if depth == 0:
        q = quiescence(board, alpha, beta, model)
        tt.store(key, q, depth, "EXACT")
        return q
    alpha_orig = alpha
    best_value = -math.inf
    moves = order_moves(board, board.legal_moves)
    if not moves:
        if board.is_checkmate():
            return -100000
        else:
            return 0
    for mv in moves:
        board.push(mv)
        score = -negamax(board, depth-1, -beta, -alpha, model, tt)
        board.pop()
        if score > best_value:
            best_value = score
        if best_value > alpha:
            alpha = best_value
        if alpha >= beta:
            break
    if best_value <= alpha_orig:
        flag = "UPPER"
    elif best_value >= beta:
        flag = "LOWER"
    else:
        flag = "EXACT"
    tt.store(key, best_value, depth, flag)
    return best_value

def find_best_move(model, board: chess.Board, max_depth=4, time_limit=None):
    tt = TranspositionTable()
    best_move = None
    best_score = None
    start_time = time.time()
    for depth in range(1, max_depth + 1):
        if time_limit is not None and (time.time() - start_time) > time_limit:
            break
        alpha = -1e9
        beta = 1e9
        best_value = -math.inf
        best_at_this_depth = None
        moves = order_moves(board, board.legal_moves)
        if not moves:
            break
        for mv in moves:
            board.push(mv)
            score = -negamax(board, depth-1, -beta, -alpha, model, tt)
            board.pop()
            if score > best_value:
                best_value = score
                best_at_this_depth = mv
            if (time_limit is not None) and (time.time() - start_time) > time_limit:
                break
        if best_at_this_depth is not None:
            best_move = best_at_this_depth
            best_score = best_value
    return best_move, best_score

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default=MODEL_PATH)
    parser.add_argument("--fen", default=None)
    parser.add_argument("--depth", type=int, default=3)
    parser.add_argument("--time", type=float, default=None)
    args = parser.parse_args()
    model = load_eval_model(args.model)
    if args.fen:
        board = chess.Board(args.fen)
    else:
        board = chess.Board()
    mv, score = find_best_move(model, board, max_depth=args.depth, time_limit=args.time)
    print("Melhor lance:", mv)
    if score is None:
        print("Avaliação: None")
    else:
        if board.turn == chess.WHITE:
            eval_white = score
        else:
            eval_white = -score
        print("Avaliação:", eval_white/100)
    if mv:
        b2 = board.copy()
        b2.push(mv)
        print(f"FEN após melhor lance: {b2.fen()}")
