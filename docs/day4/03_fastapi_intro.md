# 33 - Fast API

FastAPI é um framework web Python que tem ganhado bastante destaque pelo fato de implementar abordagens mais modernas ao desenvolvimento web.

O FastAPI utiliza funções assincronas para definição de views e também tem sua API baseada
em anotação de tipos o que deixa o código mais
expressivo e menos sujeito a erros.

O FastAPI é baseado em outros 3 projetos Python.

1. Starlette (Framework ASGI)
2. Pydantic (Validador de Tipos)
3. Uvicorn (Servidor ASGI)

## Instalação

Para instalar o framework completo use

```console
$ pip install "fastapi[all]"
``` 

> adicionando `[all]` faz com que o uvicorn também seja instalado.

## Hello World

Crie um arquivo chamado `hello_fastapi.py` com o seguinte conteúdo:

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def hello():
    return {"message": "Hello World"}
```

na mesma pasta execute o **uvicorn**

```console
$ uvicorn hello_fastapi:app --reload

INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [28720]
INFO:     Started server process [28722]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
``` 

O comando `uvicorn hello_fastapi:main --reload` refere-se a:

- hello_fastapi = o módulo Python `hello_fastapi.py`
- `app` é o objeto FastAPI dentro do módulo
- `--reload` faz com que o reload seja automático ao efetuar alterações

Acesse http://127.0.0.1:8000 e veja a mensagem 

```json
{"message": "Hello World"}
```

## OpenAPI Docs

O FastAPI automaticamente cria uma documentação viva do projeto baseada na OpenAPI spec (swagger) que é uma documentação para desenvolvedores que pretendem fazer integração com sua API.

Acesse http://127.0.0.1:8000/docs e veja a documentação da API

## Redoc

Além do swagger o FastAPI também cria uma documentação baseada em Redoc que tem uma interface mais amigável e é mais legivel podendo até servir para imprimir a especificação da API para incluir em contratos por exemplo.

Acesse http://127.0.0.1:8000/redoc e veja a documentação com Redoc.

## Parametros de URL Path

É possivel receber parametros dinâmicos através do caminho da URL, imagine que estamos criando uma API que irá retornar informações de um usuário e queremos que a URL http://127.0.0.1:8000/user/jim retorne informações sobre Jim e http://127.0.0.1:8000/pam retorne informações sobre a Pam.

Edite o `hello_fastapi.py` e adicione ao final.

```python
...

@app.get("/user/{username}")
async def user_profile(username: str):
    return {"data": username}

```

Agora acesse http://127.0.0.1:8000/user/jim e veja o retorno.

## Multiplos parâmetros

Seguindo a mesma lógica podemos adicionar multiplos paramêtros, vamos criar por exemplo um endpoint que retorna uma conta bancária através de seu numero inteiro

```python

@app.get("/account/{number}")
async def account_detail(number: int):
    return {"account": number}
```

Acesse http://127.0.0.1:8000/account/1234 e veja o resultado.

## Validação com tipos

Em nossos simples exemplos ainda não estamos fazendo muita coisa, apenas um retorno fixo em formato JSON porém o FastAPI com a ajuda do Pydantic já está adicionando uma camada poderosa de validação, anotamos a view `account_detail` com `number: int` portanto não precisamos nos preocupar com a validação, experimente:

http://127.0.0.1:8000/account/foobarzaz

como `foobarzaz` não é um `int` válido, o FastAPI vai automaticamente validar e retornar.

```json
{
    "detail": [
        {
            "loc": [
                "path",
                "number"
            ],
            "msg": "value is not a valid integer",
            "type": "type_error.integer"
        }
    ]
}
```

Esta validação também estará explicita na documentação

http://127.0.0.1:8000/docs

## Ordem das URLS

A ordem de definição das URLs é muito importante, lembra de quando criamos nosso próprio framework lá no day1 e fizemos match em cima de uma lista de regex patterns? O primeiro que faz match é o que o FastAPI vai assumir como o correto, portanto no seguinte exemplo:

```python
...

@app.get("/user/{username}")
async def user_profile(username: str):
    return {"data": username}

@app.get("/user/list")
async def user_list():
    return {"users": ["jim", "pam", "dwight"]}
```

No exemplo acima nunca conseguiremos acessar a URL `/user/list` pois a URL `/user/{username}` irá fazer match antes e `list` será considerado o valor para `username`.

Neste caso precisamos sempre declarar as rotas mais especificas antes,basta inverter a ordem.

```python
...

@app.get("/user/list")
async def user_list():
    return {"users": ["jim", "pam", "dwight"]}


@app.get("/user/{username}")
async def user_profile(username: str):
    return {"data": username}
```

## Parametros pré definidos

Caso uma URL possua parametros pré definidos, ou seja, o request pode ser feito apenas em cima de um conjunto especifico de opções, podemos usar `Enum` para definir.

Vamos alterar a nossa rota `/user/list` para ser mais genérica e também aceitar `/account/list/` e `/department/list`

```python
from enum import Enum


class ListOption(str, Enum):
    user = "user"
    account = "account"
    department = "department"


@app.get("/{list_option}/list")
async def generic_list(list_option: ListOption):

    if list_option == ListOption.user:
        data = ["jim", "pam", "dwight"]
    elif list_option.value == "account":
        data =  [1234, 5555, 9999]
    elif list_option == ListOption.department:
        data = ["Sales", "Management", "IT"]
    
    return {list_option: data}
```

Veja só com isso é tratado na OpenAPI

http://127.0.0.1:8000/docs


## Paths contendo paths

Existe um caso especial onde apenas a declaração de tipo não é suficiente para dar o match na URL, que é quando temos uma url que recebe um caminho de um arquivo ou pasta como paramêtro, como o caminho do arquivo pode conter `/` o matcher precisa saber exatamente onde começa essa especificação, neste caso usamos um **path convertor** diretamente do Starlette.

Imagine agora uma rota onde precisamos iniciar a importação de um arquivo que está no sistema de arquivos do servidor no caminho `arquivos/sistema/dados.csv`, para isso usamos `:path` na definição da rota.

```python

@app.get("/import/{file_path:path}")
async def import_file(file_path: str):
    return {"importing": file_path}

```

## Outros métodos HTTP

Até aqui falamos sobre `app.get` mas basta substituir pelo método HTTP desejado e o funcionamento do roteamento é o mesmo.

Crud Básico:

```python
@app.post()     # Create
@app.get()      # Read
@app.put()      # Update
@app.delete()   # Delete
```

E métodos alternativos HTTP que raramente precisamos utilizar.

```python
@app.patch()   # Update Parcial
@app.options() # Opções do protocolo
@app.head()    # Headers
@app.trace()   # Diagnosticos
```