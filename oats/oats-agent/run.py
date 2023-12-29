#! /usr/bin/python3

from app import create_app, socketio
from eventlet import monkey_patch
from app.utils.logger_conf import setup_logger

# Setup logger
logger = setup_logger(__name__)
monkey_patch()

# Create Flask app
app, port = create_app()

if __name__ == '__main__':
    try:
        logger.info("Starting the Flask server")
        # fancy box to display the URL
        url = f" app @:  http://localhost:{port}"
        box_width = len(url) + 6
        top_bottom_border = "+" + "-" * (box_width - 2) + "+"
        spacer = "|" + " " * (box_width - 2) + "|"
        url_line = "|  " + url + "  |"

        fancy_box = (
            f"\n\t{top_bottom_border}\n\t{spacer}\n"
            f"\t{url_line}\n\t{spacer}\n\t{top_bottom_border}"
        )
        logger.info(fancy_box)

        logger.info("Starting the Flask-SocketIO server")
        socketio.run(app, port=port)
        logger.info("Flask-SocketIO server stopped")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        socketio.stop()
