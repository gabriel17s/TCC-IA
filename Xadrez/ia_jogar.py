import numpy as np
import sys
import os
import chess
from time import perf_counter

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from dataset import fen_to_input
from analisadordejogadas import load_eval_model, find_best_move

def jogar_contra_ia(xadrez, cor_jogador='brancas', profundidade=5):
    try:
        model_path = os.path.join(current_dir, "análises", "chess_eval_tf.keras")
        if not os.path.exists(model_path):
            model_path = os.path.join("tratamento de dados", "análises", "chess_eval_tf.keras")
        
        modelo_ia = load_eval_model(model_path)
        print("Modelo da IA carregado com sucesso!")

    except Exception as e:
        print(f"Erro ao carregar modelo da IA: {e}")
        print("Modo IA desativado. Use o modo Humano vs Humano.")
        return
    
    #print(f"Você está jogando com as {cor_jogador.upper()}")
    print(f"A IA está usando avaliação neural + busca em profundidade ({profundidade})")

    print('='*19)
    print("*PARTIDA INICIADA*")
    print('='*19)

    xadrez.printartabuleiroemoji()
    print("")

    vez_brancas = True
    start_time = None

    while True:
        cor_atual = 'brancas' if vez_brancas else 'pretas'
        print(f"VEZ DAS {cor_atual.upper()}")

        if cor_atual == cor_jogador:
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

            xadrez.printartabuleiroemoji()
            print(f"FEN: {fen_after}")
            try:
                model_path = os.path.join(current_dir, "análises", "chess_eval_tf.keras")
                if not os.path.exists(model_path):
                    model_path = os.path.join("tratamento de dados", "análises", "chess_eval_tf.keras")
                modelo_ia = load_eval_model(model_path)

                avaliacao = avaliar_posicao_simples(modelo_ia, fen_after)
                print(f"Avaliação: {avaliacao:+.2f} -->", end=" ")
                interpretar_avaliacao(avaliacao)
            except Exception as e:
                print(f"Erro na avaliação: {e}")
            print("")

        else:
            print("\nIA está analisando a posição...", end=" ")

            fen_atual = xadrez.matriz_para_fen(xadrez.tabAtual)
            board_chess = chess.Board(fen_atual)

            try:
                melhor_lance, avaliacao = find_best_move(
                    modelo_ia, 
                    board_chess, 
                    max_depth=profundidade,
                    time_limit=10.0
                )
            except Exception as e:
                print(f"Erro na busca da IA: {e}")
                melhor_lance = None
                avaliacao = None

            if melhor_lance is None:
                print("IA não encontrou um lance válido! Usando fallback...")
                melhor_lance = fallback_melhor_lance(xadrez, modelo_ia, cor_atual)
                if melhor_lance is None:
                    print("Nenhum lance possível encontrado!")
                    break

            origem_ia = melhor_lance.uci()[:2].upper()
            destino_ia = melhor_lance.uci()[2:4].upper()

            print(f"IA escolheu: {origem_ia}{destino_ia}")

            if board_chess.turn == chess.WHITE:
                avaliacao_final = avaliacao
            else:
                avaliacao_final = -avaliacao if avaliacao is not None else 0

            try:
                xadrez.moverPedra(origem_ia, destino_ia)

                if start_time is None:
                    start_time = perf_counter()

                xadrez.printartabuleiroemoji()
                fen_apos_ia = xadrez.matriz_para_fen(xadrez.tabAtual)
                print(f"FEN: {fen_apos_ia}")

                if avaliacao_final is not None:
                    print(f"Avaliação: {avaliacao_final/100:+.2f} -->", end=" ")
                    interpretar_avaliacao(avaliacao_final/100)

            except Exception as e:
                print(f"Erro ao executar lance da IA: {e}")
                if not executar_fallback(xadrez, cor_atual):
                    break

            print("")


        try:
            fim, vencedor = xadrez.verificarFimDeJogo()
            if fim is not None:
                print(f"\n{'='*60}")
                print(f"FIM DE JOGO: {fim.upper()}")
                if vencedor:
                    if vencedor == cor_jogador:
                        print(f"VITÓRIA DO JOGADOR HUMANO!")
                    else:
                        print(f"VITÓRIA DA IA!")
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


def avaliar_posicao_simples(modelo, fen):

    try:
        planes, extras = fen_to_input(fen)
        Xp = np.expand_dims(planes, axis=0)
        Xe = np.expand_dims(extras, axis=0)
        predicao = modelo.predict([Xp, Xe], verbose=0)
        avaliacao = float(np.squeeze(predicao)) * 10.0
        return avaliacao
    except Exception as e:
        print(f"Erro na avaliação simples: {e}")
        return 0.0


def fallback_melhor_lance(xadrez, modelo, cor):

    print("Usando fallback: análise simples de todos os lances...")

    try:
        lances = xadrez.buscarTodosLances(cor)
    except Exception as e:
        print(f"Erro ao buscar lances: {e}")
        return None

    if not lances:
        return None

    melhor_lance = None
    melhor_avaliacao = -9999 if cor == 'brancas' else 9999

    for (origem_x, origem_y), (destino_x, destino_y) in lances:
        try:
            tab_simulado = xadrez.simularMovimento((origem_x, origem_y), (destino_x, destino_y))
            fen_simulada = xadrez.matriz_para_fen(tab_simulado)

            avaliacao = avaliar_posicao_simples(modelo, fen_simulada)

            if cor == 'pretas':
                avaliacao = -avaliacao

            if (cor == 'brancas' and avaliacao > melhor_avaliacao) or \
               (cor == 'pretas' and avaliacao < melhor_avaliacao):
                melhor_avaliacao = avaliacao

                colunas = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
                origem_str = f"{colunas[origem_y]}{8 - origem_x}"
                destino_str = f"{colunas[destino_y]}{8 - destino_x}"

                movimento_str = f"{origem_str.lower()}{destino_str.lower()}"
                melhor_lance = chess.Move.from_uci(movimento_str)

        except Exception as e:
            print(f"Erro ao analisar lance: {e}")
            continue

    if melhor_lance:
        print(f"Fallback escolheu: {melhor_lance.uci().upper()}")
    return melhor_lance


def executar_fallback(xadrez, cor):
    try:
        lances = xadrez.buscarTodosLances(cor)
        if lances:
            (origem_x, origem_y), (destino_x, destino_y) = lances[0]
            colunas = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
            origem_str = f"{colunas[origem_y]}{8 - origem_x}"
            destino_str = f"{colunas[destino_y]}{8 - destino_x}"

            try:
                xadrez.moverPedra(origem_str, destino_str)
                print(f"Movimento de fallback executado: {origem_str}{destino_str}")
                xadrez.printartabuleiroemoji()
                return True
            except Exception as e:
                print(f"Erro ao executar fallback: {e}")
    except Exception as e:
        print(f"Erro ao buscar lances para fallback: {e}")

    return False


def interpretar_avaliacao(avaliacao):

    abs_avaliacao = abs(avaliacao)

    if abs_avaliacao < 0.3:
        print("Posição equilibrada")
    elif abs_avaliacao < 0.8:
        if avaliacao > 0:
            print("Ligeira vantagem para as brancas")
        else:
            print("Ligeira vantagem para as pretas")
    elif abs_avaliacao < 1.5:
        if avaliacao > 0:
            print("Vantagem clara para as brancas")
        else:
            print("Vantagem clara para as pretas")
    elif abs_avaliacao < 3.0:
        if avaliacao > 0:
            print("Vantagem decisiva para as brancas")
        else:
            print("Vantagem decisiva para as pretas")
    else:
        if avaliacao > 0:
            print("Posição vitoriosa para as brancas")
        else:
            print("Posição vitoriosa para as pretas")
