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

O processo de deploy delas é praticamente o mesmo, desde que a gente aponte o servidor de aplicação **gunicorn** para a função WSGI o funcionamento será o mesmo.


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

Então vamos atualizar o `pip` 

```bash
~/.venv/bin/python -m pip install --upgrade pip
``` 

> **atenção** a atualização do pip pode demorar alguns minutos na primeira execução.

## 3. Obtendo os arquivos do projeto via git

Agora vamos obter o código da aplicação atrav;es do git, você pode usar meu repositório se quiser ou utilizar a sua cópia do repositório para fazer deploy da app que você desenvolveu.

```bash
cd
git clone -b day2 https://github.com/rochacbruno/python-web-api

cd python-web-api
ls exemplos/day2/django
```
```
blog  djblog  manage.py  setup.py  templates
```

## 4. Instalando o Projeto

Agora que o projeto já está clonado podemos instalar na virtualenv

```bash
cd
~/.venv/bin/python -m pip install python-web-api/exemplos/day2/django/
```

O comando pode demorar alguns minutos e a saida

```
~/.venv/bin/python -m pip install python-web-api/exemplos/day2/django/
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

Package     Version
----------- -------
asgiref     3.5.2
Django      4.1
django-blog 0.1.0   # <-- IMPORTANT -->
pip         22.2.2
setuptools  59.6.0
sqlparse    0.4.2
```

## 5. Configurações iniciais

Agora vamos inicializar a nossa aplicação Django e fazer um pequeno teste para ver se tudo está funcionando.

```
$ export DJANGO_SETTINGS_MODULE=djblog.settings
```

```
$ ~/.venv/bin/django-admin --help

Type 'django-admin help <subcommand>' for help on a specific subcommand.

Available subcommands:

[auth]
    changepassword
    createsuperuser
...
```

Agora inicializamos o banco de dados com o comando `migrate`

```bash
~/.venv/bin/django-admin migrate --noinput

Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions
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
  Applying sessions.0001_initial... OK
```

E criamos um superuser

```bash
$ ~/.venv/bin/django-admin createsuperuser --username admin --email admin@example.com

Password: 
Password (again): 
The password is too similar to the username.
This password is too short. It must contain at least 8 characters.
This password is too common.
Bypass password validation and create user anyway? [y/N]: y
Superuser created successfully.
```

Executando uma vez no modo standalone para testar

```
~/.venv/bin/django-admin runserver 0.0.0.0:8000

Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
August 04, 2022 - 16:27:35
Django version 4.1, using settings 'djblog.settings'
Starting development server at http://0.0.0.0:8000/
Quit the server with CONTROL-C.
```

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

No Django os settings ficam no arquivo `settings.py` então em teoria poderiamos abrir este arquivo e alterar as chaves de configuração, porém não é recomendado alterar código diretamente no servidor e além disso é recomendado seguirmos o **12factorapp** guide https://12factor.net/pt_br/config que recomenda que as configurações pertençam ao ambiente.

O Django por default não carrega as variáveis de ambiente, portanto usaremos a biblioteca Dynaconf.


### Adicionando Dynaconf ao projeto.

As alterações a seguir já foram implementadas e você pode obter no server diretamente com os seguintes comandos:

```bash
cd

```

#### Alterando manualmente nos arquivos

`setup.py`
```python

```



## 6. Configurando o APP Server Gunicorn

## 7. Configurando o WEB Server NGINX
