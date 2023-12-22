#! /usr/bin/python3

# run.py

import eventlet
eventlet.monkey_patch()  # Monkey patch for eventlet

from app import create_app, socketio

app = create_app()

if __name__ == '__main__':
    socketio.run(app, debug=True)
