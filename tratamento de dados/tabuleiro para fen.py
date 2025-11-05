MAP = {'t':'r', 'c':'n', 'b':'b', 'd':'q', 'r':'k', 'p':'p'}

def line_to_fen_rank(line):
    line = line.strip().replace(" ", "")
    if len(line) != 8:
        raise ValueError("Cada linha deve ter exatamente 8 caracteres (pode usar '.' para vazio).")
    fen_parts = []
    empty_count = 0
    for ch in line:
        if ch == '.':
            empty_count += 1
            continue
        if empty_count:
            fen_parts.append(str(empty_count))
            empty_count = 0
        key = ch.lower()
        if key not in MAP:
            raise ValueError(f"Caractere inválido: '{ch}'. Use t,c,b,d,r,p ou '.'")
        piece = MAP[key]
        if ch.isupper():
            fen_parts.append(piece.upper())
        else:
            fen_parts.append(piece.lower())
    if empty_count:
        fen_parts.append(str(empty_count))
    return "".join(fen_parts)

def board_to_fen(lines):
    if len(lines) != 8:
        raise ValueError("Forneça exatamente 8 linhas.")
    ranks = [line_to_fen_rank(l) for l in lines]
    placement = "/".join(ranks)

    return f"{placement} b - - 0 1"

tab = [
    ["t","c","b","d","r","b","c","t"],
    ["p","p","p","p","p","p","p","p"],
    [".",".",".",".",".",".",".","."],
    [".",".",".",".",".",".",".","."],
    [".",".",".",".",".",".",".","."],
    [".",".",".",".",".",".",".","."],
    ["P","P","P","P","P","P","P","P"],
    ["T","C","B","D","R","B","C","T"]
]

print("Tabuleiro inicial: \n")
print("A B C D E F G H |")
print("------------------")
for i, linha in enumerate(tab):
    print(" ".join(linha), "|", 8 - i)
print("\n")

def main():
    print("Cole/Digite 8 linhas do tabuleiro (use '.' para vazio).")
    lines = []
    for i in range(8):
        l = input(f"linha {i+1}: ")
        lines.append(l)
    try:
        fen = board_to_fen(lines)
    except ValueError as e:
        print("Erro:", e)
        return
    print("\nFEN gerada:")
    print(fen)

if __name__ == "__main__":
    main()
