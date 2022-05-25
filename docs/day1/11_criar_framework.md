# Criando seu próprio framework

Você já deve ter ouvido falar do **Flask** ? um dos principais frameworks para desenvolvimento web com Python, agora vamos fazer um exercicio bem simples, vamos criar nosso próprio framework que vai funcionar de maneira similar ao Flask.

A primeira tarefa é escolher qual será o nome do framework, e você pode escolher o nome que você quiser!

Eu por exemplo vou dar ao meu framework o nome do meu filho `Erik` e você ai no seu ambiente pode acompanhar este exercicio dando o nome que você quiser! pode usar o nome de uma pessoa, de um animal de estimação, de um personagem do seu filme favorito.

Precisa de idéias?

- Corleone framework
- Tony framework
- Dwight framework
- SpaceGhost framework
- Banana framework
- Tapioca framework
- Farofa framework

Use sua criatividade.

Por enquanto toda a lógica do nosso programa está em `wsgi.py` vamos então criar um novo arquivo na mesma pasta.

```bash
# use o nome que quiser,
# desde que siga as regras de nomenclatura do Python
# tudo em minusculo, sem espaços.
touch erik.py
```

Agora vamos usar orientação a objetos para transformar o que tinhamos no `wsgi.py` usando apenas funções para um modelo usando orientação a objetos, portanto no arquivo `erik.py` (lembre-se que você pode usar o nome que quiser) nós vamos.

01. Criar uma classe para representar a `app` do nosso framework
00. Inicializar os objetos essenciais de um framework
    - Mapa de roteamento de URLs
    - Configuração de template
    - Ambiente do motor de templates
00. Um decorator para registar novas URLs no estilo do Flask.
00. Um método para renderizar templates.
00. A aplicação `wsgi` implementada em um método `__call__`
00. Um método `run` para executar a aplicação


Um framework web em 60 linhas de código :)


```py
import cgi
import json
import re
from wsgiref.simple_server import make_server

from jinja2 import Environment, FileSystemLoader


class Erik:  # Dê o nome que quiser :) ex: `class Banana`
    def __init__(self):
        self.url_map = []
        self.template_folder = "templates"
        self.env = Environment(loader=FileSystemLoader("templates"))

    def route(self, rule, method="GET", template=None):
        def decorator(view):
            self.url_map.append((rule, method, view, template))
            return view

        return decorator

    def render_template(self, template_name, **context):
        template = self.env.get_template(template_name)
        return template.render(**context).encode("utf-8")

    def __call__(self, environ, start_response):
        path = environ["PATH_INFO"]
        request_method = environ["REQUEST_METHOD"]
        body = b"Content Not Found"
        status = "404 Not Found"
        ctype = "text/html"

        for rule, method, view, template in self.url_map:
            match = re.match(rule, path)
            if match:
                if method != request_method:
                    continue
                view_args = match.groupdict()
                if method == "POST":
                    view_args["form"] = cgi.FieldStorage(
                        fp=environ["wsgi.input"],
                        environ=environ,
                        keep_blank_values=1,
                    )
                view_result = view(**view_args)

                if isinstance(view_result, tuple):
                    view_result, status, ctype = view_result
                else:
                    status = "200 OK"

                if template:
                    body = self.render_template(template, **view_result)
                elif (
                    isinstance(view_result, dict)
                    and ctype == "application/json"
                ):
                    body = json.dumps(view_result).encode("utf-8")
                else:
                    body = str(view_result).encode("utf-8")

        start_response(status, [("Content-type", ctype)])
        return [body]

    def run(self, host="0.0.0.0", port=8000):
        server = make_server(host, port, self)
        server.serve_forever()
```


Podemos testar com:

```py
app = Erik()

@app.route("^/$")
def foo():
    return "Hello"

@app.route("^/(?P<id>\d{1,})$")
def foo2(id):
    return f"Hello {id}", 400, "foo"


# Simular chamadas HTTP
print(
    app(
        {"PATH_INFO": "/1234", "REQUEST_METHOD": "GET"},
        lambda *args: print(args),
    )
)
print(
    app(
        {"PATH_INFO": "/", "REQUEST_METHOD": "GET"},
        lambda *args: print(args),
    )
)
```
O resultado
```
(400, [('Content-type', 'foo')])
[b'Hello 1234']
('200 OK', [('Content-type', 'text/html')])
[b'Hello']
```

Agora vamos colocar em uso em nosso blog, alteramos o arquivo `wsgi.py` para usar o nosso framework.


```py
from database import conn
from erik import Erik

app = Erik()


@app.route("^/$", template="list.template.html")
def post_list():
    posts = get_posts_from_database()
    return {"post_list": posts}


@app.route("^/(?P<id>\d{1,})$", template="post.template.html")
def post_detail(id):
    post = get_posts_from_database(post_id=id)[0]
    return {"post": post}


@app.route("^/new$", template="form.template.html")
def new_post_form():
    return {}


@app.route("^/new$", method="POST")
def new_post_add(form):
    post = {item.name: item.value for item in form.list}
    add_new_post(post)
    return "New post Created with Success!", "201 Created", "text/plain"


def get_posts_from_database(post_id=None):
    cursor = conn.cursor()
    fields = ("id", "title", "content", "author")

    if post_id:
        results = cursor.execute("SELECT * FROM post WHERE id = ?;", post_id)
    else:
        results = cursor.execute("SELECT * FROM post;")

    return [dict(zip(fields, post)) for post in results]


def add_new_post(post):
    cursor = conn.cursor()
    cursor.execute(
        """\
        INSERT INTO post (title, content, author)
        VALUES (:title, :content, :author);
        """,
        post,
    )
    conn.commit()


if __name__ == "__main__":
    app.run()
```


## Conclusão:

Criar um framework com Python é super divertido, porém tem muito mais coisas que um framework precisa fazer:

- Facilidade no registro de rotas
- Segurança e autenticação
- Sessões e Cookies
- Execução assincrona

Para não ter esse trabalho todo manualmente, vamos deixar nosso framerwork caseiro de lado e começar a conhecer as soluções prontas para Python.

Finalizamos aqui o Day 1 e no próximo daremos inicio ao aprendizado dos frameworks Django, Flask e FastAPI :)


Até o Day 2 :)