# Cliente Servidor

No exemplo que fizemos anteriormente abrimos o arquivo `pagina.html`  diretamente no navegador pois o navegador estava localizado no mesmo computador onde o arquivo está armazenado.

Geralmente não é assim que as coisas funcionam na web, quase sempre teremos os arquivos em computadores remotos, os **servidores** e um outro computador que faz um **pedido** de um arquivo, o **cliente**.

## Proxy Reverso

Além de ter o arquivo disponível para ser servido no sistema de arquivos do servidor (e.x: no HD) o computador servidor precisa de um software que controle o acesso aos arquivos, pois se simplesmente deixar a porta de acesso aberta livremente para qualquer pedido dos clientes poderia abrir brechas de segurança.

Para controlar o acesso aos recursos internos existe um sistema chamado de **proxy**, neste caso especificamente um **proxy reverso** e existem várias tecnologias para fazer isso sendo as famosas o **Apache** e o **Nginx**, como esses programas fazem muito mais coisas do que apenas serem um proxy chamamos eles de **web servers**.

![](imgs/proxy_reverso.png)

## O protocolo HTTP

No lado servidor teremos um **web server** como o **Nginx** ou **Apache** e no lado cliente teremos navegadores como **Firefox** ou **Chrome**.

Para que todos esses programas consigam trocar informações de forma padronizada, no começo dos anos 90 foi criado um protocolo, um padrão de comunicação que todos os sistemas web seguem, o [HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP), HyperText Transfer Protocol (Protocolo de Transferência de Hiper Texto) e ele foi inicialmente pensado para suportar um texto no formato HTML, arquivos estáticos como css, js e imagens e também metadados que são informações que trafegam junto com os arquivos.

O HTTP está baseado em 2 açoes principais.

- **PEDIDO** (Request) - Um texto que especifica o pedido do cliente.
- **RESPOSTA** (Response) - Um texto que contém a resposta do servidor.

E organiza-se em uma série de **verbos**, que também são chamados de **métodos** e são palavras chave que determinam a natureza da ação que o cliente deseja executar no servidor.

https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods

- **GET** - O cliente quer **pegar** um arquivo que está no servidor.
- **POST** - O cliente quer **enviar** um arquivo para o servidor.
- **PUT** ou **PATCH** - O cliente quer **alterar** um arquivo que está no servidor.
- **DELETE** - O cliente quer **apagar** um arquivo que está no servidor.

> 99% de tudo o que fazemos na web está relacionado a estas operações, essas operações são chamadas geralmente pela sigla **CRUD** (Create, Read, Update, Delete)

### Request

O navegador vai enviar ao servidor um texto como esse:

```http
GET /pagina.html
User-Agent: Firefox/100
Accept: */*

```

Detalhando:
- Pedido **GET** para pegar o arquivo no caminho **/pagina.html**.
- Cabeçalhos: 
    - Informação sobre qual é o cliente, neste caso um navegador **Firefox**.
    - Informação sobre quais tipos de arquivo o cliente aceita, neste caso qualquer tipo, mas poderia ser `text/html` para ser mais especifico.

Além de `User-Agent:` e `Accept:` várias outras informações podem ser enviadas e essas informações são chamadas de `HEADERS` (cabeçalho)

> Repare na linha em branco no final, ela indica que o request terminou.

#### Criando um HTTP client com Python

```py
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('example.com', 80))
cmd = 'GET http://example.com/index.html HTTP/1.0\r\n\r\n'.encode()
client.send(cmd)

while True:
    data = client.recv(512)
    if len(data) < 1:
        break
    print(data.decode(),end='')

client.close()
```

Felizmente não precisamos escrever sockets desta maneira em Python pois existem muitas bibliotecas que já fazem isso de maneira abstraida.

Com biblioteca built-in
```py
from urllib.request import urlopen
result = urlopen("http://example.com/index.html")
print(result.read().decode("utf-8"))
```

Com biblioteca externa

```py
import requests
result = requests.get("http://example.com/index.html")
print(result.status_code)
print(result.content)
```

> **NOTA** aconselho substituir `requests` por `httpx` sempre que possível.


### Response

Quando o **web server** recebe este pedido ele processa as informações ali contidas e faz processamentos como por exemplo roteamento, validação, autenticação etc para finalmente ir ao sistema de arquivos e encontrar o arquivo a ser retornado.

A resposta também será dada em forma de texto.

```html
HTTP/2 200 Ok
Server: Nginx
Content-Type: text/html
Date: 07 May 2022 00:40:25 GMT
Content-Lenght: 140

<html>

<head>
    <link rel="stylesheet" href="estilo.css">
</head>
<body>
    ...
    <script type="application/javascript" src="script.js"></script>
</body>

</html>
```

Detalhando:
- Resposta `HTTP/2` com status `200` ok
- Cabeçalhos:
    - Nome do servidor
    - Tipo de conteúdo
    - Data de criação do conteúdo
    - Tamanho do conteúdo em bytes
- Body:
    - O Hypertexto, neste caso HTML

> **Detalhe**: O servidor responde apenas com o arquivo `pagina.html` e portanto o navegador na hora de processar este arquivo vai perceber que existe uma tag `<link>` apontando para o arquivo `estilo.css` e outra tag `<script>` apontando para o arquivo `script.js` e então mais 2 pedidos separados serão efetuados.


### Status codes

Uma informação importantissima nas respostas HTTP é o código de estado, ou `status code`.

É com esse código que podemos validar se seu tudo certo com o pedido que fizemos ao servidor.

No exemplo anterior o código retornado foi `200 Ok` e existe uma lista de códigos divididos em 5 categorias.

- **100-199** = Informativos.
- **200-299** = Códigos de sucesso.
- **300-399** = Redirecionamentos.
- **400-499** = Algo errado no lado cliente ou o pedido foi mal feito.
- **500-599** = Algo errado no lado servidor. 

Para ver a lista completa: 
https://developer.mozilla.org/en-US/docs/Web/HTTP/Status


## Conclusão

O objetivo do desenvolvimento web backend é acessar recursos disponíveis no servidor, processar e entregar ao cliente em formato de texto, para esta comunicação ocorrer de forma organizada seguimos um protocolo HTTP e um formato especifico de texto.