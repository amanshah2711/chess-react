from . import player
import random

class RandomPlayer(player.Player):
    
    def take_turn(self):
        move = random.choice(self.controller.possible_moves(pseudo=False))
        self.controller.take_turn(move)
    