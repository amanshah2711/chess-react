
from chess.controller import Controller
from chess.move import Move

controller = Controller()

def possible_states(controller, depth=0, verbose=False):
    if depth == 0:
        return 1
    else:
        total = 0
        possible_moves = controller.legal_moves()
        for move in possible_moves:
            controller.take_turn(move, bypass=True)
            value = possible_states(controller, depth - 1)
            total += value
            if verbose:
                print(move, value)
            controller.undo()
        return total
    
def state1(controller, i, verbose=False): #correct up to depth 3, incorrect at 4 
    print(possible_states(controller=controller, depth=i, verbose=verbose))

def state2(controller, i, verbose=False): #correct up to depth 1, incorrect after reason unknown 2041
    controller.set_fen_position("r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1")
    print(possible_states(controller=controller, depth=i, verbose=verbose))

def state3(controller, i, verbose=False): #correct up to depth 6, unsure after 
    controller.set_fen_position("8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - - 0 1")
    print(possible_states(controller=controller, depth=i, verbose=verbose))

def state4(controller, i, verbose=False): #correct up to depth 2, incorrect at 3 reason unknown 9443
    controller.set_fen_position("r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2Q1RK1 w kq - 0 1")
    print(possible_states(controller=controller, depth=i, verbose=verbose))

def state5(controller, i, verbose=False): #correct at depth 3, unsure after
    controller.set_fen_position("rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ - 1 8")
    print(possible_states(controller=controller, depth=i, verbose=verbose))


state1(controller, 1) # PASSED 
state1(controller, 2) # PASSED 
state1(controller, 3) # PASSED
state1(controller, 4) # PASSED
state1(controller, 5) # PASSED
print() # PASSED

state2(controller, 1) # PASSED
state2(controller, 2) # PASSED
state2(controller, 3) # PASSED
state2(controller, 4) # PASSED
state2(controller, 5) # PASSED
print() # PASSED

state3(controller, 1) # PASSED
state3(controller, 2) # PASSED
state3(controller, 3) # PASSED
state3(controller, 4) # PASSED
state3(controller, 5) # PASSED
print() # PASSED

state4(controller, 1) # PASSED
state4(controller, 2) # PASSED
state4(controller, 3) # PASSED
state4(controller, 4) # PASSED
state4(controller, 5) # PASSED
print() # PASSED

state5(controller, 1) # PASSED
state5(controller, 2) # PASSED
state5(controller, 3) # PASSED
state5(controller, 4) # PASSED
state5(controller, 5) # PASSED 