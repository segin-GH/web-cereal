#! /usr/bin/python3

from app import create_app, socketio
from eventlet import monkey_patch
from app.utils.logger_conf import setup_logger

# Setup logger
logger = setup_logger(__name__)
monkey_patch()

# Create Flask app
app = create_app()

if __name__ == '__main__':
    try:
        logger.info("Starting the Flask-SocketIO server")
        socketio.run(app)
        logger.info("Flask-SocketIO server stopped")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        socketio.stop()
