# HTTP Server

Ao invés de acessarmos diretamente o recurso que está no sistema de arquivos. ex: páginas HTML, precisamos da figura do HTTP server, ou web server, que vai servir de intermédio e garantir qua o acesso seja principalmente controlado, pois não queremos expor todos os arquivos para a web.


## Criando um server com socket

Da mesma maneira que criamos um client com socket podemos também abrir um socket do lado servidor

`server.py`
```python
import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 9000))
server.listen()

try:
    while True:
        client, address = server.accept()
        data = client.recv(5000).decode()
        print(data)

        client.sendall(
            "HTTP/1.0 200 OK\r\n<html><body>Hello World</body></html>\r\n\r\n".encode()
        )
        client.shutdown(socket.SHUT_WR)
except:
    server.close()
```
```
python server.py
```


Agora em outro terminal podemos rodar nosso client para se conectar a este server:


`http_client.py`
```python
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 9000))
cmd = "GET http://example.com/index.html HTTP/1.0\r\n\r\n".encode()
client.send(cmd)

while True:
    data = client.recv(512)
    if len(data) < 1:
        break
    print(data.decode(), end="")

client.close()
```
```
python http_client.py
```

Felizmente não precisamos criar servidores usando `socket` diretamente pois Python já oferece algumas abstrações como veremos a seguir.


## Python builtin server

O Python já tem um servidor HTTP integrado que é capaz de servir contéudo estático de qualquer diretório.

Na pasta onde o arquivo `pagina.html` está localizado:

```bash
python -m http.server
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/)
```

Ao abrir no navegador http://0.0.0.0:8000

No navegador:

```
Directory listing for /

    estilo.css
    pagina.html
    script.js
```

No terminal verá:

```bash
10.20.1.2 - - [09/May/2022 18:10:16] "GET / HTTP/1.1" 200 -
10.20.1.2 - - [09/May/2022 18:10:16] "GET /favicon.ico HTTP/1.1" 404 -
```

Ao clicar para acessar http://0.0.0.0:8000/pagina.html

No terminal verá
```bash
0.20.1.2 - - [09/May/2022 18:12:31] "GET /pagina.html HTTP/1.1" 200 -
10.20.1.2 - - [09/May/2022 18:12:31] "GET /estilo.css HTTP/1.1" 200 -
10.20.1.2 - - [09/May/2022 18:12:31] "GET /script.js HTTP/1.1" 200 -
```

As duas grandes vantagens de servir o conteúdo utilizando um servidor `HTTP` são:

- Expor apenas o conteúdo que desejar
- Obter log de acessos

## Outros servidores

Um dos principais servidores do mercado é o `Nginx` (Engine X) e ele é mais seguro e mais performático do que o servidor builtin do Python, porém é recomendado apenas para ambiente de produção.

É possivel rodar o nginx usando containers

```
sudo docker run --name docker-nginx -p 8000:80 -d -v $PWD:/usr/share/nginx/html nginx
```

E então acessar http://0.0.0.0:8000 

No navegador verá:
```bash
403 Forbidden
nginx/1.21.6
```

O Nginx não expoe os arquivos todos do sistema de arquivos e além disso
pode ser configurado para efetuar outros controles como por exemplo o controle de acesso por rede privada, senha, limitações de acesso etc...

Ao adicionar http://0.0.0.0:8000/pagina.html ao final da url o site funciona normalmente.


## Conclusão

Até aqui estamos servindo o que chamamos de arquivos estáticos, `html`, `css`, `js` e `imagens`, repare que não existe programação envolvida no lado servidor, o JS é computado apenas quando o conteúdo já está entregue ao navegador.

Agora vamos finalmente ao Python :)
