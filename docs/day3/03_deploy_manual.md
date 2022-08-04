# 26 Deploy Manual

Apartir daqui eu vou assumir que você tem acesso a uma Máquina Virtual Ubuntu Server 22.04 e consegue acessar a VM via SSH a apartir do seu terminal.

Essa VM pode estar rodando no VirtualBox, em um outro sustema de virtualização de sua preferencia, ou em um provedor de VPS como DigitalOcean, AWS, etc.


Vamos ao deploy manual da nossa aplicação, no momento nós temos 4 versões da aplicações web **blog** desenvolvidas.

- Uma que criamos com Python Puro e Jinja
  `exemplos/day1/blog_jinja_blocks`

- Uma que criamos com o nosso próprio framework
  `exemplos/day1/blog_framework`

- Uma que criamos com Flask
  `exemplos/day2/flask`

- A que acabamos de criar com Django
`exemplos/day2/django`


Todas essas aplicações tem uma coisa em comum: **Todas implementam o protocolo WSGI.**

O processo de deploy delas é praticamente o mesmo, desde que a gente aponte o servidor de aplicação **gunicorn** ou **uvicorn** para a função WSGI ou ASGI o funcionamento será o mesmo.


Para este exemplo vamos começar usando a última que fizemos em Django e depois você pode experimentar trocar na configuração para servir as outras opções.


## 0. Conectando via SSH

Conecte a VM usando um terminal e SSH

```bash
ssh user@IP
```
exemplo

```bash
ssh osboxes@192.168.1.100
```

Se tiver configurado a chave SSH não irá precisar de user e senha, caso contrário forneça a senha do usuário.

## 1. Instalando os softwares requeridos

Vamos usar o gerenciador de pacotes do Ubuntu para garantir que todos os pacotes estão instalados.

```bash
sudo apt-get install -y python3-dev python-is-python3 nginx git sqlite3 python3.10-venv
```

> Se encontrar uma mensagem de erro relacionada a `initramfs` pode ignorar por enquanto.

## 2. Criando um ambiente virtual

O ambiente virtual Python que usaremos será criado na pasta do seu usuário atual portando digite:

```bash
cd
python3 -m venv .venv
```

Isso irá criar a pasta `~/.venv` digite `ls ~/.venv` só para verificar.

Aqui nós não iremos ativar a virtualenv, em ambientes de produção ao invés de ativar a venv nós sempre executamos usando o caminho completo.

```bash
~/.venv/bin/python -V
```
```
Python 3.10.4
```

> **DICA** ao invés de usar `~/.venv/bin/python` é recomendado sempre usar o caminho absoluto `/home/osboxes/.venv/bin/python`, para executar manualmente é repetivivo, mas lembre-se que vamos colocar esse comando em um script em breve.

Vamos começar atualizando a versão do `pip`  na virtualenv recém criada.

```bash
~/.venv/bin/python -m pip install --upgrade pip
``` 

> **atenção** a atualização do pip pode demorar alguns minutos na primeira execução.

## 3. Obtendo os arquivos do projeto via git


Vamos primeiro criar a pasta onde o aplivativo será armazenado, ao invés de fazer isso na pasta home `~/` como fizemos com a venv, eu recomendo criar
esta pasta na raiz da VM pois depois podemos seguir o mesmo procedimento ao executar
em containers e desta forma fica mais fácil de dar permissões ao web server para servir os arquivos estáticos.

```bash
sudo mkdir /app
```

Ajustar as permissões da pasta `/app`

Primeiro vamos determinar que esta pasta pertence ao grupo `www-data` que é o grupo do usuário que executa o servidor web `nginx`.

```bash
sudo chgrp www-data /app
sudo chmod g+rwxs /app
```

Agora adicionamos o nosso usuário atual ao grupo `www-data`, execute o comando `usermod` com `-a -G` (adicionar ao Grupo) `www-data` (grupo) `$USER` (user atual)

```bash
sudo usermod -a -G www-data $USER
```

Reload dos grupos do usuário corrente

```bash
$ su - $USER
$ groups
... www-data ...
```

Agora vamos obter o código da aplicação através do git, você pode usar meu repositório se quiser ou utilizar a sua cópia do repositório para fazer deploy da app que você desenvolveu.

> **ATENÇÃO** daqui para frente a pasta `/app` será sempre nosso working directory.

```bash
cd /app
git clone -b day2 https://github.com/rochacbruno/python-web-api
```

```bash
cd python-web-api
ls exemplos/day2/django
```
```
blog  djblog  manage.py  setup.py  templates
```

## 4. Instalando o Projeto

Agora que o projeto já está clonado podemos instalar na virtualenv

```bash
cd /app
~/.venv/bin/python -m pip install /app/python-web-api/exemplos/day2/django/
```

O comando pode demorar alguns minutos e a saida

```bash
~/.venv/bin/python -m pip install /app/python-web-api/exemplos/day2/django/
```
```
Processing ./python-web-api/exemplos/day2/django
  Preparing metadata (setup.py) ... done
Collecting django
  Downloading Django-4.1-py3-none-any.whl (8.1 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 8.1/8.1 MB 16.0 MB/s eta 0:00:00
Collecting sqlparse>=0.2.2
  Downloading sqlparse-0.4.2-py3-none-any.whl (42 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 42.3/42.3 kB 6.5 MB/s eta 0:00:00
Collecting asgiref<4,>=3.5.2
  Downloading asgiref-3.5.2-py3-none-any.whl (22 kB)
Using legacy 'setup.py install' for django-blog, since package 'wheel' is not installed.
Installing collected packages: sqlparse, asgiref, django, django-blog
  Running setup.py install for django-blog ... done
Successfully installed asgiref-3.5.2 django-4.1 django-blog-0.1.0 sqlparse-0.4.2

```

Agora certifique-se de que está tudo instalado.

```bash
~/.venv/bin/python -m pip list
```
```
Package     Version
----------- -------
asgiref     3.5.2
Django      4.1
django-blog 0.1.0   # <-- IMPORTANT -->
pip         22.2.2
setuptools  59.6.0
sqlparse    0.4.2
...
```

## 5. Configurações iniciais

Agora vamos inicializar a nossa aplicação Django e fazer um pequeno teste para ver se tudo está funcionando.

Essas 2 variáveis de ambiente sempre serão requeridas.

```bash
export PYTHONPATH=/app/python-web-api/exemplos/day2/django/
export DJANGO_SETTINGS_MODULE=djblog.settings
```

```bash
$ ~/.venv/bin/django-admin --help
```
```
Type 'django-admin help <subcommand>' for help on a specific subcommand.

Available subcommands:

[auth]
    changepassword
    createsuperuser

[blog]
    add_post
...
```

Executando uma vez no modo standalone só para testar

```bash
~/.venv/bin/django-admin runserver 0.0.0.0:8000
```
```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).

You have 19 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, blog, contenttypes, sessions.
Run 'python manage.py migrate' to apply them.

August 04, 2022 - 16:27:35
Django version 4.1, using settings 'djblog.settings'
Starting development server at http://0.0.0.0:8000/
Quit the server with CONTROL-C.
```

> **Atenção**: IGNORE A mensagem a respeito das 19 migrations não aplicadas por enquanto.

Agora abra o seu navegador e tente acessar http://192.168.1.100:8000/ (altere para o IP da sua VM se preciso)

Você vai reparar uma mensagem de erro.

```
DisallowedHost at /

Invalid HTTP_HOST header: '192.168.1.100:8000'. You may need to add '192.168.1.100' to ALLOWED_HOSTS.
```

A própria mensagem já nos dá a dica do que fazer para resolver, precisamos adicionar a cofniguração `ALLOWED_HOSTS` os endereços pelo qual o Django é autorizado a servir, esta é uma config de segurança e nós podemos colocar lá o IP completo como a mensagem recomenda ou podemos simplesmente colocar `"*"` para permitir qualquer host.

Ao fazer scroll pela página de erro você vai ser capaz de ver as chaves de configuração do projeto

![](imgs/django_debug.png)

E isso não é desejavel, estamos fazendo deploy em um servidor de produção, não podemos expor variáveis de modo debug, parece que remos agora 2 variáveis de configuração para alterar.

```python
DEBUG=False
ALLOWED_HOSTS=["*"]
```

No Django os settings ficam no arquivo `settings.py` então em teoria poderiamos abrir este arquivo e alterar as chaves de configuração, porém **não é recomendado alterar código diretamente no servidor** e além disso é recomendado seguirmos o **12factorapp** guide https://12factor.net/pt_br/config que recomenda que as configurações pertençam ao ambiente.

O Django por default não carrega as variáveis de ambiente, portanto usaremos a biblioteca [Dynaconf](https://dynaconf.com).

### Adicionando Dynaconf ao projeto.

As alterações a seguir já foram implementadas e você pode obter no server diretamente com os seguintes comandos:

```bash
cd /app/python-web-api
git fetch --all
git checkout day3
git pull --rebase
git branch
```

Agora seu projeto estará na branch day3, se preferir pode também fazer manualmente com as instruções a seguir.

#### (opcional) Alterando manualmente nos arquivos

`/app/python-web-api/exemplos/day2/django/setup.py`
```python
from setuptools import setup

setup(
    name="django_blog",
    version="0.1.0",
    packages=["djblog", "blog", "templates"],  # NEW
    include_package_data=True,  # NEW
    install_requires=[
        "django",
        "django-markdownify",
        "django-extensions",
        "dynaconf",  # NEW
    ],
)
```

Adicione um arquivo MANIFEST para incluirmos os templates junto ao build.

```bash
echo "recursive-include templates *.html" > exemplos/day2/django/MANIFEST.in
```

Altere o `djblog/settings.py`
```python
# No final do arquivo
from dynaconf import DjangoDynaconf  # noqa

settings = DjangoDynaconf(
    __name__,
    load_dotenv=False,
    envvar_prefix='BLOG',
    env_switcher="BLOG_ENV",
    settings_files=["blog_settings.toml"]
)
```

Agora o projeto está pronto para ser configurado de maneira dinâmica através de variáveis de ambiente ou arquivo opcional local `blog_settings.toml`


### Reinstale

**IMPORTANTE** Reinstale pois não estamos em modo editável.

Apague o build anterior caso exista

```bash
rm -rf exemplos/day2/django/build/
rm -rf exemplos/day2/django/django_blog.egg-info/
```

Resinstale

```bash
~/.venv/bin/python -m pip install /app/python-web-api/exemplos/day2/django/
```

> Em VM pode demorar um pouco o download dos pacotes.

## 6. Configuração local de deploy

O Dynaconf permite de duas maneiras

1. Environment

```bash
cd /app
export PYTHONPATH=/app/python-web-api/exemplos/day2/django/
export DJANGO_SETTINGS_MODULE=djblog.settings
export BLOG_DEBUG=false
export BLOG_DATABASES__default__NAME="/app/db.sqlite3"
export BLOG_ALLOWED_HOSTS='["*"]'
```

2. Ou com arquivo local `/app/blog_settings.toml`

Primeiro limpe as variáveis de ambiente prefixadas com `BLOG_` caso tenha testado com elas

```bash
unset BLOG_ALLOWED_HOSTS 
unset BLOG_DEBUG
unset BLOG_DATABASES__default__NAME
```

crie o arquivo `/app/blog_settings.toml` no servidor

> Dica: `nano /app/blog_settings.toml` e cole o conteúdo abaixo.

```toml
[production]
allowed_hosts = ["*"]
debug = false
DATABASES__default__NAME="/app/db.sqlite3"
```

> No Nano, Salve com `Ctrl + s` e depois saia com `Ctrl + x`  
> No Vim, Salve com `:w` e saia com `:q`


## Comandos iniciais

Repare que desta vez estamos indicando um caminho para o banco de dados
portanto vamos rodar o comando `migrate` para que o banco seja criado.

```bash
cd /app
export PYTHONPATH=/app/python-web-api/exemplos/day2/django/
export DJANGO_SETTINGS_MODULE=djblog.settings
export BLOG_ENV=production
~/.venv/bin/django-admin migrate
```
```
Operations to perform:
  Apply all migrations: admin, auth, blog, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying auth.0012_alter_user_first_name_max_length... OK
  Applying blog.0001_initial... OK
  Applying sessions.0001_initial... OK
```

Repare que agora existe um arquivo `db.sqlite3`

```bash
ls /app
```
```
blog_settings.toml  db.sqlite3  python-web-api
```

Criaremos agora um super usuário.

```bash
cd /app
~/.venv/bin/django-admin createsuperuser --username admin --email admin@example.com
```
```
Password: 
Password (again): 
The password is too similar to the username.
This password is too short. It must contain at least 8 characters.
This password is too common.
Bypass password validation and create user anyway? [y/N]: y
Superuser created successfully.
```

Executando para testar

```bash
cd /app
~/.venv/bin/django-admin runserver 0.0.0.0:8000
```
```
Performing system checks...

System check identified no issues (0 silenced).
August 04, 2022 - 17:40:29
Django version 4.1, using settings ['blog_settings.toml']
Starting development server at http://0.0.0.0:8000/
Quit the server with CONTROL-C.

```

http://192.168.1.100:8000/ e verifique se tudo funcionou

Tente agora o `/admin` e faça login.

![](imgs/django_admin_no_static.png)

Repare que funciona mas a aparencia do site admin não é muito boa!

Vamos resolver, precisamos criar uma pasta para os arquivos estáticos.

**Ctrl + C** para parar o server e então

```bash
mkdir /app/static
```

Agora ecolha uma das opções:

1. Exporte as variavéis com o prefixo `BLOG_`

```bash
export BLOG_STATIC_ROOT="/app/static/"
export BLOG_STATICFILES_DIR="/app/static/"
export BLOG_STATIC_URL="/static/"
```

2. Ou adicione ao `/app/blog_settings.toml` sem o prefixo **BLOG_** (recomendado)

> `nano /app/blog_settings.toml`

```toml
STATIC_ROOT="/app/static/"
STATICFILES_DIR="/app/static/"
STATIC_URL="/static/"
```

Agora execute

```bash
cd /app
~/.venv/bin/django-admin collectstatic
```
```
135 static files copied to '/app/static'.
```

Isso faz com que o Django copie os arquivos estáticos da app admin para a pasta `static` porém ainda não será possível acessar estes arquivos, por razões de segurança e performance o Django exige que usemos um proxy reverso para servir arquivos estáticos e faremos isso brevemente.

Execute o server novamente com 

```bash
~/.venv/bin/django-admin runserver 0.0.0.0:8000
```

Acesse http://192.168.1.100:8000/new/ e adicione um post.

Pode dar **Ctrl + C** para parar o servidor no terminal pois não é o ideal que a gente deixe o servidor rodando desta maneira, o ideal é usar um servidor `WSGI` mais robusto como o gunicorn.

## 7. Configurando o APP Server Gunicorn

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

## 8. Configurando o WEB Server NGINX

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
