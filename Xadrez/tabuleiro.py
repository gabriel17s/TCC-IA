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
        for i in range(8):
            self.matriz[6][i] = "P"

        self.matriz[7] = ["T", "C", "B", "D", "R", "B", "C", "T"]

        for i in range(8):
            self.matriz[1][i] = "p"

        self.matriz[0] = ["t", "c", "b", "d", "r", "b", "c", "t"]

        self.tabAtual = [linha[:] for linha in self.matriz]

    def printartabuleiro(self):
        print('A B C D E F G H |')
        print("————————————————————")
        colunaRef = list(range(8, 0, -1))
        for i, linha in enumerate(self.tabAtual):
            print(" ".join(f"{elem}" for elem in linha), "|", colunaRef[i])

    def printartabuleiroemoji(self):
        mapa = {
            "t": "♖", "c": "♘", "b": "♗", "d": "♕", "r": "♔", "p": "♙",
            "T": "♜", "C": "♞", "B": "♝", "D": "♛", "R": "♚", "P": "♟"
        }
        clara = "◼"
        escura = " "

        print("A B C D E F G H |")
        print("————————————————————")
        colunaRef = list(range(8, 0, -1))

        for i, linha in enumerate(self.tabAtual):
            exibicao = []
            for j, casa in enumerate(linha):
                if casa == ".":
                    quad = clara if (i + j) % 2 == 0 else escura
                    exibicao.append(quad)
                else:
                    exibicao.append(mapa.get(casa, "?"))
            print(" ".join(exibicao), "|", colunaRef[i])

        print("————————————————————")
        print("A B C D E F G H |")