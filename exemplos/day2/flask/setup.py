from setuptools import setup

setup(
    name="flask_blog",
    version="0.1.0",
    packages=["blog"],
    install_requires=[
        "flask",
        "flask-pymongo",
        "dynaconf",
        "flask-bootstrap",
        "mistune",
        "flask-simplelogin",
        # "flask-admin",
        "flask-admin @ git+ssh://git@github.com/flask-admin/flask-admin#egg=flask-admin"
    ],
)
