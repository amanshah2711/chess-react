# Import flask and datetime module for showing date and time
from flask import render_template 
from flask_socketio import emit
from chess.controller import Controller
from chess.move import Move
from chess.guiplayer import GUIPlayer

from chess_gui import app, socketio
# Initializing flask app

user = GUIPlayer(color="w")
controller = Controller(white=user)
user.equip(controller)

@app.route('/', defaults={'path': ''})
def index(*args, **kwargs):
    return render_template('index.html')

@socketio.on('make_move')
def make_move(message):
    user.take_turn(Move(message))
    emit("update", controller.get_fen_position())
    emit("move_data", controller.moves)

@socketio.on('reset')
def reset():
    controller.reset()
    emit("update", controller.get_fen_position())
    emit("move_data", controller.moves)
    emit("possible", '')

@socketio.on('undo')
def undo():
    controller.undo()
    emit("update", controller.get_fen_position())
    emit("move_data", controller.moves)
    emit("possible", '')

@socketio.on('selected')
def selected(location):
    if location:
        i, j = controller.board._location_to_coordinate(location)
        moves = controller.possible_moves_from(i, j, False)
        emit('possible' ,' '.join([str(move) for move in moves]))
    else:
        emit('possible' , '')
