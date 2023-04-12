# Import flask and datetime module for showing date and time
from flask import abort, render_template, request, url_for, copy_current_request_context, jsonify, send_from_directory
from flask_socketio import send, emit
from chess.controller import Controller
from chess.move import Move
from chess.guiplayer import GUIPlayer

from chess_gui import app, socketio, cross_origin
# Initializing flask app

app.config.from_pyfile('settings.py')
user = GUIPlayer(color="w")
controller = Controller(white=user)
user.equip(controller)

@app.route('/', defaults={'path': ''})
def index(*args, **kwargs):
    return render_template('index.html')

@socketio.on('make_move')
@cross_origin()
def make_move(message):
    user.take_turn(Move(message))
    emit("update", controller.get_fen_position())
    emit("move_data", controller.moves)
    return 'a'

@socketio.on('reset')
def reset():
    controller.reset()
    emit("update", controller.get_fen_position())
    emit("move_data", controller.moves)
    emit("possible", '')
    return 'a'

@socketio.on('undo')
def undo():
    controller.undo()
    emit("update", controller.get_fen_position())
    emit("move_data", controller.moves)
    emit("possible", '')
    return 'a'

@socketio.on('selected')
def selected(location):
    if location:
        i, j = controller.board._location_to_coordinate(location)
        moves = controller.possible_moves_from(i, j, False)
        print('KAHUNA', moves)
        emit('possible' ,' '.join([str(move) for move in moves]))
    else:
        emit('possible' , '')
    return 'a'
