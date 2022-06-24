# Projeto

Nós vamos criar agora um pequeno blog usando Flask, salvaremos as postagens em um banco de dados MongoDB (pois uma das caracteristicas interessantes do Flask é trabalhar bem com bancos não relacionais) e usaremos markdown como linguagem de marcação para as postagens.

Este exemplo é bem simples mas vai nos dar material necessário para explorar as principais funcionalidades do framework.


## Os Contextos do Flask

O Flask funciona baseado em contextos, um contexto é o estado da aplicação Flask durante cada um dos estágios da aplicação e isso é importante pois define o acesso a certos objetos que só existem em determinados contextos e existem 3 contextos principais.

### 1. Configuração

Dizemos que a aplicação Flask está em contexto de configuração (ou tempo de configuração) a partir do momento em que a instância do objeto é criada até o momento em que o servidor de aplicação WSGI começa a servir a aplicação.

No contexto de configuração podemos efetuar algumas operações como:

- Iniciar a instância
- Definir configurações
- Registrar extensões/plugins
- Registrar Blueprints/modulos
- Adicionar filtros e funções ao Jinja (para os templates)
- Adicionar Hooks
- Adicionar processadores de contexto (uteis para autenticação)

Vamos começar fazendo algumas dessas coisas e em breve voltamos para adicionar mais.

Vamos editar o arquivo `app.py` e adicionar algumas configurações:

```python
from flask import Flask

app = Flask(__name__)

# O nome da aplicação para usarmos no title do front-end
app.config["APP_NAME"] = "Meu Blog"

# Adicionamos um error handler
@app.errorhandler(404)
def not_found_page(error):
    return f"<strong>Desculpe</strong> página não encontrada em {app.config['APP_NAME']}"

# Opcionalmente podemos registrar sem o decorator
# app.register_error_handler(404, not_found_page)
```

Execute a aplicação com

```bash
FLASK_ENV=development flask run
```

E acesse http://127.0.0.1:5000/ verá a mensagem ou http://127.0.0.1:5000/titulo-do-post:

para qualquer página que tentar acessar verá:

```text
Desculpe página não encontrada em Meu Blog
```

**Lembre-se** estamos no contexto de configuração do Flask, portanto só podemos fazer as coisas listadas acima.

Se tentarmos por exemplo, gerar uma URL usando a função `url_for`

```python
from flask import Flask, url_for  # NEW

...

print(url_for("index"))

```

Veremos um erro:

```python
RuntimeError: Attempted to generate a URL without the application context being pushed. This has to be executed when application context is available.
```

Isso acontece pois alguns objetos só podem ser utilizados no contexto de ***aplicação**, esses objetos são: 

- url_for - função usada para gerar URL reversa
- current_app - objeto que retorna a instancia da aplicação em execução
- g - objeto Global usado para compartilhar dados entre componentes


Mas ainda no contexto de **configuração** podemos registrar novas URLs.


No final do `app.py`

```python
#Adicionamos uma URL usando decorator
@app.route("/")
def index():
    return f"<h1>Boas vindas a {app.config['APP_NAME']}</h1>"


# Adicionamos outra URL usando método add_url_rule
def read_content(slug):
    return f"<h1>{slug}</h1>"


# passamos a **view** como parametro
app.add_url_rule("/<string:slug>", view_func=read_content)
```

> Usar `@app.route` é a mesma coisa que usar `app.add_url_rule`.

Agora ao acessar a aplicação poderá ver as mensagens na rota `/` e `/qualquer-titulo`

### 2. Aplicação

O contexto de aplicação começa a partir do momento em que a aplicação começa a ser servida por um servidor WSGI.

Este contexto só pode ser acessado de maneira **Lazy**, ou seja, apenas após a aplicação estar em execução e dentro de **views**.

Vamos alterar as views `index` e `read_content` e focar em entender o funcionamento da geração de URLs reversas com `url_for`.

```python
def index():
    content_url = url_for("read_content", slug="qualquer-coisa")
    return (
        f"<h1>Boas vindas a {app.config['APP_NAME']}</h1>"
        f"<a href='{content_url}'>Leia um post</a>"
    )

def read_content(slug):
    index_url = url_for("index")
    return f"<h1>{slug}</h1><a href='{index_url}'>Voltar ao inicio</a>"
```


### 3. Request

Existem alguns objetos que só estão disponíveis no contexto de **request** que é quando a aplicação recebe uma requisição, processa e retorna a resposta.

Por exemplo tente colocar na raiz do `app.py` o seguinte código

```python
from flask import Flask, url_for, request  # NEW

app = Flask(__name__)

print(request.args)
```

Ao tentar acessar a aplicação verá o seguinte erro:

```python
RuntimeError: Working outside of request context.

This typically means that you attempted to use functionality that needed
an active HTTP request.  Consult the documentation on testing for
information about how to avoid this problem.
```

Isso significa que para acessar os valores no objeto `request` precisamos ter uma requisição HTTP ativa e no entando colocamos
o `print(request.args)` no contexto de configuração.

Alguns objetos só podem ser acessados no contexto de request e eles são:

- **request** - Para acessarmos as informações da requisição HTTP
- **session** - Para criarmos e acessarmos sessões criadas com cookies


Ou seja, esses objetos só podem ser acessados dentro de funções que serão invocadas durante uma requisição HTTP como `views`, `context_processors`, `error_handlers` etc.


Agora podemos alterar o `app.py` e usar o `request` no local correto.


```python
@app.route("/")
def index():
    content_url = url_for("read_content", slug="qualquer-coisa")
    return (
        f"<h1>Boas vindas a {app.config['APP_NAME']}</h1>"
        f"<a href='{content_url}'>Leia um post</a>"
        "<hr>"
        f"{request.args}"
    )
```

Ao acessar a aplicação em http://127.0.0.1:5000/ verá o seguinte:

```python
Boas vindas a Meu Blog
Leia um post
----------------------
ImmutableMultiDict([])
```

o objeto `request` possui vários atributos, o `.args` é onde ficam os argumentos passados via query string, tente abrir agora a URL http://127.0.0.1:5000/?published=true&order_by=date&author=Bruno

Os argumentos passados em `?published=true&order_by=date&author=Bruno` estarão disponíveis em `request.args`

```python
Boas vindas a Meu Blog
Leia um post
----------------------
ImmutableMultiDict([('published', 'true'), ('order_by', 'date'), ('author', 'Bruno')])
```

O objeto `ImmutableMultiDict` serve para armazenar dados vindos do request, similar so `cgi.FieldStorage` que vimos no Day 1 do treinamento.

Como este objeto é um `Dict Like` object podemos acessar apenas as chaves que desejarmos usando `.get`

```python
def index():
    content_url = url_for("read_content", slug="qualquer-coisa")
    return (
        f"<h1>Boas vindas a {app.config['APP_NAME']}</h1>"
        f"<a href='{content_url}'>Leia um post</a>"
        "<hr>"
        f"{request.args.get('author')}"  # NEW
    )
```

Resultado ao acessar http://127.0.0.1:5000/?published=true&order_by=date&author=Bruno

```python
Boas vindas a Meu Blog
Leia um post
----------------------
Bruno
```

O objeto `request` tem muitos atributos interessantes que podem ser acessados dentro de uma `view function`

- `request.method` - O método HTTP utilizado 
- `request.headers` - Todos os cabeçalhos HTTP
- `request.cookies` - Listar e criar cookies no cliente HTTP
- `request.url` - A URL requisitada
- `request.environ` - O `environ` do protocolo WSGI que vimos no Day 1
- `request.form` - Dados submetidos através de um POST de formulário
- `request.json` - Dados recebidos com `content-type/json`
- `request.files` - Arquivos recebidos via upload
- `request.args` - Dados recebidos via query string
- `request.data` - Todos os dados agrupados


Agora que você já sabe sobre os 3 contextos do **Flask** podemos partir para nossa próxima missão, te vejo na próxima aula.
