from flask import Flask, url_for, request

app = Flask(__name__)


# O nome da aplicação para usarmos no title do front-end
app.config["APP_NAME"] = "Meu Blog"

# Adicionamos um error handler
@app.errorhandler(404)
def not_found_page(error):
    return f"<strong>Desculpe</strong> página não encontrada em {app.config['APP_NAME']}"


# Opcionalmente podemos registrar sem o decorator
# app.register_error_handler(404, not_found_page)


#Adicionamos uma URL usando decorator
@app.route("/")
def index():
    content_url = url_for("read_content", slug="qualquer-coisa")
    return (
        f"<h1>Boas vindas a {app.config['APP_NAME']}</h1>"
        f"<a href='{content_url}'>Leia um post</a>"
        "<hr>"
        f"{request.args.get('author')}"
        "<hr>"
        f"{dir(request)}"
    )


# Adicionamos outra URL usando método add_url_rule
def read_content(slug):
    index_url = url_for("index")
    return f"<h1>{slug}</h1><a href='{index_url}'>Voltar ao inicio</a>"


app.add_url_rule("/<string:slug>", view_func=read_content)
