import numpy as np
import re

PIECES = "PNBRQKpnbrqk"
IDX = {c: i for i, c in enumerate(PIECES)}

def fen_to_planes(fen: str):
    parts = fen.strip().split()
    board, turn, castling, ep = parts[0], parts[1], parts[2], parts[3]
    planes = np.zeros((8, 8, 13), dtype=np.float32)
    
    r = 0
    for row in board.split('/'):
        c = 0
        for ch in row:
            if ch.isdigit():
                c += int(ch)
            else:
                if ch in IDX:
                    planes[r, c, IDX[ch]] = 1.0
                c += 1
        r += 1

    if ep != '-':
        col = ord(ep[0]) - ord('a')
        row = 8 - int(ep[1])
        if 0 <= row < 8 and 0 <= col < 8:
            planes[row, col, 12] = 1.0
    
    side = np.array([1.0 if turn == 'w' else -1.0], dtype=np.float32)
    cast = np.array([
        1.0 if 'K' in castling else 0.0,
        1.0 if 'Q' in castling else 0.0,
        1.0 if 'k' in castling else 0.0,
        1.0 if 'q' in castling else 0.0,
    ], dtype=np.float32)
    
    extras = np.concatenate([side, cast], dtype=np.float32)
    return planes, extras

def fen_to_input(fen: str):
    planes, extras = fen_to_planes(fen)
    return planes, extras

def parse_line(line: str):
    if ':' not in line:
        return None
    fen, score = line.split(':', 1)
    fen = fen.strip()
    try:
        score = float(score.strip())
    except:
        return None
    return fen, score

def load_dataset(path, clip=1000.0):
    X_planes = []
    X_extras = []
    y = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            p = parse_line(line)
            if not p:
                continue
            fen, score = p
            planes, extras = fen_to_planes(fen)
            X_planes.append(planes)
            X_extras.append(extras)
            score = max(-clip, min(clip, score))
            y.append(score / clip)
    
    X_planes = np.stack(X_planes)
    X_extras = np.stack(X_extras)
    y = np.array(y, dtype=np.float32)[:, None]
    return (X_planes, X_extras), y