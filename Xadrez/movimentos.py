class Movimentos:
    def verificarTurno(self, pedra):
        return (self.turno == 'brancas' and pedra.isupper()) or (self.turno == 'pretas' and pedra.islower())

    def mudarTurno(self):
        self.turno = 'pretas' if self.turno == 'brancas' else 'brancas'

    def movimentoRei(self, pedra, x, y, tabuleiro=None):
        if tabuleiro is None:
            tabuleiro = self.tabAtual
        movimentos_validos = []
        possiveis_movimentos = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),          (0, 1),
            (1, -1),  (1, 0), (1, 1)
        ]
        for dx, dy in possiveis_movimentos:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                destino = tabuleiro[nx][ny]
                if destino == ".":
                    movimentos_validos.append((x, y, nx, ny))
                elif (pedra.isupper() and destino.islower()) or (pedra.islower() and destino.isupper()):
                    movimentos_validos.append((x, y, nx, ny))
        return movimentos_validos

    def movimentoBispo(self, pedra, x, y, tabuleiro=None):
        if tabuleiro is None:
            tabuleiro = self.tabAtual
        possiveis_movimentos = [(-1, +1), (-1, -1), (1, +1), (1, -1)]
        movimentos_validos = []
        for dx, dy in possiveis_movimentos:
            nx, ny = x + dx, y + dy
            while 0 <= nx < 8 and 0 <= ny < 8:
                destino = tabuleiro[nx][ny]
                if destino == ".":
                    movimentos_validos.append((x, y, nx, ny))
                elif (pedra.isupper() and destino.islower()) or (pedra.islower() and destino.isupper()):
                    movimentos_validos.append((x, y, nx, ny))
                    break
                else:
                    break
                nx += dx
                ny += dy
        return movimentos_validos

    def movimentoDama(self, pedra, x, y, tabuleiro=None):
        if tabuleiro is None:
            tabuleiro = self.tabAtual
        movimentos_validos = []
        direcoes = [
            (-1, 0), (1, 0), (0, -1), (0, 1),
            (-1, -1), (-1, 1), (1, -1), (1, 1)
        ]
        for dx, dy in direcoes:
            nx, ny = x + dx, y + dy
            while 0 <= nx < 8 and 0 <= ny < 8:
                destino = tabuleiro[nx][ny]
                if destino == ".":
                    movimentos_validos.append((x, y, nx, ny))
                elif (pedra.isupper() and destino.islower()) or (pedra.islower() and destino.isupper()):
                    movimentos_validos.append((x, y, nx, ny))
                    break
                else:
                    break
                nx += dx
                ny += dy
        return movimentos_validos

    def movimentoPeao(self, pedra, x, y, tabuleiro=None):
        if tabuleiro is None:
            tabuleiro = self.tabAtual
        
        movimentos_validos = []
        
        if pedra == 'p':
         
            if x + 1 < 8:
                destino = tabuleiro[x + 1][y]
                if destino == '.':
                    movimentos_validos.append((x, y, x + 1, y))
            
          
            if x == 1 and x + 2 < 8:
                if tabuleiro[x + 1][y] == '.' and tabuleiro[x + 2][y] == '.':
                    movimentos_validos.append((x, y, x + 2, y))
            
           
            if x + 1 < 8 and y + 1 < 8:
                captura1 = tabuleiro[x + 1][y + 1]
                if captura1 != '.' and captura1.isupper():
                    movimentos_validos.append((x, y, x + 1, y + 1))
            if x + 1 < 8 and y - 1 >= 0:
                captura2 = tabuleiro[x + 1][y - 1]
                if captura2 != '.' and captura2.isupper():
                    movimentos_validos.append((x, y, x + 1, y - 1))
            
          
            if x == 4: 
              
                if y + 1 < 8 and tabuleiro[x][y + 1].lower() == 'p' and tabuleiro[x][y + 1] == '.' and self.jogadas:
                    ultima_jogada = self.jogadas[-1]
                    origem_x, origem_y = ultima_jogada[0]
                    destino_x, destino_y = ultima_jogada[1]
                    if origem_x == 6 and destino_x == 4 and origem_y == y + 1:
                        
                        movimentos_validos.append((x, y, x + 1, y + 1))  
                        
                if y - 1 >= 0 and tabuleiro[x][y - 1].lower() == 'p' and tabuleiro[x][y - 1] == '.' and self.jogadas:
                    ultima_jogada = self.jogadas[-1]
                    origem_x, origem_y = ultima_jogada[0]
                    destino_x, destino_y = ultima_jogada[1]
                    if origem_x == 6 and destino_x == 4 and origem_y == y - 1:
                      
                        movimentos_validos.append((x, y, x + 1, y - 1))  

            return movimentos_validos

        if pedra == 'P':
            if x - 1 >= 0:
                destino = tabuleiro[x - 1][y]
                if destino == '.':
                    movimentos_validos.append((x, y, x - 1, y))
            
            if x == 6 and x - 2 >= 0:
                if tabuleiro[x - 1][y] == '.' and tabuleiro[x - 2][y] == '.':
                    movimentos_validos.append((x, y, x - 2, y))
            
           
            if x - 1 >= 0 and y + 1 < 8:
                captura1 = tabuleiro[x - 1][y + 1]
                if captura1 != '.' and captura1.islower():
                    movimentos_validos.append((x, y, x - 1, y + 1))
            if x - 1 >= 0 and y - 1 >= 0:
                captura2 = tabuleiro[x - 1][y - 1]
                if captura2 != '.' and captura2.islower():
                    movimentos_validos.append((x, y, x - 1, y - 1))
            
           
            if x == 3: 
                if y + 1 < 8 and tabuleiro[x][y + 1].lower() == 'p' and tabuleiro[x][y + 1] == '.' and self.jogadas:
                    ultima_jogada = self.jogadas[-1]
                    origem_x, origem_y = ultima_jogada[0]
                    destino_x, destino_y = ultima_jogada[1]
                    if origem_x == 1 and destino_x == 3 and origem_y == y + 1:
                      
                        movimentos_validos.append((x, y, x - 1, y + 1))  

                if y - 1 >= 0 and tabuleiro[x][y - 1].lower() == 'p' and tabuleiro[x][y - 1] == '.' and self.jogadas:
                    ultima_jogada = self.jogadas[-1]
                    origem_x, origem_y = ultima_jogada[0]
                    destino_x, destino_y = ultima_jogada[1]
                    if origem_x == 1 and destino_x == 3 and origem_y == y - 1:
                       
                        movimentos_validos.append((x, y, x - 1, y - 1))  

            return movimentos_validos


    def movimentoCavalo(self, pedra, x, y, tabuleiro=None):
        if tabuleiro is None:
            tabuleiro = self.tabAtual
        movimentos_validos = []
        possiveis_movimentos = [
            (-2, 1), (-2, -1), (2, 1), (2, -1),
            (-1, 2), (-1, -2), (1, 2), (1, -2)
        ]
        for dx, dy in possiveis_movimentos:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                destino = tabuleiro[nx][ny]
                if destino == '.':
                    movimentos_validos.append((x, y, nx, ny))
                elif (pedra.isupper() and destino.islower()) or (pedra.islower() and destino.isupper()):
                    movimentos_validos.append((x, y, nx, ny))
        return movimentos_validos

    def movimentoTorre(self, pedra, x, y, tabuleiro=None):
        if tabuleiro is None:
            tabuleiro = self.tabAtual
        movimentos_validos = []
        direcoes = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in direcoes:
            nx, ny = x + dx, y + dy
            while 0 <= nx < 8 and 0 <= ny < 8:
                destino = tabuleiro[nx][ny]
                if destino == '.':
                    movimentos_validos.append((x, y, nx, ny))
                elif (pedra.isupper() and destino.islower()) or (pedra.islower() and destino.isupper()):
                    movimentos_validos.append((x, y, nx, ny))
                    break
                else:
                    break
                nx += dx
                ny += dy
        return movimentos_validos