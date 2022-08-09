# 28 App e Web Server

## 5. Configurando o APP Server Gunicorn

O primeiro passo é instalar o gunicorn na venv

```bash
~/.venv/bin/python -m pip install gunicorn
```

**aguarde**

Agora vamos testar se o gunicorn consegue servir nosso app Django

```bash
cd /app
export PYTHONPATH=/app/python-web-api/exemplos/day2/django/
export DJANGO_SETTINGS_MODULE=djblog.settings
export BLOG_ENV=production

~/.venv/bin/gunicorn --bind 0.0.0.0:8000 djblog.wsgi
```
```
[2022-08-04 18:12:23 +0000] [77618] [INFO] Starting gunicorn 20.1.0
[2022-08-04 18:12:23 +0000] [77618] [INFO] Listening at: http://0.0.0.0:8000 (77618)
[2022-08-04 18:12:23 +0000] [77618] [INFO] Using worker: sync
[2022-08-04 18:12:23 +0000] [77619] [INFO] Booting worker with pid: 77619
```

Acesse para ver se está tudo funcionando corretamente http://192.168.1.100:8000/

Ok, se funcionou está tudo certo, agora precisamos fazer com que o **gunicorn** execute como um serviço do sistema operacional e para isso usaremos o **systemd**

**Ctrl + C** e agora vamos criar um **socket** para o gunicorn.

```bash
sudo nano /etc/systemd/system/gunicorn.socket
```

Cole o seguinte conteúdo

```ini
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
```

Próximo passo é criar um serviço com nossa app


```bash
sudo nano /etc/systemd/system/gunicorn.service
```
cole o seguinte conteúdo

> **ATENÇÃO** Substititua `osboxes` pelo usuário da sua VM caso a sua VM tenha um usuário diferente
> isto é importante pois este serviço será executado por este usuário.

```ini
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
Environment=PYTHONPATH=/app/python-web-api/exemplos/day2/django/
Environment=DJANGO_SETTINGS_MODULE=djblog.settings
Environment=BLOG_ENV=production
User=osboxes
Group=www-data
WorkingDirectory=/app
ExecStart=/home/osboxes/.venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          djblog.wsgi

[Install]
WantedBy=multi-user.target
```

Agora vamos ativar os serviços

```bash
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket
sudo systemctl status gunicorn.socket
sudo systemctl status gunicorn
```

A mansagem deve conter

```bash
Active: active (running)
```

Se por acaso não tiver iniciado podemos usar

```bash
sudo systemctl daemon-reload
sudo systemctl restart gunicorn
sudo systemctl status gunicorn
```

O gunicorn está servindo em um **socket** portanto não temos uma porta TCP para 
acessar como tinhamos antes mas podemos verificar se o socket está ativo com: 

```bash
ss -l | grep gunicorn
```
```
u_str LISTEN 0  2048  /run/gunicorn.sock 32549   * 0   
```

Agora precisamos de um proxy que mapeie uma porta HTTP a este socket.

## 6. Configurando o WEB Server NGINX

Primeiro apagamos a config default que já vem com o nginx

```bash 
sudo rm -rf /etc/nginx/sites-enabled/default 
```

Agora criamos nossa config:

```bash
sudo nano /etc/nginx/sites-available/blog
```

Cole o seguinte conteúdo

```conf
server {
    listen 80 default_server;
    listen [::]:80 default_server;

    server_name _;

    location = /favicon.ico { access_log off; log_not_found off; }

    location /static/ {
        autoindex on;
        alias /app/static/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
```

Agora ativamos o site no nginx

```bash
sudo ln -s /etc/nginx/sites-available/blog /etc/nginx/sites-enabled
```

Verificamos se está tudo certo com a config

```bash
sudo nginx -t
```
```
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
```

Reiniciamos

```bash
sudo systemctl restart nginx
```

Agora acessamos http://192.168.1.100/ e experimente o /admin.
