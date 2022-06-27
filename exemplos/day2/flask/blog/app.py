from flask import Flask
from .config import configure


def create_app():
    app = Flask(__name__)
    configure(app)
    return app
