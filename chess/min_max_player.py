
from . import player
import time

class MinMaxPlayer(player.Player):
# white is negative
# black is positive

    def __init__(self, color, controller=None) -> None:
        super().__init__(color, controller)
        self.best_move = None
        self.counter = 0

    def find_move(self, color, depth, save=False, alpha=-float('inf'), beta=float('inf')):
        if depth == 0:
            return self.heuristic(self.controller.board)

        tic = time.perf_counter()
        possible_moves = self.controller.legal_moves()
        toc = time.perf_counter()
        print(f"The time to think of a move was {toc - tic:0.6f} seconds")
        if color == 'b':
            best_value = -float('inf')
        elif color == 'w':
            best_value = float('inf')

        for move in possible_moves:
            self.controller.take_turn(move, bypass=True)
            if color == 'b':
                maximin_value = self.find_move('w', depth - 1, False, alpha, beta)
                if maximin_value > best_value:
                    best_value = maximin_value
                    alpha = max(alpha, best_value)
                    if save:
                        self.best_move = move

            elif color == 'w':
                minimax_value = self.find_move('b', depth - 1, False, alpha, beta)
                if minimax_value < best_value:
                    best_value = minimax_value
                    beta = min(beta, best_value)
                    if save:
                        self.best_move = move
            self.controller.undo()
            if alpha >= beta:
                break

        return best_value

    def take_turn(self):
        self.find_move(self.color, depth=3, save=True)
        self.controller.take_turn(self.best_move)

    def heuristic(self, board):
        total = 0
        sign = lambda i, j: 1 if board.is_black(i, j) else -1
        for i, j in board.get_locations():
            if board.is_queen(i, j):
                total += sign(i, j) * 9
            if board.is_bishop(i, j):
                total += sign(i, j) * 3
            if board.is_knight(i, j):
                total += sign(i, j) * 3
            if board.is_rook(i, j):
                total += sign(i, j) * 5
            if board.is_pawn(i, j):
                total += sign(i, j) * 1
        return total