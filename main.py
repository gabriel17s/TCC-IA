import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from Xadrez.tabuleiro import Xadrez
from Xadrez.ia_jogar import jogar_contra_ia
from Xadrez.h_jogar import humano_vs_humano

xadrez = Xadrez()

print("\nEscolha o modo de jogo:\n1 - Humano vs Humano\n2 - Humano vs IA")

while True:
    modo = input("Digite 1 ou 2: ").strip()
    if modo == "1" or modo == "2":
        break
    print("Por favor digite '1' ou '2' para jogar.")
print("")

if modo == "2":
    cor_jogador = 'brancas'
    jogar_contra_ia(xadrez, cor_jogador, profundidade=5)
else:
    humano_vs_humano(xadrez)