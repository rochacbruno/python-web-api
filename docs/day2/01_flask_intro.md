# Flask

## Instalação

O Flask é a união entre 2 importantes e bastante estabelecidas bibliotecas.

- Werkzeug: Uma biblioteca que implementa o protocolo HTTP conforme vimos no Day1
- Jinja2: Um motor de templates conforme vimos no Day1

O Flask é a junção dessas 2 ferramentas utilizando boas práticas de orientação a objetos e uma ótima documentação.

Uma das coisas mais interessantes do Flask é o seu sistema de plugins que permite ser facilmente estendido para as mais diversas necessidades.

Para instalar:

**dentro de uma virtualenv**
```bash
pip install flask
```

Após instalado o pacote pode ser inspecionado com:

```bash
pip show flask   
```

Resultado:
```yaml
Name: Flask
Version: 2.1.2
Summary: A simple framework for building complex web applications.
Home-page: https://palletsprojects.com/p/flask
Author: Armin Ronacher
Author-email: armin.ronacher@active-4.com
License: BSD-3-Clause
Location: ./.venv/lib/python3.8/site-packages
Requires: click, importlib-metadata, itsdangerous, Jinja2, Werkzeug
```

> Como pode perceber o Flask instala junto com ele o Jinja2, o Werkzeug, o Click e outras 2 bibliotecas de utilidade.

## Iniciando

Para começar criamos uma pasta em `exemplos/day2/flask` e dentro desta pasta um arquivo `app.py`, poderiamos dar qualquer nome ao nosso programa mas existe uma convenção na comunidade Flask de nomear sempre com `app.py` o arquivo que serve como ponto de entrada para a aplicação.

Para começar bem vamos fazer primeiro o "Hello World" do Flask e então entender como funciona sua ferramenta de linha de comando.

`app.py`
```python
from flask import Flask

app = Flask("app")  # ou Flask(__name__)

@app.route("/")
def hello():
    return "<strong>Hello World</strong>"
```

Com esse conteúdo dentro do arquivo podemos agora executar:

```bash
flask run
```

> Repare que se por acaso você executar `flask run` fora da pasta onde está o arquivo `app.py` vai obter o seguinte erro `Error: Could not locate a Flask application. You did not provide the "FLASK_APP" environment variable, and a "wsgi.py" or "app.py" module was not found in the current directory.`

Portanto o Flask espera que a variável de ambiente `FLASK_APP` indique o caminho para o módulo onde está a aplicação, ou que tenha um arquivo com nomes app ou wsgi.

Para resolver podemos fazer de 2 maneiras.

1. setando a variável de ambiente:

```bash
FLASK_APP=exemplos/day2/flask/app.py flask run 
```

Ou melhor, entrando diretamente na pasta

```bash
cd exemplos/day2/flask/
flask run
```

Em ambos os casos o resultado será:

```bash
 * Serving Flask app 'exemplos/day2/flask/app.py' (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000 (Press CTRL+C to quit)
```

Em primeiro lugar acesse http://127.0.0.1:5000 no seu navegador para ver se está tudo ok, você deve ver a mensagem `Hello World`

Agora vamos analisar um pouco do funcionamento do `flask` CLI, essa ferramenta que rodamos na linha de comando.

Para visualizar todos os comandos:

```bash
flask --help
...
Commands:
  routes  Show the routes for the app.
  run     Run a development server.
  shell   Run a shell in the app context.
```

Experimente cada um dos comandos:

routes - exibe todas as URLs registradas.

```bash
flask routes

Endpoint  Methods  Rule
--------  -------  -----------------------
hello     GET      /
static    GET      /static/<path:filename>
```

shell - abre um terminal interativo no contexto da aplicação

```bash
flask shell
...

App: app [production]
Instance: ./exemplos/day2/flask/instance
```

E o comando `run` executa a aplicação usando o servidor de desenvolvimento.

```bash
flask run   
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000 (Press CTRL+C to quit)
```

Ao executar com o `run` alguns detalhes são importantes, repare que a mensagem de warning recomenda não
usar em ambiente de produção, pois como já vimos no Day1 do treinamento, para produção existem outros tipos de servidores mais robustos como o `gunicorn`.

Portanto durante o desenvolvimento precisaremos sempre rodar no modo de dev e isso pode ser feito usando uma variável de ambiente.

```bash
export FLASK_ENV=development
flask run
```

A execução agora será um pouco diferente:

```bash
FLASK_ENV=development flask run
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000 (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 844-118-716
```

Com isso estamos executando no modo de `development` que faz com que algumas features estejam ativadas, as principais: 

- Auto Reload: Quando mudamos o código o servidor reinicia automaticamente
- Debugger: Em caso de erros teremos acesso a um terminal de debugging no próprio navegador
    - **IMPORTANTE** Para acessar o debugger será necessário ter o código PIN impresso no terminal.
