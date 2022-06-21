# Os frameworks

Como vimos no Day1 para criar um framework basta utilizarmos os recursos da linguagem Python aliados aos protocolo e os padrões web, especialmente HTTP e WSGI, é uma tarefa bastante divertida, criar seu próprio framework do zero te dá um poder e controle que são realmente incríveis.

Mas ao mesmo tempo criar as coisas do zero traz uma responsabilidade e trabalho imenso até que tudo fique de acordo com o esperado, e a maioria das soluções e testes que você vai precisar fazer com certeza já foram feitos por dezenas de outras pessoas e com a cultura de software open-source podemos simplesmente utilizar o que já existe, estender, contribuir e construir aplicações web baseadas em plataformas sólidas.

Vamos agora conhecer os principais frameworks web para Python.

## Tipos de frameworks

Existem vários frameworks web baseados na linguagem Python, todos focados no backend, e cada um com suas carecteristicas e limitações, os frameworks estão divididos em 2 categorias:

- Micro Frameworks
    - Pequenos frameworks que tomam poucas (ou nenhuma) decisões por vocÊ, são leves e oferecem flexibilidade para você arquitetar o software da maneira que preferir.
        - PRO: Leve, simples, flexivel, fácil de entender e debugar
        - CON: Exige que você tome decisões de arquitetura e crie soluções do zero.
- Full Stack Frameworks
    - Framework completo que toma a maior parte das decisões e pretende encapsular a soluções para a maioria dos seus problemas.
        PRO: Já possui modelos e padrões para resolver os principais problemas
        CON: Pesado, carrega mais features que as que você vai utilizar, pouco flexivel e altamente acoplado.

## Os principais frameworks do ecossistema Python

Eu já devo ter trabalhado com uns 15 frameworks em Python, para listar alguns: Zope, Plone, web.py, Pylons, Turbogears, Repoze, Pyramid, web2py, Tornado, Django, Flask, Sanic, Bottle, Chalice, Falcon, Hug, FastAPI.

Durante 4 anos atuei como uns dos core-developers e co-criador do web2py e foi durante esta prática que aprendi muito sobre web com Python.

Hoje em dia, durante a produção deste treinamento o mercado de frameworks Python se estabeleceu em 4 frameworks.

- Django
    - Framework Full Stack, focado em gestão de conteúdo (blogs, lojas, portais), bastante acoplado a bancos de dados SQL e utilizado por empresas como Instagram, Spotify, Pinterest, Disqus
- Flask
    - Micro Framework para sites e APIs, permite maior flexibilidade e não é acoplado a nenhum sistema de banco de dados sendo bastante utilizado com NOSQL e é utilizado em empresas como Uber, Netflix, Lyft, Airbnb, Patreon, Trivago.
- FastAPI
    - Micro framework com foco em APIs e micro serviços, utiliza funções assincronas e anotação de tipos e é usado por empresas como Microsoft, Soudcloud, Infinity e é um dos mais promissores frameworks para Python no momento.

Neste treinamento veremos os 3 frameworks para que você tenha conhecimento para trabalhar com as principais aplicações e concorrer a vagas em qualquer empresa web que utilize Python.

## Qual framework é o melhor?

Esta pergunta é bastante comum, e levando em consideração que nos últimos 20 anos ninguém conseguiu responder esta pergunta, podemos concluir que TODOS são melhores, cada um em seu nicho e objetivo especifico.

Ao escolher um framework não podemos analisar apenas os quesitos técnicos, precisamos colocar na equação as necessidades do negócio, o tamanho do time e o tipo de produto que iremos desenvolver.

Para 90% dos softwares web, qualquer um dos 3 frameworks será ótimo e a escolha será baseada em gosto e no conhecimento que você e seu time já possuem.

E em 10% dos casos sempre teremos aquelas soluções especificas onde um framework se sobressai.

Vamos agora explorar cada um deles para que você tenha discernimento quando precisar tomar a decisão de qual deles escolher.

Em cada um dos exemplos que vamos desenvolver eu vou focar nas principais features de cada um dos frameworks e durante o desenvolvimento vou comentar a respeito das partes ruins deles também.

Nós vamos começar com Flask que é o mais simples e o que mais se assemelha ao framework que fizemos no Day 1, depois veremos o Django que é o principal e mais utilizado hoje em dia na maior parte das empresas.

Depois vamos ter um espaço mais dedicado ao FastAPI, pois é o mais moderno e com certeza o mais promissor e que já se coloca como a melhor escolha em qualquer cenário para o futuro do Python.
