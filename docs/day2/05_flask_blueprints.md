# Blueprints

Blueprint é o padrão usado pelo flask para extendermos nossa aplicação com funcionalidades,
em nosso caso teremos as views para o nosso blog.

- / -> listar todos os posts
- /slug-do-post -> Ler um post especifico
- /new -> formulário para criar novo post

Vamos começar pelos templates

Em todas essas URLs iremos renderizar um template base usando o framework CSS **Bootstrap**, portanto precisaremos da extensão Flask-Bootstrap e para inicializa-la faremos 2 alterações

`setup.py`
```python

    install_requires=["flask", "flask-pymongo", "dynaconf", "flask-bootstrap"]  # NEW

```
Depois rodamos na mesma pasta onde está o `setup.py`

```bash
pip install -e .
```

E no `settings.toml`

```toml
[default]
mongo_uri = "mongodb://localhost:27017/blog"
extensions = [
    "blog.database:configure",
    "blog.commands:configure",
    "flask_bootstrap:Bootstrap"  # NEW
]
```

## Templates

Agora podemos criar os templates:

`templates/base.html.j2`
```html
{% extends "bootstrap/base.html" %}
{% block title %}{{config.get('TITLE')}}{% endblock %}

{% block navbar %}
<div class="navbar">
<div class="navbar-header">
    <a class="navbar-brand" href="#">
    <img alt="Brand" src="https://via.placeholder.com/150x50?text=BLOG">
    </a>
</div>
</div>
{% endblock %}
```

`templates/index.html.j2`
```html
{% extends "base.html.j2" %}

{% block content %}
<div class="container">
<h1>{{config.get('TITLE')}}</h1>

<div class="jumbotron">
<ul class="list-group">
    {% for post in posts %}
    <li class="list-group-item">
        <a href="{{url_for('post.detail', slug=post.slug)}}">{{post.title}}</a>
    </li>
    {% endfor %}
</ul>
</div>

</div>
{% endblock %}
```

`templates/post.html.j2`
```html
{% extends "base.html.j2" %}
{% block content %}
<div class="container">
<h1>{{ post.title }}</h1>

<div class="jumbotron">
<h2>{{ post.date }}</h2>
<p>
    {{ post.content }}
</p>
</div>
</div>
{% endblock %}
```

`templates/form.html.j2`
```html
{% extends "base.html.j2" %}
{% block content %}
<div class="container">
<h1>New Post</h1>

<div class="jumbotron">

<form action="/new" method="post">
    <label for="title">Title:</label><br>
    <input type="text" name="title" /><br>
    <label for="content">Content:</label><br>
    <textarea name="content" cols="30" rows="5"></textarea><br>
    <input type="submit" value="Enviar">
</form>

</div>
</div>
{% endblock %}
```

### Blueprint

Vamos criar o nosso blueprint no arquivo `view.py`


```python

```
