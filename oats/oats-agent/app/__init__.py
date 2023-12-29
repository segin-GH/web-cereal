from app.utils.logger_conf import setup_logger
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO

socketio = SocketIO()
logger = setup_logger(__name__)


def create_app():
    app = Flask(__name__)

    logger.info("Starting Flask app")

    CORS(app, cors_allowed_origins="*")
    socketio.init_app(app, async_mode='eventlet', cors_allowed_origins="*")

    register_blueprints(app)

    standard_port = 5678

    # fancy box to display the URL
    url = f" app @:  http://localhost:{standard_port}"
    box_width = len(url) + 6
    top_bottom_border = "+" + "-" * (box_width - 2) + "+"
    spacer = "|" + " " * (box_width - 2) + "|"
    url_line = "|  " + url + "  |"

    fancy_box = (
        f"\n\t{top_bottom_border}\n\t{spacer}\n"
        f"\t{url_line}\n\t{spacer}\n\t{top_bottom_border}"
    )
    logger.info(fancy_box)

    return app, standard_port


def register_blueprints(app):
    from .routes.route_usb import bp as usb_bp
    app.register_blueprint(usb_bp)

    logger.info("Blueprints registered successfully")
