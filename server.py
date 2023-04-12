from flask_script import Manager

from chess_gui import app, socketio
manager = Manager(app)
@manager.command
def run():
    socketio.run(app,
                 host='127.0.0.1',
                 port=5000)


# Running app
if __name__ == '__main__':
    socketio.run(app,
                 host='127.0.0.1',
                 port=5000)