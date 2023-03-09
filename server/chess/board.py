

class ChessBoard(object):
    
    start = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
    board_width = 8
    board_height = 8
   
    def __init__(self) -> None:
        self.board = []
        self.history= []
        self.reset()

    def reset(self):
        self.set_fen_position(ChessBoard.start)
        self.history = []

    def set_fen_position(self, fen_string) -> None:
        self.board = []
        for string_row in fen_string.split(' ')[0].split('/'):
            row = []
            for character in string_row:
                if character.isalpha():
                    row.append(character)
                elif character.isdigit():
                    row.extend(["blank"] * int(character))
                else:
                    raise Error
            self.board.append(row)

    def make_move(self, move) -> str:
        scol, srow = self._location_to_coordinate(move.start)
        ecol, erow = self._location_to_coordinate(move.end)
        piece, self.board[scol][srow] = self.board[scol][srow], 'blank' 
        self.board[ecol][erow] = piece
    
    def make_move_coord(self, srow, scol, erow, ecol):
        piece, self.board[srow][scol] = self.board[srow][scol], 'blank'
        self.board[erow][ecol] = piece

    def _location_to_coordinate(self, location):
        file = ord(location[0]) - 96
        rank = int(location[1])

        file -= 1
        rank = self.board_height - rank
        return rank, file
    
    def _coordinate_to_location(self, row, col):
        rank = str(self.board_height - row)
        file = chr(col + 97)
        return file + rank

    def is_black(self, piece):
        return piece != 'blank' and piece.lower() == piece

    def is_white(self, piece):
        return piece != 'blank' and piece.upper() == piece

    def is_blank(self, piece):
        return piece == 'blank'
    
    def in_board(self, row, col):
        return row >= 0 and row < self.board_height and col >=0 and col < self.board_width

    def white_king_coords(self):
        for i in range(self.board_height):
            for j in range(self.board_width):
                if self.board[i][j] == 'K':
                    return i, j

    def black_king_coords(self):
        for i in range(self.board_height):
            for j in range(self.board_width):
                if self.board[i][j] == 'k':
                    return i, j
        