
class ChessBoard(object):
    
    start = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
    board_width = 8
    board_height = 8
   
    def __init__(self) -> None:
        self.board = []
        self.locations = []
        self.reset()

    def reset(self):
        self.set_fen_position(ChessBoard.start)

    def set_fen_position(self, fen_string) -> None:
        self.board = []
        self.locations = []
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

        for i in range(self.board_height):
            for j in range(self.board_width):
                if self.board[i][j] != 'blank':
                    self.locations.append((i, j))

    def get(self, row, col):
        return self.board[row][col]

    def get_coord(self, row, col):
        return self.board[row][col]
    
    def get_locations(self):
        return self.locations[:]

    def make_move(self, move) -> str:
        srow, scol = self._location_to_coordinate(move.start)
        erow, ecol = self._location_to_coordinate(move.end)
        piece, self.board[srow][scol] = self.board[srow][scol], 'blank' 
        self.board[erow][ecol] = piece
        self.locations.remove((srow, scol))
        self.locations.append((erow, ecol))
    
    def make_move_coord(self, srow, scol, erow, ecol):
        piece, self.board[srow][scol] = self.board[srow][scol], 'blank'
        self.board[erow][ecol] = piece
        self.locations.remove((srow, scol))
        self.locations.append((erow, ecol))
    
    def set_blank(self, row, col):
        self.board[row][col] = "blank"
        self.locations.remove((row, col))

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

    def remaining_pieces(self):
        pieces = ''
        for i, j in self.locations:
            pieces += self.board[i][j]
        return pieces

    def is_black(self, i, j):
        return self.board[i][j] != 'blank' and self.board[i][j].lower() == self.board[i][j]

    def is_white(self, i, j):
        return self.board[i][j] != 'blank' and self.board[i][j].upper() == self.board[i][j]

    def is_blank(self, i, j):
        return self.board[i][j] == 'blank'
    
    def is_king(self, i, j):
        return self.board[i][j].lower() == 'k'

    def is_queen(self, i, j):
        return self.board[i][j].lower() == 'q'

    def is_bishop(self, i, j):
        return self.board[i][j].lower() == 'b'

    def is_knight(self, i, j):
        return self.board[i][j].lower() == 'n'

    def is_rook(self, i, j):
        return self.board[i][j].lower() == 'r'

    def is_pawn(self, i, j):
        return self.board[i][j].lower() == 'p'