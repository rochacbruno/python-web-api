from flask_pymongo import PyMongo

mongo = PyMongo()


def configure(app):
    mongo.init_app(app)
