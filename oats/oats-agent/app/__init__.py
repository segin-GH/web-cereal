from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO  # Import Flask-SocketIO
from config import Config

socketio = SocketIO()  # Create a SocketIO instance


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Enable CORS
    CORS(app)

    # Initialize Flask-SocketIO with your app
    # Adjust cors_allowed_origins as needed
    socketio.init_app(app, cors_allowed_origins="*")

    from app.routes.usb import bp as usb_bp
    app.register_blueprint(usb_bp)

    return app
