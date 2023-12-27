from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from config import Config

socketio = SocketIO()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    CORS(app, cors_allowed_origins="*")

    socketio.init_app(app, async_mode='eventlet')

    # Import and register your blueprints here to avoid circular imports
    from .routes.route_usb import bp as usb_bp
    app.register_blueprint(usb_bp)

    return app
