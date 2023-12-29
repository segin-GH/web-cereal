from app.utils.logger_conf import setup_logger
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO

socketio = SocketIO()


def create_app():
    app = Flask(__name__)
    CORS(app, cors_allowed_origins="*")
    socketio.init_app(app, async_mode='eventlet', cors_allowed_origins="*")
    register_blueprints(app)
    standard_port = 5678
    return app, standard_port


def register_blueprints(app):
    from .routes.route_usb import bp as usb_bp
    app.register_blueprint(usb_bp)
