from flask import Flask
from flask_socketio import SocketIO, send, emit
from chess_gui import assets
import os

app = Flask(__name__, static_url_path='/chess_gui/static')
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "secret!")
app.config['DEBUG'] = os.getenv("DEBUG", False)
app.jinja_env.globals.update({
  'assets_env': assets.assets_env,
})

socketio = SocketIO(app, cors_allowed_origins="http://chess.amanshah2711.me")

import chess_gui.views





