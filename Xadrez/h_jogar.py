import sys
from time import perf_counter

def humano_vs_humano(xadrez):
    vez_brancas = True
    start_time = None
    print('='*19)
    print("*PARTIDA INICIADA*")
    print('='*19)
    xadrez.printarTabuleiro()
    print(" ")
    while True:
        cor_atual = 'brancas' if vez_brancas else 'pretas'
        print(f"VEZ DAS {cor_atual.upper()}")

        movimento = input("\nDigite seu lance (ex: A2A4 ou 'sair'): ").strip().upper()
        if movimento == 'SAIR':
            if start_time is not None:
                tempjogo = perf_counter() - start_time
                if tempjogo >= 60:
                    minutos = int(tempjogo // 60)
                    segundos = tempjogo % 60
                    print(f"Tempo total de jogo: {minutos:.0f}:{segundos:02.0f} minutos")
                else:
                    print(f"Tempo total de jogo: {tempjogo:.2f} segundos")
            print("Jogo encerrado.")
            break

        if len(movimento) < 4:
            print("Formato inválido! Use A2A4 ou A2 A4.")
            continue

        movimento = movimento.replace(" ", "")
        origem, destino = movimento[:2], movimento[2:4]
        fen_before = xadrez.matriz_para_fen(xadrez.tabAtual)

        try:
            resultado = xadrez.moverPedra(origem, destino)
        except Exception as e:
            print("Erro:", e)
            continue

        fen_after = xadrez.matriz_para_fen(xadrez.tabAtual)
        if fen_after == fen_before:
            print("Lance inválido, tente novamente.")
            continue
        if start_time is None:
            start_time = perf_counter()

        xadrez.printarTabuleiro()
        print(f"FEN: {fen_after}")
        try:
            fim, vencedor = xadrez.verificarFimDeJogo()
            if fim is not None:
                print(f"\n{'='*60}")
                print(f"FIM DE JOGO: {fim.upper()}")
                if vencedor:
                    print(f"VENCEDOR: {vencedor}")
                print('='*60)

                if start_time is not None:
                    tempjogo = perf_counter() - start_time
                    if tempjogo >= 60:
                        minutos = int(tempjogo // 60)
                        segundos = tempjogo % 60
                        print(f"Tempo total de jogo: {minutos:.0f}:{segundos:02.0f} minutos")
                    else:
                        print(f"Tempo total de jogo: {tempjogo:.2f} segundos")
                break
        except Exception as e:
            print(f"Erro ao verificar fim de jogo: {e}")

        vez_brancas = not vez_brancas
