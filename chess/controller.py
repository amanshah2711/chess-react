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

    def undo(self):
        if len(self.history) > 1:
            self.history.pop()
            self.set_fen_position(self.history[-1])
            self.moves = ' '.join(self.moves.split(' ')[:-1])

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

    def game_over(self):
        return self.legal_moves() == []

    def switch(self):
        if self.turn == "w":
            self.turn = "b"
        else:
            self.turn = "w"

    def legal_moves(self):
        moves = []
        for i, j in self.board.get_locations():
            moves.extend(self.legal_moves_from(i, j))
        return moves

    def legal_moves_from(self, i, j):
        moves = [move for move in self.pseudo_moves_from(i, j) if self.check_safe(move)]
        if self.board.is_king(i, j):
            return self.legal_castle(i, j) + moves
        else:
            return moves

    def pseudo_moves(self):
        moves = []
        for i, j in self.board.get_locations():
            moves.extend(self.pseudo_moves_from(i, j))
        return moves
    
    def pseudo_moves_from(self, i, j):
        moves = []
        if not self.board.is_blank(i, j) and ((self.turn == 'w' and self.board.is_white(i, j)) or (self.turn == 'b' and self.board.is_black(i, j))):
            if self.board.is_king(i, j):
                moves.extend(self.pseudo_king_moves(i, j)) 
            if self.board.is_queen(i, j):
                moves.extend(self.pseudo_queen_moves(i, j)) 
            if self.board.is_bishop(i,j):
                moves.extend(self.pseudo_bishop_moves(i, j)) 
            if self.board.is_knight(i, j):
                moves.extend(self.pseudo_knight_moves(i, j)) 
            if self.board.is_rook(i, j):
                moves.extend(self.pseudo_rook_moves(i, j)) 
            if self.board.is_pawn(i, j):
                moves.extend(self.pseudo_pawn_moves(i, j)) 
                moves.extend(self.pseudo_en_passant(i, j))
        return moves

    def take_turn(self, move):
        if move in self.legal_moves():
            self.chess_move(move)
            self.switch()
            self.halfmove_clock += 1
            if self.turn == 'w':
                self.fullmove_clock += 1
            self.history.append(self.get_fen_position())
            if self.moves:
                self.moves += ' ' + str(move) 
            else:
                self.moves += str(move)
            return True
        return False

    def chess_move(self, move):
        rank, file = self.board._location_to_coordinate(move.start)
        castle_update = self.castle_update(move)
        en_passant_update = self.en_passant_update(move)
        if self.board.is_king(rank, file) and self.valid_castle(move):
            self.castle_move(move)
        elif self.board.is_pawn(rank, file) and self.valid_en_passant(move):
            self.en_passant_move(move)
        else:
            self.board.make_move(move)
        self.castling = castle_update if castle_update else '-'
        self.en_passant = en_passant_update

    def castle_update(self, move):
        rank, file = self.board._location_to_coordinate(move.start)
        if self.board.is_king(rank, file) and self.board.is_white(rank, file):
            return self.castling.replace('K', '').replace('Q', '')
        elif self.board.is_king(rank, file) and self.board.is_black(rank, file):
            return self.castling.replace('k', '').replace('q', '')
        elif self.board.is_rook(rank, file) and self.board.is_white(rank, file):
            if file == self.board.board_width - 1:
                return self.castling.replace('K', '')
            elif file == 0:
                return self.castling.replace('Q', '')
            else:
                return self.castling
        elif self.board.is_rook(rank, file) and self.board.is_black(rank, file):
            if file == self.board.board_width - 1:
                return self.castling.replace('k', '')
            elif file == 0:
                return self.castling.replace('q', '')
            else:
                return self.castling
        else:
            return self.castling

    def en_passant_update(self, move):
        srow, scol = self.board._location_to_coordinate(move.start)
        erow, ecol = self.board._location_to_coordinate(move.end)
        vrow, vcol = erow - srow, scol - ecol
        if self.board.is_pawn(srow, scol) and abs(vrow) == 2:
            return move.start[0] + str(self.board.board_height - (srow + sign(vrow)))
        else:
            return '-'

    def castle_move(self, move):
        srow, scol = self.board._location_to_coordinate(move.start) 
        erow, ecol = self.board._location_to_coordinate(move.end)
        if ecol == self.board.board_width - 1:
            self.board.make_move_coord(srow, scol, erow, self.board.board_width - 2)
            self.board.make_move_coord(erow, ecol, erow, self.board.board_width - 3)
        if ecol == 0:
            self.board.make_move_coord(srow, scol, erow, 2)
            self.board.make_move_coord(erow, ecol, erow, 3)
            
    def en_passant_move(self, move):
        self.board.make_move(move)
        if self.turn == 'w':
            rank, file = self.board._location_to_coordinate(move.end)
            self.board.set_blank(rank + 1, file)
        else:
            rank, file = self.board._location_to_coordinate(move.end)
            self.board.set_blank(rank - 1, file)
            
    def check_safe(self, move):
        self.chess_move(move)
        illegal = self.king_in_check()
        self.set_fen_position(self.history[-1])
        return not illegal 

    def king_in_check(self):
        if self.turn == 'w':
            i, j = self.board.white_king_coords()
        else:
            i, j = self.board.black_king_coords()
        return self.under_attack(i, j)

    def under_attack(self, i, j):
        self.switch()
        moves = self.pseudo_moves()
        end = self.board._coordinate_to_location(i, j)
        self.switch()
        return end in [move.end for move in moves]

    def is_blocked(self, move):
        srow, scol = self.board._location_to_coordinate(move.start)
        erow, ecol = self.board._location_to_coordinate(move.end)
        vrow, vcol = erow - srow, ecol - scol
        drow, dcol = sign(vrow), sign(vcol)
        while srow != erow - drow or scol != ecol - dcol:
            srow += drow
            scol += dcol
            if not self.board.is_blank(srow, scol):
                return True
        return False
    
    def same_side(self, side, i, j):
        return ((side == 'w' and self.board.is_white(i, j)) or (side == 'b' and self.board.is_black(i, j)))

    def pseudo_king_moves(self, i, j): # only propose castles when possible
        moves = []
        start = self.board._coordinate_to_location(i, j)
        for row_shift in [-1, 0, 1]:
            for col_shift in [-1, 0, 1]:
                erow, ecol = i + row_shift, j + col_shift
                if (row_shift != 0 or col_shift !=0) and self.board.in_board(erow, ecol) and not self.same_side(self.turn, erow, ecol):
                    moves.append(move.Move(start + self.board._coordinate_to_location(erow, ecol)))
        return moves
    
    def legal_castle(self, i, j): 
        moves = []
        start = self.board._coordinate_to_location(i, j)
        if self.board.is_white(i, j):
            king_castle = move.Move(start + 'h1')
            queen_castle = move.Move(start + 'a1')
            mark1, mark2 = 'K', 'Q'
        elif self.board.is_black(i, j): 
            king_castle = move.Move(start + 'h8')
            queen_castle = move.Move(start + 'a8')
            mark1, mark2 = 'k', 'q'
        if not self.king_in_check():
            if mark1 in self.castling and not self.under_attack(i, j + 1) and not self.under_attack(i, j + 2) and not self.is_blocked(king_castle):
                moves.append(king_castle)
            if mark2 in self.castling and not self.under_attack(i, j - 1) and not self.under_attack(i, j - 2) and not self.is_blocked(queen_castle):
                moves.append(queen_castle)
        return moves

    def pseudo_queen_moves(self, i, j):
        return self.pseudo_bishop_moves(i, j) + self.pseudo_rook_moves(i, j)

    def pseudo_bishop_moves(self, i, j):
        moves = []
        start = self.board._coordinate_to_location(i, j)
        for step in range(0, 8):
            erow, ecol = i + step, j + step
            if self.board.in_board(erow, ecol) and (erow != i or ecol != j):
                if self.board.is_blank(erow, ecol):
                    moves.append(move.Move(start + self.board._coordinate_to_location(erow, ecol)))
                elif not self.same_side(self.turn, erow, ecol):
                    moves.append(move.Move(start + self.board._coordinate_to_location(erow, ecol)))
                    break
                else:
                    break
        for step in reversed(range(-7, 0)):
            erow, ecol = i + step, j + step
            if self.board.in_board(erow, ecol) and (erow != i or ecol != j):
                if self.board.is_blank(erow, ecol):
                    moves.append(move.Move(start + self.board._coordinate_to_location(erow, ecol)))
                elif not self.same_side(self.turn, erow, ecol):
                    moves.append(move.Move(start + self.board._coordinate_to_location(erow, ecol)))
                    break
                else:
                    break
        for step in range(0, 8):
            erow, ecol = i + step, j - step
            if self.board.in_board(erow, ecol) and (erow != i or ecol != j):
                if self.board.is_blank(erow, ecol):
                    moves.append(move.Move(start + self.board._coordinate_to_location(erow, ecol)))
                elif not self.same_side(self.turn, erow, ecol):
                    moves.append(move.Move(start + self.board._coordinate_to_location(erow, ecol)))
                    break
                else:
                    break
        for step in reversed(range(-7, 0)):
            erow, ecol = i + step, j - step
            if self.board.in_board(erow, ecol) and (erow != i or ecol != j):
                if self.board.is_blank(erow, ecol):
                    moves.append(move.Move(start + self.board._coordinate_to_location(erow, ecol)))
                elif not self.same_side(self.turn, erow, ecol):
                    moves.append(move.Move(start + self.board._coordinate_to_location(erow, ecol)))
                    break
                else:
                    break
        return moves

    def pseudo_knight_moves(self, i, j):
        moves = []
        start = self.board._coordinate_to_location(i, j)
        for row_shift in [2, -2]:
            for col_shift in [1, -1]:
                erow, ecol = i + row_shift, j + col_shift
                if self.board.in_board(erow, ecol) and not self.same_side(self.turn, erow, ecol):
                    moves.append(move.Move(start + self.board._coordinate_to_location(erow, ecol)))
                erow, ecol = i + col_shift, j + row_shift 
                if self.board.in_board(erow, ecol) and not self.same_side(self.turn, erow, ecol):
                    moves.append(move.Move(start + self.board._coordinate_to_location(erow, ecol)))
        return moves

    def pseudo_rook_moves(self, i, j):
        moves = []
        start = self.board._coordinate_to_location(i, j)
        for step in range(0, 8):
            erow = i + 1 * step
            if self.board.in_board(erow, j) and erow != i:
                if self.board.is_blank(erow, j):
                    moves.append(move.Move(start + self.board._coordinate_to_location(erow, j)))
                elif not self.same_side(self.turn, erow, j):
                    moves.append(move.Move(start + self.board._coordinate_to_location(erow, j)))
                    break
                else:
                    break
        for step in reversed(range(-7, 0)):
            erow = i + 1 * step
            if self.board.in_board(erow, j) and erow != i:
                if self.board.is_blank(erow, j):
                    moves.append(move.Move(start + self.board._coordinate_to_location(erow, j)))
                elif not self.same_side(self.turn, erow, j):
                    moves.append(move.Move(start + self.board._coordinate_to_location(erow, j)))
                    break
                else:
                    break
        for step in range(0, 8):
            ecol = j + 1 * step
            if self.board.in_board(i, ecol) and ecol != j:
                if self.board.is_blank(i, ecol):
                    moves.append(move.Move(start + self.board._coordinate_to_location(i, ecol)))
                elif not self.same_side(self.turn, i, ecol):
                    moves.append(move.Move(start + self.board._coordinate_to_location(i, ecol)))
                    break
                else:
                    break
        for step in reversed(range(-7, 0)):
            ecol = j + 1 * step
            if self.board.in_board(i, ecol) and ecol != j:
                if self.board.is_blank(i, ecol):
                    moves.append(move.Move(start + self.board._coordinate_to_location(i, ecol)))
                elif not self.same_side(self.turn, i, ecol):
                    moves.append(move.Move(start + self.board._coordinate_to_location(i, ecol)))
                    break
                else:
                    break
        return moves
    
    def pseudo_pawn_moves(self, i, j): 
        moves = []
        start = self.board._coordinate_to_location(i, j)
        if self.board.is_white(i, j):
            if self.board.in_board(i - 1, j) and self.board.is_blank(i - 1, j): # move forward
                moves.append(move.Move(start + self.board._coordinate_to_location(i - 1, j)))
            if self.board.in_board(i - 2, j) and self.board.is_blank(i - 2, j) and self.board.is_blank(i - 1, j) and i == 6: # move forward 2 from starting rank
                moves.append(move.Move(start + self.board._coordinate_to_location(i - 2, j)))
            if self.board.in_board(i - 1, j + 1) and not self.board.is_blank(i - 1, j + 1) and not self.same_side(self.turn, i - 1, j + 1):
                moves.append(move.Move(start + self.board._coordinate_to_location(i - 1, j + 1)))
            if self.board.in_board(i - 1, j - 1) and not self.board.is_blank(i - 1, j - 1) and not self.same_side(self.turn, i - 1, j - 1):
                moves.append(move.Move(start + self.board._coordinate_to_location(i - 1, j - 1)))
        elif self.board.is_black(i, j):
            if self.board.in_board(i + 1, j) and self.board.is_blank(i + 1, j):
                moves.append(move.Move(start + self.board._coordinate_to_location(i + 1, j)))
            if self.board.in_board(i + 2, j) and self.board.is_blank(i + 2, j) and self.board.is_blank(i + 1, j) and i == 1:
                moves.append(move.Move(start + self.board._coordinate_to_location(i + 2, j)))
            if self.board.in_board(i + 1, j + 1) and not self.board.is_blank(i + 1, j + 1) and not self.same_side(self.turn, i + 1, j + 1):
                moves.append(move.Move(start + self.board._coordinate_to_location(i + 1, j + 1)))
            if self.board.in_board(i + 1, j - 1) and not self.board.is_blank(i + 1, j - 1) and not self.same_side(self.turn, i + 1, j - 1):
                moves.append(move.Move(start + self.board._coordinate_to_location(i + 1, j - 1)))
        return moves

    def pseudo_en_passant(self, i, j):
        moves = []
        start = self.board._coordinate_to_location(i, j)
        if self.board.is_white(i, j):
            if self.en_passant == self.board._coordinate_to_location(i - 1, j + 1):
                moves.append(move.Move(start + self.board._coordinate_to_location(i - 1, j + 1)))
            if self.en_passant == self.board._coordinate_to_location(i - 1, j - 1):
                moves.append(move.Move(start + self.board._coordinate_to_location(i - 1, j - 1)))
        elif self.board.is_black(i, j):
            if self.en_passant == self.board._coordinate_to_location(i + 1, j + 1):
                moves.append(move.Move(start + self.board._coordinate_to_location(i + 1, j + 1)))
            if self.en_passant == self.board._coordinate_to_location(i + 1, j - 1):
                moves.append(move.Move(start + self.board._coordinate_to_location(i + 1, j - 1)))
        return moves

    def valid_en_passant(self, move):
        i, j = self.board._location_to_coordinate(move.start)
        return move in self.pseudo_en_passant(i, j)

    def valid_castle(self, move):
        i, j = self.board._location_to_coordinate(move.start)
        return move in self.legal_castle(i, j)