from flask import Flask
from flask_socketio import SocketIO, send, emit
from chess_gui import assets
import os

app = Flask(__name__, static_url_path='/chess_gui/static')
app.config['DEBUG'] = os.getenv("DEBUG", False)
app.jinja_env.globals.update({
  'assets_env': assets.assets_env,
})
cors_origins = os.getenv('CORS_ALLOWED_ORIGINS', '').split(',')
socketio = SocketIO(app, cors_origins=cors_origins)

import chess_gui.views





