
class Player(object):

    def __init__(self, color, controller=None) -> None:
        self.color = color
        self.controller = controller

    def equip(self, controller):
        self.controller = controller

    def take_turn(self):
        pass


