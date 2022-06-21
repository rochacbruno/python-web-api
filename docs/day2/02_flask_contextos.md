# Contexts

O Flask funciona baseado em contextos, um contexto é o estado da aplicação Flask durante cada um dos estágios da aplicação e isso é importante pois define o acesso a certos objetos que só existem em determinados contextos e existem 3 contextos principais.

## 1. Configuração

Dizemos que a aplicação Flask está em contexto de configuração (ou tempo de configuração) a partir do momento em que a instância do objeto é criada até o momento em que o servidor de aplicação WSGI começa a servir a aplicação.

No contexto de configuração podemos efetuar algumas operações como:

```python
# criamos a instância e iniciamos o contexto de configuração
from flask import Flask
app = Flask(__name__)

# Adicionar variáveis de configuração
app.config["CHAVE"] = "valor"

# Registrar novas extensões/plugins
admin = Admin()
admin.init_app(app)

# Registrar Blueprints (módulos flask)
app.register_blueprint(modulo)

# Registrar Template Filters e Context Processors
app.add_template_global(function)

@app.template_filter('reverse')
def reverse_filter(s):
    return s[::-1]

@app.context_processor
def inject_user():
    return dict(user=g.user)

# Registrar hooks
@app.before_request
def function(): ...

app.register_error_handler(400, handle_bad_request)

# Registrar novas URLS
@app.route("/")
def function(): ...

app.add_url_rule("/", view_func=function)
```

## 2. Aplicação

O contexto de aplicação começa a partir do momento em que a aplicação começa a ser servida por um servidor WSGI.


## 3. Request
