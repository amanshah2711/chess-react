
from . import player

class MinMaxPlayer(player.Player):
# white is negative
# black is positive

    def __init__(self, color, controller=None) -> None:
        super().__init__(color, controller)
        self.best_move = None

    def find_move(self, color, depth=4, save=False):
        if depth == 0:
            return self.heuristic()
        
        possible_moves = self.controller.possible_moves()
        if color == 'b':
            best_value = float('inf')
        elif color == 'w':
            best_value = -float('inf')

        for move in possible_moves:
            self.controller.take_turn(move)
            if color == 'b':
                value = self.find_move('w', depth - 1, False)
                if value < best_value:
                    best_value = value
                    if save:
                        self.best_move = move

            elif color == 'w':
                value = self.find_move('b', depth - 1, False)
                if value > best_value:
                    best_value = value
                    if save:
                        self.best_move = move
            self.controller.undo()

        return best_value

    def take_turn(self):
        self.find_move()
        self.controller.take_turn(self.best_move)

    def heuristic(self):
        pass
