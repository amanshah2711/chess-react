
from . import player

class MinMaxPlayer(player.Player):
# white is negative
# black is positive

    def __init__(self, color, controller=None) -> None:
        super().__init__(color, controller)
        self.best_move = None
        self.counter = 0

    def find_move(self, color, depth, save=False, alpha=-float('inf'), beta=float('inf')):
        self.counter += 1
        if depth == 0:
            return self.heuristic(self.controller.board)

        possible_moves = self.controller.legal_moves()
        if color == 'b':
            best_value = -float('inf')
        elif color == 'w':
            best_value = float('inf')

        for move in possible_moves:
            self.controller.take_turn(move)
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
        self.find_move(self.color, depth=2, save=True)
        self.counter = 0
        self.controller.take_turn(self.best_move)

    def heuristic(self, board):
        total = 0
        sign = lambda piece : 1 if board.is_black(piece) else -1
        for piece in board.remaining_pieces():
            if board.is_queen(piece):
                total += sign(piece) * 9
            if board.is_bishop(piece):
                total += sign(piece) * 3
            if board.is_knight(piece):
                total += sign(piece) * 3
            if board.is_rook(piece):
                total += sign(piece) * 5
            if board.is_pawn(piece):
                total += sign(piece) * 1
        return total