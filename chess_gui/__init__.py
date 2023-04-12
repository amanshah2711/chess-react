from flask import Flask
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO, send, emit
from chess_gui import assets
app = Flask(__name__, static_url_path='/chess_gui/static')
app.config['SECRET_KEY'] = 'secret!'
app.config['CORS_HEADERS'] = 'Content-Type'
app.debug=True
app.jinja_env.globals.update({
  'assets_env': assets.assets_env,
})

CORS(app)
socketio = SocketIO(app, cors_allowed_origins='*')

import chess_gui.views





