
from msilib.schema import Error
from multiprocessing.dummy import Array
from tokenize import String

class ChessBoard(object):
    
    start = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
    board_width = 8
    board_height = 8
   
    def __init__(self) -> None:
        self.board = []
        for string_row in self.start.split(' ')[0].split('/'):
            row = []
            for character in string_row:
                if character.isalpha():
                    row.append(character)
                elif character.isdigit():
                    row.append(["blank"] * int(character))
                else:
                    raise Error
            self.board.append(row)
        assert len(self.board_height) == 8 and len(self.board_width == 8)


        