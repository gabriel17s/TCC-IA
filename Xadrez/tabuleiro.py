from .movimentos import Movimentos
from .regras import Regras
from .utils import Utils
from .avaliador import Avaliador

class Xadrez(Movimentos, Regras, Utils, Avaliador):
    def __init__(self):
        self.matriz = [["." for _ in range(8)] for _ in range(8)]
        self.tabAtual = []
        self.turno = "brancas"
        self.jogadas = []
        self.criarTabuleiro()

    def criarTabuleiro(self):
        # Peões brancos
        for i in range(8):
            self.matriz[6][i] = "P"

        # Peças brancas
        self.matriz[7] = ["T", "C", "B", "D", "R", "B", "C", "T"]

        # Peões pretos
        for i in range(8):
            self.matriz[1][i] = "p"

        # Peças pretas
        self.matriz[0] = ["t", "c", "b", "d", "r", "b", "c", "t"]

        self.tabAtual = [linha[:] for linha in self.matriz]

    def printarTabuleiro(self):
        print('A B C D E F G H |')
        print("————————————————————")
        colunaRef = list(range(8, 0, -1))
        for i, linha in enumerate(self.tabAtual):
            print(" ".join(f"{elem}" for elem in linha), "|", colunaRef[i])
