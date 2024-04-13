from flask import Flask
from flask_socketio import SocketIO, send, emit
from chess_gui import assets
app = Flask(__name__, static_url_path='/chess_gui/static')
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True 
app.jinja_env.globals.update({
  'assets_env': assets.assets_env,
})

socketio = SocketIO(app)

import chess_gui.views





