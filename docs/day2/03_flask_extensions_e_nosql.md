# Extensões

Um dos poderes do Flask é a sua capacidade de ser estendido com facilidade, as extensões do Flask
são criadas seguindo um modelo chamado `Blueprint` que é um template de um pedaço da aplicação que
em determinado momento é acoplado ao `app` em execução.

Blueprints são a mesma coisa que `plugins`, mais para frente veremos como criar um do zero, mas agora vamos ver como podemos usar os plugins em nossa aplicação.

## Banco de dados

O Flask pode trabalhar com qualquer sistema de banco de dados já que ele não tem acoplamento com
nenhum em especifico, como em breve usaremos o Django e o FastAPI com SQL, vamos aproveitar para usar o MongoDB agora com Flask.

O MongoDB é um banco de dados não relacional orientado a documentos `NoSQL` e ao invés de armazenar tabelas ele armazena documentos escritos no formato `BSON` (Binary JSON) que é compatível com a notação `JSON` que já estamos acostumados para trabalhar com APIs e também com `dicts` Python já que podemos facilmente serializar dicts para o formato JSON.

### PyMongo

Pymongo é o driver oficial para conectar a aplicação Python ao MongoDB e com o Flask temos uma extensão chamada `Flask-Pymongo`

```bash
pip install Flask-PyMongo
```

Agora podemos alterar o `app.py` para adicionar uma conexão com banco de dados:

```python
from flask import Flask, url_for, request
from flask_pymongo import PyMongo  # NEW

app = Flask(__name__)

app.config["APP_NAME"] = "Meu Blog"
app.config["MONGO_URI"] = "mongodb://localhost:27017/blog"  # NEW

mongo = PyMongo(app)  # NEW
```

E na view `/` podemos adicionar uma query para listar todos os posts do banco de dados:

`mongo.db.posts.find()` irá através do nosso objeto `mongo` acessar o banco de dados `blog` (que setamos na URI) e procurar
uma coleção chamada `posts`, uma collection é como se fosse uma tabela, mas dentro dela teremos documentos, nesse caso esperamos encontrar as postagens do nosso blog. (não se preocupe já iremos adicionar postagens no banco de dados logo mais)


```py
@app.route("/")
def index():
    posts = mongo.db.posts.find()  # NEW
    content_url = url_for("read_content", slug="qualquer-coisa")
    return (
        f"<h1>Boas vindas a {app.config['APP_NAME']}</h1>"
        f"<a href='{content_url}'>Leia um post</a>"
        "<hr>"
        f"{list(posts)}"  # NEW
    )
```

Ao tentar acessar `/` no navegador termos um erro:

```python
pymongo.errors.ServerSelectionTimeoutError: localhost:27017: [Errno 111] Connection refused, Timeout: 30s
```

E isso acontece pois não temos um servidor **MongoDB** em execução portanto é ideal iniciarmos, você pode optar por instalar o MongoDB, acessar o Mongo as a Service usando uma URL ou rodar dentro de um container, eu vou optar pelo container por ser o jeito mais fácil:

Em um terminal com docker execute:

```bash
docker run -d -p 27017:27017 --name mongo-blog mongo:latest
```

O comando acima irá rodar o MongoDb dentro de um container e deixar executando em segundo plano.

pode verificar usando 

```bash
docker container ls -f name=mongo-blog

CONTAINER ID   IMAGE          COMMAND                  CREATED          STATUS          PORTS                                           NAMES
c58834d006a8   mongo:latest   "docker-entrypoint.s…"   11 minutes ago   Up 11 minutes   0.0.0.0:27017->27017/tcp, :::27017->27017/tcp   mongo-blog
```

Agora sim com o Mongo em execução você pode tentar acessar `/` e verá

```plain
Boas vindas a Meu Blog
Leia um post
-----------------------
[]
```

repare na lista vazia `[]` indicando que não existe nenhum post salvo no banco de dados, agora vamos continuar desenvolvendo as view necessárias para adicionar novos posts em nosso blog.

> Se precisar parar o container pode usar `docker stop mongo-blog`


> DICA: A extensão **MongoDB for VS Code** é útil para acessar o banco de dados através do VSCode.


### PyMongo Overview

Vamos agora explorar o básico das operações que faremos com o MongoDB, comece instalando o terminal ipython com `pip install ipython` e depois executando.

```bash
ipython -i app.py
```

Entramos em um terminal interativo onde podemos efetuar as principais operações com o PyMongo através do objeto `mongo`, comece inspecionando este objeto:

```python
# A conexão com o banco de dados
In [1]: mongo
Out[1]: <flask_pymongo.PyMongo at 0x7f11a04cf3d0>

# O banco de dados chamado `blog`
In [2]: mongo.db
Out[2]: Database(MongoClient(host=['localhost:27017'], document_class=dict, tz_aware=False, connect=False), 'blog')

# A collection `posts` onde salvaremos os documentos contendo as postagens
In [3]: mongo.db.posts
Out[3]: Collection(Database(MongoClient(host=['localhost:27017'], document_class=dict, tz_aware=False, connect=False), 'blog'), 'posts')

# Um cursor que permite executar uma consulta
In [4]: mongo.db.posts.find()
Out[4]: <pymongo.cursor.Cursor at 0x7f11a0a78220>
```

E agora neste mesmo terminal podemos efetuar algumas operações:

```python
# Inserir um novo post no banco de dados
In [5]: mongo.db.posts.insert_one({"title": "Meu primeiro post", "content": "Este é meu primeiro blog post", "published": True})
Out[5]: <pymongo.results.InsertOneResult at 0x7f119b5f5100>

# Obter o ID gerado para o documento inserido
In [6]: _.inserted_id
Out[6]: ObjectId('62b613a07e4b3c31107abd2b')

# Buscar um post através de um atributo especifico
In [7]: mongo.db.posts.find_one({"title": "Meu primeiro post"})
Out[7]: 
{'_id': ObjectId('62b613a07e4b3c31107abd2b'),
 'title': 'Meu primeiro post',
 'content': 'Este é meu primeiro blog post',
 'published': True}

# Buscar todos os posts através de um atributo
In [8]: mongo.db.posts.find({"published": True})
Out[8]: <pymongo.cursor.Cursor at 0x7f11a0130970>

# Consumindo o cursor
In [9]: list(_)
Out[9]: 
[{'_id': ObjectId('62b613a07e4b3c31107abd2b'),
  'title': 'Meu primeiro post',
  'content': 'Este é meu primeiro blog post',
  'published': True}]
```

Estas serão as principais operações que faremos no MongoDB.
