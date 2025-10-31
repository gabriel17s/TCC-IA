class Regras:
    def _to_coords(self, pos):
        if isinstance(pos, tuple):
            return pos
        if isinstance(pos, list):
            return tuple(pos)
        if isinstance(pos, str):
            try:
                return self.algebraica_para_coords(pos)
            except Exception:
                return None
        return None

    def _posicao_moveu(self, pos):
        pos_coords = self._to_coords(pos)
        if pos_coords is None:
            return False
        for jog in getattr(self, "jogadas", []):
            origem = jog[0] if len(jog) > 0 else None
            origem_coords = self._to_coords(origem)
            if origem_coords == pos_coords:
                return True
        return False

    def emXeque(self, cor, tabuleiro=None):
        if tabuleiro is None:
            tabuleiro = self.tabAtual
        
        rei = 'R' if cor == 'brancas' else 'r'
        rei_x, rei_y = -1, -1
        for i in range(8):
            for j in range(8):
                if tabuleiro[i][j] == rei:
                    rei_x, rei_y = i, j
                    break
            if rei_x != -1:
                break
        if rei_x == -1:
            return False

        for i in range(8):
            for j in range(8):
                peca = tabuleiro[i][j]
                if peca == '.':
                    continue
                if (cor == 'brancas' and peca.islower()) or (cor == 'pretas' and peca.isupper()):
                    movimentos = []
                    if peca.lower() == 'p':
                        movimentos = self.movimentoPeao(peca, i, j, tabuleiro)
                    elif peca.lower() == 't':
                        movimentos = self.movimentoTorre(peca, i, j, tabuleiro)
                    elif peca.lower() == 'c':
                        movimentos = self.movimentoCavalo(peca, i, j, tabuleiro)
                    elif peca.lower() == 'b':
                        movimentos = self.movimentoBispo(peca, i, j, tabuleiro)
                    elif peca.lower() == 'd':
                        movimentos = self.movimentoDama(peca, i, j, tabuleiro)
                    elif peca.lower() == 'r':
                        movimentos = self.movimentoRei(peca, i, j, tabuleiro)
                    
                    for mov in movimentos:
                        if mov[2] == rei_x and mov[3] == rei_y:
                            return True
        return False

    def simularMovimento(self, origem, destino):
        tabuleiro_simulado = [linha[:] for linha in self.tabAtual]
        origem_x, origem_y = origem
        destino_x, destino_y = destino
        pedra = tabuleiro_simulado[origem_x][origem_y]
        tabuleiro_simulado[destino_x][destino_y] = pedra
        tabuleiro_simulado[origem_x][origem_y] = "."
        return tabuleiro_simulado

    def buscarTodosLances(self, cor=None):
        lances_possiveis = []
        if cor is None:
            cor = self.turno
        for i in range(8):
            for j in range(8):
                peca = self.tabAtual[i][j]
                if (cor == "brancas" and peca.isupper()) or (cor == "pretas" and peca.islower()):
                    movimentos_validos = []
                    if peca.upper() == 'T':
                        movimentos_validos = self.movimentoTorre(peca, i, j)
                    elif peca.upper() == 'C':
                        movimentos_validos = self.movimentoCavalo(peca, i, j)
                    elif peca.upper() == 'P':
                        movimentos_validos = self.movimentoPeao(peca, i, j)
                    elif peca.upper() == 'B':
                        movimentos_validos = self.movimentoBispo(peca, i, j)
                    elif peca.upper() == 'R':
                        movimentos_validos = self.movimentoRei(peca, i, j)
                        if cor == self.turno:
                            resultado_roque = self.pode_fazer_roque(cor)
                            if resultado_roque in ('roque pequeno', 'roque ambos'):
                                movimentos_validos.append((i, j, i, j + 2))
                            if resultado_roque in ('roque grande', 'roque ambos'):
                                movimentos_validos.append((i, j, i, j - 2))
                    elif peca.upper() == 'D':
                        movimentos_validos = self.movimentoDama(peca, i, j)
                    else:
                        continue

                    for movimento in movimentos_validos:
                        destino_i, destino_j = movimento[2], movimento[3]
                        if destino_i < 0 or destino_i > 7 or destino_j < 0 or destino_j > 7:
                            continue
                        if self.tabAtual[destino_i][destino_j] != '.':
                            peca_destino = self.tabAtual[destino_i][destino_j]
                            if (cor == "brancas" and peca_destino.isupper()) or (cor == "pretas" and peca_destino.islower()):
                                continue
                        tabuleiro_simulado = self.simularMovimento((i, j), (destino_i, destino_j))
                        if self.emXeque(cor, tabuleiro_simulado):
                            continue
                        lances_possiveis.append(((i, j), (destino_i, destino_j)))
        return lances_possiveis

    def pode_fazer_roque(self, cor):

        if self.emXeque(cor):
            return False

        if cor == 'brancas':
            rei_pos = (7, 4)
            torre_esq_pos = (7, 0)
            torre_dir_pos = (7, 7)
            adversaria = 'pretas'
            rei_char = 'R'
            torre_char = 'T'
        else:
            rei_pos = (0, 4)
            torre_esq_pos = (0, 0)
            torre_dir_pos = (0, 7)
            adversaria = 'brancas'
            rei_char = 'r'
            torre_char = 't'

        if self.tabAtual[rei_pos[0]][rei_pos[1]] != rei_char:
            return False

        torre_esq_presente = (self.tabAtual[torre_esq_pos[0]][torre_esq_pos[1]] == torre_char)
        torre_dir_presente = (self.tabAtual[torre_dir_pos[0]][torre_dir_pos[1]] == torre_char)

        if self._posicao_moveu(rei_pos):
            return False

        pode_pequeno = False
        pode_grande = False

        lances_adversarios = self.buscarTodosLances(cor=adversaria)
        casas_proibidas = {lance[1] for lance in lances_adversarios}

        row = rei_pos[0]

        if torre_esq_presente and not self._posicao_moveu(torre_esq_pos):
            if (self.tabAtual[row][1] == '.' and self.tabAtual[row][2] == '.' and self.tabAtual[row][3] == '.'):
                if (rei_pos not in casas_proibidas) and ((row,2) not in casas_proibidas) and ((row,3) not in casas_proibidas):
                    pode_grande = True

        if torre_dir_presente and not self._posicao_moveu(torre_dir_pos):
            if (self.tabAtual[row][5] == '.' and self.tabAtual[row][6] == '.'):
                if (rei_pos not in casas_proibidas) and ((row,5) not in casas_proibidas) and ((row,6) not in casas_proibidas):
                    pode_pequeno = True

        if pode_pequeno and pode_grande:
            return 'roque ambos'
        if pode_pequeno:
            return 'roque pequeno'
        if pode_grande:
            return 'roque grande'
        return False

    def matriz_para_fen(self, tabuleiro=None):
        if tabuleiro is None:
            tabuleiro = self.tabAtual
        mapa = {
            'P':'P','p':'p',
            'T':'R','t':'r',
            'C':'N','c':'n',
            'B':'B','b':'b',
            'D':'Q','d':'q',
            'R':'K','r':'k',
            '.':'.'
        }
        fen_rows = []
        for linha in tabuleiro:
            row_fen = ""
            empty = 0
            for cell in linha:
                ch = mapa[cell]
                if ch == '.':
                    empty += 1
                else:
                    if empty:
                        row_fen += str(empty)
                        empty = 0
                    row_fen += ch
            if empty:
                row_fen += str(empty)
            fen_rows.append(row_fen)
        fen = "/".join(fen_rows)
        fen += " " + ("w" if self.turno == "brancas" else "b")

        roque = ""
        res_b = self.pode_fazer_roque('brancas')
        if res_b in ('roque pequeno', 'roque ambos'):
            roque += "K"
        if res_b in ('roque grande', 'roque ambos'):
            roque += "Q"
        res_p = self.pode_fazer_roque('pretas')
        if res_p in ('roque pequeno', 'roque ambos'):
            roque += "k"
        if res_p in ('roque grande', 'roque ambos'):
            roque += "q"
        if not roque:
            roque = "-"
        fen += " " + roque

        fen += " -"
        fen += " 0 1"
        return fen

    def verificarFimDeJogo(self):
        lances = self.buscarTodosLances(self.turno)
        if not lances:
            if self.emXeque(self.turno):
                vencedor = "pretas" if self.turno == "brancas" else "brancas"
                print(f"Xeque mate! Vitória das {vencedor}.")
                return "xeque mate", vencedor
            else:
                print("Empate por afogamento!")
                return "empate", None
        return None, None

    def validarLance(self, pedra, origem, destino, checkTurn=True):
        origem_x, origem_y = origem
        destino_x, destino_y = destino

        if (origem_x > 7 or origem_y > 7 or destino_x > 7 or destino_y > 7 or
            origem_x < 0 or origem_y < 0 or destino_x < 0 or destino_y < 0):
            print("Lance inválido: Posições fora do tabuleiro")
            return None

        if checkTurn and not self.verificarTurno(pedra):
            print("Lance inválido: Não é a vez dessa cor")
            return None

        if pedra.upper() == 'T':
            movimentos_validos = self.movimentoTorre(pedra, origem_x, origem_y)
        elif pedra.upper() == 'C':
            movimentos_validos = self.movimentoCavalo(pedra, origem_x, origem_y)
        elif pedra.upper() == 'P':
            movimentos_validos = self.movimentoPeao(pedra, origem_x, origem_y)
        elif pedra.upper() == 'B':
            movimentos_validos = self.movimentoBispo(pedra, origem_x, origem_y)
        elif pedra.upper() == 'R':
            movimentos_validos = self.movimentoRei(pedra, origem_x, origem_y)
            resultado_roque = self.pode_fazer_roque(self.turno)
            if resultado_roque in ('roque pequeno', 'roque ambos'):
                movimentos_validos.append((origem_x, origem_y, origem_x, origem_y + 2))
            if resultado_roque in ('roque grande', 'roque ambos'):
                movimentos_validos.append((origem_x, origem_y, origem_x, origem_y - 2))
        elif pedra.upper() == 'D':
            movimentos_validos = self.movimentoDama(pedra, origem_x, origem_y)
        else:
            return None

        if (origem_x, origem_y, destino_x, destino_y) not in movimentos_validos:
            return None

        tabuleiro_simulado = self.simularMovimento((origem_x, origem_y), (destino_x, destino_y))
        if self.emXeque(self.turno, tabuleiro_simulado):
            print("Lance inválido: o rei ficará em xeque após o movimento")
            return None

        return movimentos_validos

    def algebraica_para_coords(self, pos):
        colunas = {'A':0,'B':1,'C':2,'D':3,'E':4,'F':5,'G':6,'H':7}
        col = colunas[pos[0].upper()]
        row = 8 - int(pos[1])
        return (row, col)

    def moverPedra(self, origem, destino):
        if isinstance(origem, str):
            origem = self.algebraica_para_coords(origem)
        if isinstance(destino, str):
            destino = self.algebraica_para_coords(destino)
        origem_x, origem_y = origem
        destino_x, destino_y = destino
        pedra = self.tabAtual[origem_x][origem_y]

        if not self.verificarTurno(pedra):
            print("Lance inválido: Não é a vez dessa cor")
            return

        if (destino_x, destino_y) == (origem_x, origem_y + 2) or (destino_x, destino_y) == (origem_x, origem_y - 2):
            resultado_roque = self.pode_fazer_roque(self.turno)
            if resultado_roque:
                if destino_y == origem_y + 2 and resultado_roque in ('roque pequeno', 'roque ambos'):
                    self.tabAtual[origem_x][origem_y] = "."
                    self.tabAtual[origem_x][origem_y + 2] = "R" if self.turno == 'brancas' else "r"
                    self.tabAtual[origem_x][7] = "."
                    self.tabAtual[origem_x][5] = "T" if self.turno == 'brancas' else "t"
                    print("Roque pequeno realizado!")
                elif destino_y == origem_y - 2 and resultado_roque in ('roque grande', 'roque ambos'):
                    self.tabAtual[origem_x][origem_y] = "."
                    self.tabAtual[origem_x][origem_y - 2] = "R" if self.turno == 'brancas' else "r"
                    self.tabAtual[origem_x][0] = "."
                    self.tabAtual[origem_x][3] = "T" if self.turno == 'brancas' else "t"
                    print("Roque grande realizado!")
                else:
                    print("Roque inválido!")
                    return
                self.jogadas.append((origem, destino))
                self.mudarTurno()
                return
            else:
                print("Roque inválido!")
                return

        if self.validarLance(pedra, origem, destino) is None:
            print("Lance inválido: Movimento não permitido para essa peça")
            return

        if pedra.upper() == 'P' and origem_y != destino_y and self.tabAtual[destino_x][destino_y] == '.':
            self.tabAtual[origem_x][destino_y] = "."

        self.tabAtual[destino_x][destino_y] = pedra
        self.tabAtual[origem_x][origem_y] = "."

        if pedra == 'P' and destino_x == 0:
            escolha = input("Promover para (D=Torre, T=Torre, B=Bispo, C=Cavalo): ").upper()
            if escolha in ['D', 'T', 'B', 'C']:
                self.tabAtual[destino_x][destino_y] = escolha
                print(f"Peão promovido a {escolha}!")
            else:
                self.tabAtual[destino_x][destino_y] = 'D'
                print("Escolha inválida. Peão promovido a Dama por padrão.")
        elif pedra == 'p' and destino_x == 7:
            escolha = input("Promover para (d=dama, t=torre, b=bispo, c=cavalo): ").lower()
            if escolha in ['d', 't', 'b', 'c']:
                self.tabAtual[destino_x][destino_y] = escolha
                print(f"Peão promovido a {escolha}!")
            else:
                self.tabAtual[destino_x][destino_y] = 'd'
                print("Escolha inválida. Peão promovido a dama por padrão.")

        self.jogadas.append((origem, destino))
        self.mudarTurno()

        fim, vencedor = self.verificarFimDeJogo()
        if fim == "xeque mate":
            print(f"Fim de jogo: Xeque mate! Vitória das {vencedor}.")
        elif fim == "empate":
            print("Fim de jogo: Empate por afogamento.")
