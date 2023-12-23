#! /usr/bin/python3

from app import create_app, socketio
from eventlet import monkey_patch

monkey_patch()

app = create_app()

if __name__ == '__main__':
    socketio.run(app, debug=True)
