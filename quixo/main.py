import random
from game import Game, Move, Player


class RandomPlayer(Player):
    def __init__(self) -> None:
        super().__init__()

    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        from_pos = (random.randint(0, 4), random.randint(0, 4))
        move = random.choice([Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT])
        return from_pos, move


class MyPlayer(Player):
    def __init__(self) -> None:
        super().__init__()

    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        from_pos = (random.randint(0, 4), random.randint(0, 4))
        move = random.choice([Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT])
        return from_pos, move

class MinMax(Player):
    def __init__(self,game:Game) -> None:
        super().__init__()
        self.game = game
    
    def fitness (self,game:Game,maximizingPlayer: bool):
        if maximizingPlayer:
            player = 1
        else:
            player=0
        max_consecutive_col = 0
        max_consecutive_row = 0
        max_consecutive_diag = 0
        for row in range(0,5):
            count_col = 0
            for col in range(0,5):
                if game._board[row,col] == player : #verifico il numero di pezzi consecutivi sulle righe e ricavo il valore massimo
                    count_col+=1
                else:
                    if max_consecutive_col < count_col:
                        max_consecutive_col=count_col
                    count_col=0
        for col in range(0,5):
            count_row = 0
            for row in range(0,5):
                if game._board[row,col] == player : #verifico il numero di pezzi consecutivi sulle colonne e ricavo il valore massimo
                    count_row+=1
                else:
                    if max_consecutive_row < count_row:
                        max_consecutive_row=count_row
                    count_row=0
        
        count_diag_princ=0
        count_diag_sec=0
        max_consecutive_diag_princ=0
        max_consecutive_diag_sec=0
        for index in range (0,5): #verifico il numeri di pezzi consecutivi sulla diagonale principale e secondaria
            if game._board[index,index] == player:
                count_diag_princ+=1
            else:
                if max_consecutive_diag_princ < count_diag_princ:
                    max_consecutive_diag_princ=count_diag_princ
                count_diag_princ=0
            if game._board[index,4-index] == player:
                count_diag_sec+=1
            else:
                if max_consecutive_diag_sec < count_diag_sec:
                    max_consecutive_diag_sec=count_diag_sec
                count_diag_sec=0

        max_consecutive_diag=max(max_consecutive_diag_princ,max_consecutive_diag_sec)
        value = max_consecutive_col+max_consecutive_diag+max_consecutive_row #il valore euristico dello stato del giocatore dipende da quanti pezzi a suo favore ha consecutivi     
        return value           
                

    def minmax(self,game: Game,depth : int,maximizingPlayer: bool,alpha: float, beta: float):
        if (depth == 0) or (game.check_winner() != -1):
            return self.fitness(game,maximizingPlayer),None,alpha,beta
        player = 0
        if maximizingPlayer :
            player = 1
        if maximizingPlayer:
            value = float('-inf')
            possible_moves = game.possible_moves(player)

            for move in possible_moves:
                child = game.get_new_state(move[0],move[1],player)

                tmp,_,alpha,beta = self.minmax(child,depth-1,False,alpha,beta)
                if tmp > value:
                    value=tmp
                    best_movement = move
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
        else:
            value = float('inf')
            possible_moves = game.possible_moves(player)

            for move in possible_moves:
                child = game.get_new_state(move[0],move[1],player)

                tmp,_,alpha,beta = self.minmax(child,depth-1,True,alpha,beta)
                if tmp < value:
                    value=tmp
                    best_movement = move
                beta = min(beta, value)
                if alpha >= beta:
                    break
        return value,best_movement,alpha,beta

    def make_move(self,game: 'Game') -> tuple[tuple[int, int], Move]:
        value,best_movement,alpha,beta = self.minmax(self.game,10,True,float('-inf'), float('inf'))
        return best_movement


if __name__ == '__main__':
    g = Game()
    g.print()
    player1 = MyPlayer()
    player2 = MinMax(g)
    winner = g.play(player1, player2)
    g.print()
    print(f"Winner: Player {winner}")


