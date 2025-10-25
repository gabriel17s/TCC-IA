def __init__(self, tabuleiro=None, turno="brancas", jogadas=None):
    """
    Inicializa estado mínimo esperado pela classe Regras.
    - tabuleiro: opcional, matriz 8x8; se None, usa posição inicial padrão.
    - turno: "brancas" ou "pretas"
    - jogadas: lista de jogadas (cada item: (origem, destino) onde origem/destino pode ser tuple ou string)
    """
    # posição inicial (interno: T=torre, C=cavalo, B=bispo, D=dama, R=rei, P=peão)
    inicio = [
        list("tcbdrbct"),  # linha 0 = rank 8 (pretas)
        list("pppppppp"),  # linha 1 = rank 7 (peões pretos)
        list("........"),  # linha 2
        list("........"),  # linha 3
        list("........"),  # linha 4
        list("........"),  # linha 5
        list("PPPPPPPP"),  # linha 6 = rank 2 (peões brancos)
        list("TCBDR BCT".replace(" ", ""))  # linha 7 = rank 1 (brancas)
    ]
    # Nota: a linha acima usa TCBDR BCT sem espaços; se quiser ser explícito:
    inicio[7] = ['T','C','B','D','R','B','C','T']

    # Atribuições principais
    self.tabAtual = [row[:] for row in (tabuleiro if tabuleiro is not None else inicio)]
    self.turno = turno  # "brancas" ou "pretas"
    self.jogadas = list(jogadas) if jogadas else []

    # extras úteis (usados pela FEN / regras)
    self.en_passant = None          # coordenada alvo de en-passant (ex: (3,4)) ou None
    self.halfmove_clock = 0
    self.fullmove_number = 1

    # métodos/flags que sua lógica pode depender — inicializar por segurança
    # (não alteram lógica se você não usar)
    self.ultimo_movimento = None    # guarda último movimento bruto se quiser
    # garantir formato correto (8x8)
    if len(self.tabAtual) != 8 or any(len(r) != 8 for r in self.tabAtual):
        raise ValueError("tabuleiro deve ser 8x8")
