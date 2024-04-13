# Import flask and datetime module for showing date and time
from flask import render_template, request, Response
from flask_socketio import emit
from chess.controller import Controller
from chess.move import Move
from chess.guiplayer import GUIPlayer
from chess.min_max_player import MinMaxPlayer
from chess.random_player import RandomPlayer

from chess_gui import app, socketio
# Initializing flask app

user = GUIPlayer(color="w")
controller = Controller()
user.equip(controller)
opponent = None
undo_style = None
opp_type = {
    'Random' : RandomPlayer,
    'Minimax' : MinMaxPlayer,
    'User' : GUIPlayer
}
undo_type = {
    'Random' : lambda : controller.undo() or controller.undo(),
    'Minimax' : lambda : controller.undo() or controller.undo(),
    'User' : lambda : controller.undo()
}
AI = False


@app.route('/', defaults={'path': ''})
def index(*args, **kwargs):
    return render_template('index.html')

@app.route('/options')
def options():
    global opponent, undo_style, AI
    if 'opponent' in request.args:
        opponent = opp_type[request.args['opponent']](color="b")
        opponent.equip(controller)
        undo_style = undo_type[request.args['opponent']]
        AI = request.args['opponent'] != 'User'
    return Response(), 204

@socketio.on('make_move')
def make_move(message):
    move = Move(message)
    if user.take_turn(move):
        if AI:
            if controller.game_over():
                emit("game_over", controller.turn)
            else:
                opponent.take_turn()
    emit("update", controller.get_fen_position())
    emit("move_data", controller.moves)
    if controller.game_over():
      emit("game_over", controller.turn)

@socketio.on('collect_data')
def collect():
    emit("update", controller.get_fen_position())
    emit("move_data", controller.moves)
    if not opponent:
        emit("show_options")

@socketio.on('reset')
def reset():
    global opponent
    controller.reset()
    opponent = None
    emit("show_options")
    emit("update", controller.get_fen_position())
    emit("move_data", controller.moves)
    emit("possible", '')

@socketio.on('undo')
def undo():
    undo_style()
    emit("update", controller.get_fen_position())
    emit("move_data", controller.moves)
    emit("possible", '')

@socketio.on('selected')
def selected(location):
    if location:
        i, j = controller.board._location_to_coordinate(location) # Make sure types clean up properly
        moves = controller.legal_moves_from(i, j)
        emit('possible' ,' '.join([str(move) for move in moves]))
    else:
        emit('possible' , '')
