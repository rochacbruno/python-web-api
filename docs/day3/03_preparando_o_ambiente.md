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

### Instalando o Projeto

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
