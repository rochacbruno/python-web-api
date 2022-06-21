from flask import Flask

app = Flask("app")

@app.route("/")
def hello():
    return "<strong>Hello World</strong>"
