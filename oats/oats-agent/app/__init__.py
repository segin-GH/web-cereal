from flask import Flask
from flask_cors import CORS
from config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Enable CORS
    CORS(app)

    from app.routes.usb import bp as usb_bp
    app.register_blueprint(usb_bp)

    return app
