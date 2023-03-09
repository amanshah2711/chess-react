# Import flask and datetime module for showing date and time
from flask import Flask
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO, send, emit
from flask import abort, render_template, request, url_for, copy_current_request_context, jsonify, send_from_directory

from chess.controller import Controller
from chess.move import Move
from chess.guiplayer import GUIPlayer

import datetime
  
  


# Initializing flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)
socketio = SocketIO(app, cors_allowed_origins='*')

user = GUIPlayer(color="w")
controller = Controller(white=user)
user.equip(controller)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
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

@socketio.on("selected")
def selected(location):
    if location:
        i, j = controller.board._location_to_coordinate(location)
        moves = controller.possible_moves_from(i, j, False)
        emit('possible' ,' '.join([str(move) for move in moves]))
    else:
        emit('possible' , '')
    return 'a'


# Running app
if __name__ == '__main__':
    socketio.run(app, debug=True)
