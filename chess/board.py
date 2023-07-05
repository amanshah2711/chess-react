
class ChessBoard(object):
    
    start = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
    board_width = 8
    board_height = 8
   
    def __init__(self) -> None:
        self.reset()

    def reset(self):
        self.board = ''
        self.board_history = [] # saving board history makes resetting states while trying moves fast
        self.locations = set() # set data structure to maintain current locations
        self.location_history = [[[], []], [[], []]] # should ideally be information needed to undo moves to make resetting fast
        self.white_king = ()
        self.black_king = ()
        self.set_fen_position(ChessBoard.start)

    def undo(self):
        self.board = self.board_history.pop() # properly resets board
        locs_to_add, locs_to_remove = self.location_history.pop()
        for i, j in locs_to_remove:
            self.locations.remove((i, j))

        for i, j in locs_to_add:
            self.locations.add((i, j))
            if self.is_king(i, j):
                if self.is_white(i, j):
                    self.white_king = (i, j)
                else:
                    self.black_king = (i, j)
    
    def save(self):
        self.board_history.append(self.board)
        self.location_history.append([[], []])

    def get_fen_position(self):
        fen_string = ''
        count = 0
        for index, piece in enumerate(self.board):
            rank, file = index // 8, index % 8
            if piece != 'e':
                if count:
                    fen_string += str(count)
                    count = 0
                fen_string += piece
            elif file == self.board_width - 1:
                count += 1
                fen_string += str(count)
                count = 0
            else:
                count += 1
            if file == self.board_width - 1:
                fen_string += '/'
        return fen_string[:-1]
            

    def set_fen_position(self, fen_string) -> None:
        self.board = ''
        for string_row in fen_string.split(' ')[0].split('/'):
            for character in string_row:
                if character.isalpha():
                    self.board += character
                elif character.isdigit():
                    self.board += 'e' * int(character) 
                else:
                    raise Exception("FEN String " + fen_string + " has given the following invalid character, " + character)

        for i in range(self.board_height):
            for j in range(self.board_width):
                if not self.is_blank(i, j):
                    self.locations.add((i, j))
                if self.is_king(i, j):
                    if self.is_white(i, j):
                        self.white_king = (i, j)
                    else:
                        self.black_king = (i, j)
        

    def get(self, row, col):
        piece = self.board[row * self.board_width + col]
        if piece == 'e':
            return 'blank'
        else:
            return piece

    def set(self, row, col, piece):
        if piece == 'blank':
            self.board = self.board[:row * self.board_width + col] + 'e' + self.board[row * self.board_width + col + 1:]
        else:
            self.board = self.board[:row * self.board_width + col] + piece + self.board[row * self.board_width + col + 1:]

    def get_locations(self):
        return self.locations.copy()

    def make_move(self, move) -> str:
        srow, scol = self._location_to_coordinate(move.start)
        erow, ecol = self._location_to_coordinate(move.end)
        self.make_move_coord(srow, scol, erow, ecol)
    
    def make_move_coord(self, srow, scol, erow, ecol):
        piece = self.get(srow, scol)
        if self.is_blank(erow, ecol):
            self.location_history[-1][1].append((erow, ecol))
        if self.is_king(srow, scol):
            if self.is_white(srow, scol):
                self.white_king = (erow, ecol)
            else:
                self.black_king = (erow, ecol)

        self.locations.add((erow, ecol))

    
        self.set_blank(srow, scol)
        self.set(erow, ecol, piece)


    def set_blank(self, row, col): #assumes row col isnt empty
        self.set(row, col, 'blank')
        self.locations.remove((row, col))
        self.location_history[-1][0].append((row, col))
    
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
        return self.white_king
        #for i in range(self.board_height):
            #for j in range(self.board_width):
                #if self.get(i, j) == 'K':
                    #return i, j

    def black_king_coords(self):
        return self.black_king
        #for i in range(self.board_height):
            #for j in range(self.board_width):
                #if self.get(i, j) == 'k':
                    #return i, j

    def remaining_pieces(self):
        pieces = ''
        for i, j in self.locations:
            pieces += self.get(i, j)
        return pieces

    def is_black(self, i, j):
        return self.get(i, j) != 'blank' and self.get(i, j).lower() == self.get(i, j)

    def is_white(self, i, j):
        return self.get(i, j) != 'blank' and self.get(i, j).upper() == self.get(i, j)

    def is_blank(self, i, j):
        return self.get(i, j) == 'blank'
    
    def is_king(self, i, j):
        return self.get(i, j).lower() == 'k'

    def is_queen(self, i, j):
        return self.get(i, j).lower() == 'q'

    def is_bishop(self, i, j):
        return self.get(i, j).lower() == 'b'

    def is_knight(self, i, j):
        return self.get(i, j).lower() == 'n'

    def is_rook(self, i, j):
        return self.get(i, j).lower() == 'r'

    def is_pawn(self, i, j):
        return self.get(i, j).lower() == 'p'