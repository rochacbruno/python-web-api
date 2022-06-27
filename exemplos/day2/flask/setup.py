from setuptools import setup

setup(
    name="flask_blog",
    version="0.1.0",
    packages=["blog"],
    install_requires=["flask", "flask-pymongo", "dynaconf", "flask-bootstrap"]
)
