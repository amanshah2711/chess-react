from . import board
from . import move
def sign(x):
    if x == 0:
        return 0
    elif x > 0:
        return 1
    else:
        return -1
    
class Controller(object):

    start = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'

    def __init__(self, reporter=None) -> None:
        self.board = board.ChessBoard()
        self.reset()
        self.reporter = reporter

    def reset(self):
        self.board.reset()
        self.turn = "w"
        self.castling = 'KQkq'
        self.en_passant = '-'
        self.halfmove_clock = 0
        self.fullmove_clock = 1
        self.history = [Controller.start]
        self.moves = ''

    def switch(self):
        if self.turn == "w":
            self.turn = "b"
        else:
            self.turn = "w"

    def get_fen_position(self):
        fen_string = ''
        count = 0
        for row in self.board.board:
            for index, square in enumerate(row): # More elegant way?
                if square != 'blank':
                    if count:
                        fen_string += str(count)
                        count = 0
                    fen_string += square
                elif index == self.board.board_width - 1:
                    count += 1
                    fen_string += str(count)
                    count = 0
                else:
                    count += 1
            
            fen_string += '/'

        fen_string += ' ' + self.turn
        fen_string += ' ' + self.castling
        fen_string += ' ' + self.en_passant
        fen_string += ' ' + str(self.halfmove_clock)
        fen_string += ' ' + str(self.fullmove_clock)
        return fen_string

    def set_fen_position(self, fen_string):
        self.board.set_fen_position(fen_string)
        self.turn = fen_string.split(' ')[1]
        _, self.turn, self.castling, self.en_passant, self.halfmove_clock, self.fullmove_clock = fen_string.split(' ')
        self.fullmove_clock = int(self.fullmove_clock)
        self.halfmove_clock = int(self.halfmove_clock)
    
    def take_turn(self, move): #validate correct player operating etc
        change = self.simulate_move(move)
        if change:  
            illegal = self.king_in_check()
            if illegal:
                self.set_fen_position(self.history[-1])
            else:
                self.switch()
                if self.turn == 'w':
                    self.fullmove_clock += 1
                self.history.append(self.get_fen_position())
                if self.moves:
                    self.moves += ' ' + str(move) 
                else:
                    self.moves += str(move)
    
    def simulate_move(self, move):
        rank, file = self.board._location_to_coordinate(move.start)
        piece = self.board.board[rank][file]
        if self.validate_move(self.turn, move):
            castle_update = self.castle_update(move)
            en_passant_update = self.en_passant_update(move)
            if piece.lower() == 'k' and self.valid_king_castle(move):
                self.castle_move(move)
            elif piece.lower() == 'p' and self.valid_en_passant(move):
                self.en_passant_move(move)
            else:
                self.board.make_move(move)
            self.castling = castle_update if castle_update else '-'
            self.en_passant = en_passant_update
            return True
        return False

    def undo(self):
        if len(self.history) > 1:
            self.history.pop()
            self.set_fen_position(self.history[-1])
            self.moves = ' '.join(self.moves.split(' ')[:-1])

    def possible_castle(self, piece, destination):
        return (piece == 'k' and destination == 'r') or (piece == 'K' and destination == 'R')

    def castle_update(self, move):
        rank, file = self.board._location_to_coordinate(move.start)
        piece = self.board.board[rank][file]
        if piece == 'K':
            return self.castling.replace('K', '').replace('Q', '')
        elif piece == 'k':
            return self.castling.replace('k', '').replace('q', '')
        elif piece == 'R':
            if file == self.board.board_width - 1:
                return self.castling.replace('K', '')
            elif file == 0:
                return self.castling.replace('Q', '')
            else:
                return self.castling
        elif piece == 'r':
            if file == self.board.board_width - 1:
                return self.castling.replace('k', '')
            elif file == 0:
                return self.castling.replace('q', '')
            else:
                return self.castling
        else:
            return self.castling
    
    def castle_move(self, move):
        srow, scol = self.board._location_to_coordinate(move.start) 
        erow, ecol = self.board._location_to_coordinate(move.end)
        piece = self.board.board[srow][scol]
        if self.possible_castle(piece, self.board.board[erow][ecol]):
            if ecol == self.board.board_width - 1:
                self.board.make_move_coord(srow, scol, erow, self.board.board_width - 2)
                self.board.make_move_coord(erow, ecol, erow, self.board.board_width - 3)
            if ecol == 0:
                self.board.make_move_coord(srow, scol, erow, 2)
                self.board.make_move_coord(erow, ecol, erow, 3)
            
    def en_passant_update(self, move):
        srow, scol = self.board._location_to_coordinate(move.start)
        erow, ecol = self.board._location_to_coordinate(move.end)
        piece = self.board.board[srow][scol]
        vrow, vcol = erow - srow, scol - ecol
        if piece.lower() == 'p' and abs(vrow) == 2:
            return move.start[0] + str(self.board.board_height - (srow + sign(vrow)))
        else:
            return '-'
    
    def en_passant_move(self, move):
        self.board.make_move(move)
        if self.turn == 'w':
            rank, file = self.board._location_to_coordinate(move.end)
            self.board.board[rank+1][file] = 'blank'
        else:
            rank, file = self.board._location_to_coordinate(move.end)
            self.board.board[rank-1][file] = 'blank'

    def king_in_check(self):
        i, j = self.opposite_king()
        return self.under_attack(i, j)
    
    def check_safe(self, move):
        i, j = self.board._location_to_coordinate(move.start)
        row, col = self.board._location_to_coordinate(move.end)
        safe = True
        if (move.start == 'e1' and self.board.board[i][j] == 'K' and self.board.board[row][col] == 'R') or (move.start == 'e8' and self.board.board[i][j] == 'k' and self.board.board[row][col] == 'r'):
            safe = self.valid_king_castle(move)
        self.simulate_move(move)
        illegal = self.king_in_check()
        self.set_fen_position(self.history[-1])
        return not illegal and safe

    def opposite_king(self):
        if self.turn == 'w':
            i, j = self.board.white_king_coords()
        else:
            i, j = self.board.black_king_coords()
        return i, j
    
    def current_king(self):
        if self.turn == 'w':
            i, j = self.board.black_king_coords()
        else:
            i, j = self.board.white_king_coords()
        return i, j

    def under_attack(self, i, j):
        self.switch()
        moves = self.possible_moves(True)
        end = self.board._coordinate_to_location(i, j)
        self.switch()
        return end in [move.end for move in moves]

    def validate_move(self, player, move):
        rank, file = self.board._location_to_coordinate(move.start)
        erank, efile = self.board._location_to_coordinate(move.end)
        piece = self.board.board[rank][file]
        destination = self.board.board[erank][efile]
        if piece == 'blank':
            return False
        elif (self.board.is_white(piece) and player == 'b') or (self.board.is_black(piece) and player == 'w'):
            return False
        elif ((self.board.is_white(destination) and player == 'w') or (self.board.is_black(destination) and player == 'b')) and not self.possible_castle(piece, destination):
            return False 
        elif piece.lower() == 'k':
            return self.valid_king_move(move) or self.valid_king_castle(move)
        elif piece.lower() == 'q':
            return self.valid_queen_move(move)
        elif piece.lower() == 'b':
            return self.valid_bishop_move(move)
        elif piece.lower() == 'n':
            return self.valid_knight_move(move)
        elif piece.lower() == 'r':
            return self.valid_rook_move(move)
        elif piece == 'p':
            return self.valid_black_pawn_move(move)
        elif piece == 'P':
            return self.valid_white_pawn_move(move)

    def valid_king_move(self, move):
        srow, scol = self.board._location_to_coordinate(move.start)
        erow, ecol = self.board._location_to_coordinate(move.end)
        vrow, vcol = abs(srow - erow), abs(scol - ecol)
        return vrow < 2 and vcol < 2

    def valid_king_castle(self, move): 
        srow, scol = self.board._location_to_coordinate(move.start)
        erow, ecol = self.board._location_to_coordinate(move.end)
        piece = self.board.board[srow][scol]
        if self.possible_castle(piece, self.board.board[erow][ecol]):
            i, j = self.opposite_king()
            if ecol == self.board.board_width - 1:
                return piece in self.castling and not self.is_blocked(move) and not self.king_in_check() and not self.under_attack(i, j + 1)
            if ecol == 0:
                return ((self.board.is_black(piece) and 'q' in self.castling) or (self.board.is_white(piece) and 'Q' in self.castling)) and not self.is_blocked(move) and not self.king_in_check() and not self.under_attack(i, j - 1)
        return False


    def valid_queen_move(self, move):
        return self.valid_bishop_move(move) or self.valid_rook_move(move)
    
    def valid_bishop_move(self, move):
        srow, scol = self.board._location_to_coordinate(move.start)
        erow, ecol = self.board._location_to_coordinate(move.end)
        vrow, vcol = abs(srow - erow), abs(scol - ecol)
        return vrow == vcol and not self.is_blocked(move)
    
    def valid_knight_move(self, move):
        srow, scol = self.board._location_to_coordinate(move.start)
        erow, ecol = self.board._location_to_coordinate(move.end)
        vrow, vcol = abs(srow - erow), abs(scol - ecol)
        return (vrow == 1 and vcol == 2) or (vrow == 2 and vcol == 1)

    def valid_rook_move(self, move):
        srow, scol = self.board._location_to_coordinate(move.start)
        erow, ecol = self.board._location_to_coordinate(move.end)
        vrow, vcol = abs(srow - erow), abs(scol - ecol)
        return ((vrow != 0 and vcol == 0) or (vrow == 0 and vcol != 0)) and not self.is_blocked(move)

    def valid_white_pawn_move(self, move):
        srow, scol = self.board._location_to_coordinate(move.start)
        erow, ecol = self.board._location_to_coordinate(move.end)
        vrow, vcol = srow - erow, scol - ecol
        if (vcol == 0 and vrow == 1):
            return self.board.board[erow][ecol] == 'blank'
        elif (vcol == 0 and vrow == 2 and srow == 6):
            return self.board.board[erow][ecol] == 'blank'
        elif (abs(vcol) == 1 and vrow == 1):
            return self.board.is_black(self.board.board[erow][ecol]) or self.valid_en_passant(move)

    def valid_black_pawn_move(self, move):
        srow, scol = self.board._location_to_coordinate(move.start)
        erow, ecol = self.board._location_to_coordinate(move.end)
        vrow, vcol = erow - srow, scol - ecol
        if (vcol == 0 and vrow == 1):
            return self.board.board[erow][ecol] == 'blank'
        elif (vcol == 0 and vrow == 2 and srow == 1):
            return self.board.board[erow][ecol] == 'blank'
        elif (abs(vcol) == 1 and vrow == 1):
            return self.board.is_white(self.board.board[erow][ecol]) or self.valid_en_passant(move)
        
    def valid_en_passant(self, move):
        return move.end == self.en_passant
    
    def is_blocked(self, move):
        srow, scol = self.board._location_to_coordinate(move.start)
        erow, ecol = self.board._location_to_coordinate(move.end)
        vrow, vcol = erow - srow, ecol - scol
        drow, dcol = sign(vrow), sign(vcol)
        while srow != erow - drow or scol != ecol - dcol:
            srow += drow
            scol += dcol
            if self.board.board[srow][scol] != "blank":
                return True
        return False

    def possible_moves(self, pseudo=True):
        moves = []
        for i in range(self.board.board_height):
            for j in range(self.board.board_width):
                moves.extend(self.possible_moves_from(i, j, pseudo))
        return moves
    
    def possible_moves_from(self, i, j, pseudo=True):
        moves = []
        piece = self.board.board[i][j]
        if piece != 'blank' and  ((self.turn == 'w' and self.board.is_white(piece)) or (self.turn == 'b' and self.board.is_black(piece))):
            if piece.lower() == 'k':
                moves.extend(self.possible_king_moves(i, j, pseudo)) 
            if piece.lower() == 'q':
                moves.extend(self.possible_queen_moves(i, j, pseudo)) 
            if piece.lower() == 'b':
                moves.extend(self.possible_bishop_moves(i, j, pseudo)) 
            if piece.lower() == 'n':
                moves.extend(self.possible_knight_moves(i, j, pseudo)) 
            if piece.lower() == 'r':
                moves.extend(self.possible_rook_moves(i, j, pseudo)) 
            if piece.lower() == 'p':
                moves.extend(self.possible_pawn_moves(i, j, pseudo)) 
        return moves
    
    def same_side(self, side, piece):
        return ((side == 'w' and self.board.is_white(piece)) or (side == 'b' and self.board.is_black(piece)))

    def possible_king_moves(self, i, j, pseudo=True): #ignores castling but maybe okay for now because cant castle under checks
        moves = []
        piece = self.board.board[i][j]
        start = self.board._coordinate_to_location(i, j)
        for row_shift in [-1, 0, 1]:
            for col_shift in [-1, 0, 1]:
                erow, ecol = i + row_shift, j + col_shift
                if (row_shift != 0 or col_shift !=0) and self.board.in_board(erow, ecol) and not self.same_side(self.turn, self.board.board[erow][ecol]):
                    moves.append(move.Move(start + self.board._coordinate_to_location(erow, ecol)))

        if self.board.is_white(piece) and start == 'e1':
            king_castle = move.Move(start + 'h1')
            queen_castle = move.Move(start + 'a1')
            moves.append(king_castle)
            moves.append(queen_castle)
        elif self.board.is_black(piece):
            king_castle = move.Move(start + 'h8')
            queen_castle = move.Move(start + 'a8')
            moves.append(king_castle)
            moves.append(queen_castle)

        if pseudo:
            return moves
        else:
            return [option for option in moves if self.check_safe(option)]
    

    def possible_queen_moves(self, i, j, pseudo=True):
        temp = self.possible_bishop_moves(i, j, pseudo) + self.possible_rook_moves(i, j, pseudo)
        return temp

    def possible_bishop_moves(self, i, j, pseudo=True):
        moves = []
        start = self.board._coordinate_to_location(i, j)
        for step in range(0, 8):
            erow, ecol = i + step, j + step
            if self.board.in_board(erow, ecol) and (erow != i or ecol != j):
                if self.board.board[erow][ecol] == 'blank':
                    moves.append(move.Move(start + self.board._coordinate_to_location(erow, ecol)))
                elif not self.same_side(self.turn, self.board.board[erow][ecol]):
                    moves.append(move.Move(start + self.board._coordinate_to_location(erow, ecol)))
                    break
                else:
                    break
        for step in reversed(range(-7, 0)):
            erow, ecol = i + step, j + step
            if self.board.in_board(erow, ecol) and (erow != i or ecol != j):
                if self.board.board[erow][ecol] == 'blank':
                    moves.append(move.Move(start + self.board._coordinate_to_location(erow, ecol)))
                elif not self.same_side(self.turn, self.board.board[erow][ecol]):
                    moves.append(move.Move(start + self.board._coordinate_to_location(erow, ecol)))
                    break
                else:
                    break
        for step in range(0, 8):
            erow, ecol = i + step, j - step
            if self.board.in_board(erow, ecol) and (erow != i or ecol != j):
                if self.board.board[erow][ecol] == 'blank':
                    moves.append(move.Move(start + self.board._coordinate_to_location(erow, ecol)))
                elif not self.same_side(self.turn, self.board.board[erow][ecol]):
                    moves.append(move.Move(start + self.board._coordinate_to_location(erow, ecol)))
                    break
                else:
                    break
        for step in reversed(range(-7, 0)):
            erow, ecol = i + step, j - step
            if self.board.in_board(erow, ecol) and (erow != i or ecol != j):
                if self.board.board[erow][ecol] == 'blank':
                    moves.append(move.Move(start + self.board._coordinate_to_location(erow, ecol)))
                elif not self.same_side(self.turn, self.board.board[erow][ecol]):
                    moves.append(move.Move(start + self.board._coordinate_to_location(erow, ecol)))
                    break
                else:
                    break
        if pseudo:
            return moves
        else:
            return [option for option in moves if self.check_safe(option)]

    def possible_knight_moves(self, i, j, pseudo=True):
        moves = []
        start = self.board._coordinate_to_location(i, j)
        for row_shift in [2, -2]:
            for col_shift in [1, -1]:
                erow, ecol = i + row_shift, j + col_shift
                if self.board.in_board(erow, ecol) and not self.same_side(self.turn, self.board.board[erow][ecol]):
                    moves.append(move.Move(start + self.board._coordinate_to_location(erow, ecol)))
                erow, ecol = i + col_shift, j + row_shift 
                if self.board.in_board(erow, ecol) and not self.same_side(self.turn, self.board.board[erow][ecol]):
                    moves.append(move.Move(start + self.board._coordinate_to_location(erow, ecol)))
        if pseudo:
            return moves
        else:
            return [option for option in moves if self.check_safe(option)]

    def possible_rook_moves(self, i, j, pseudo=True):
        moves = []
        start = self.board._coordinate_to_location(i, j)
        
        for step in range(0, 8):
            erow = i + 1 * step
            if self.board.in_board(erow, j) and erow != i:
                if self.board.board[erow][j] == 'blank':
                    moves.append(move.Move(start + self.board._coordinate_to_location(erow, j)))
                elif not self.same_side(self.turn, self.board.board[erow][j]):
                    moves.append(move.Move(start + self.board._coordinate_to_location(erow, j)))
                    break
                else:
                    break
        for step in reversed(range(-7, 0)):
            erow = i + 1 * step
            if self.board.in_board(erow, j) and erow != i:
                if self.board.board[erow][j] == 'blank':
                    moves.append(move.Move(start + self.board._coordinate_to_location(erow, j)))
                elif not self.same_side(self.turn, self.board.board[erow][j]):
                    moves.append(move.Move(start + self.board._coordinate_to_location(erow, j)))
                    break
                else:
                    break
        for step in range(0, 8):
            ecol = j + 1 * step
            if self.board.in_board(i, ecol) and ecol != j:
                if self.board.board[i][ecol] == 'blank':
                    moves.append(move.Move(start + self.board._coordinate_to_location(i, ecol)))
                elif not self.same_side(self.turn, self.board.board[i][ecol]):
                    moves.append(move.Move(start + self.board._coordinate_to_location(i, ecol)))
                    break
                else:
                    break
        for step in reversed(range(-7, 0)):
            ecol = j + 1 * step
            if self.board.in_board(i, ecol) and ecol != j:
                if self.board.board[i][ecol] == 'blank':
                    moves.append(move.Move(start + self.board._coordinate_to_location(i, ecol)))
                elif not self.same_side(self.turn, self.board.board[i][ecol]):
                    moves.append(move.Move(start + self.board._coordinate_to_location(i, ecol)))
                    break
                else:
                    break
        if pseudo:
            return moves
        else:
            return [option for option in moves if self.check_safe(option)]
    
    def possible_pawn_moves(self, i, j, pseudo=True): #doesn't en passants promotion
        moves = []
        start = self.board._coordinate_to_location(i, j)
        if self.board.is_white(self.board.board[i][j]):
            if self.board.in_board(i - 1, j) and self.board.board[i - 1][j] == 'blank':
                moves.append(move.Move(start + self.board._coordinate_to_location(i - 1, j)))
            if self.board.in_board(i - 2, j) and self.board.board[i - 2][j] == 'blank' and i == 6:
                moves.append(move.Move(start + self.board._coordinate_to_location(i - 2, j)))
            if self.board.in_board(i - 1, j + 1) and ((self.board.board[i - 1][j + 1] != 'blank' and not self.same_side(self.turn, self.board.board[i - 1][j + 1])) or self.en_passant == self.board._coordinate_to_location(i - 1, j + 1)):
                moves.append(move.Move(start + self.board._coordinate_to_location(i - 1, j + 1)))
            if self.board.in_board(i - 1, j - 1) and ((self.board.board[i - 1][j - 1] != 'blank' and not self.same_side(self.turn, self.board.board[i - 1][j - 1])) or self.en_passant == self.board._coordinate_to_location(i - 1, j - 1)):
                moves.append(move.Move(start + self.board._coordinate_to_location(i - 1, j - 1)))
        elif self.board.is_black(self.board.board[i][j]):
            if self.board.in_board(i + 1, j) and self.board.board[i + 1][j] == 'blank':
                moves.append(move.Move(start + self.board._coordinate_to_location(i + 1, j)))
            if self.board.in_board(i + 2, j) and self.board.board[i + 2][j] == 'blank' and i == 1:
                moves.append(move.Move(start + self.board._coordinate_to_location(i + 2, j)))
            if self.board.in_board(i + 1, j + 1) and self.board.board[i + 1][j + 1] != 'blank' and not self.same_side(self.turn, self.board.board[i + 1][j + 1]):
                moves.append(move.Move(start + self.board._coordinate_to_location(i + 1, j + 1)))
            if self.board.in_board(i + 1, j - 1) and self.board.board[i + 1][j - 1] != 'blank' and not self.same_side(self.turn, self.board.board[i + 1][j - 1]):
                moves.append(move.Move(start + self.board._coordinate_to_location(i + 1, j - 1)))
        if pseudo:
            return moves
        else:
            return [option for option in moves if self.check_safe(option)]
    
    def game_over(self):
        if len(self.possible(moves, pseudo)):
            pass


    
        




        