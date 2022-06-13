# carregar os dados
dados = [
    {"nome": "Bruno", "cidade": "Viana"},
    {"nome": "Guido", "cidade": "Amsterdan"}
]

# processar
template = """\
<html>
<body>
    <ul>
        <li> Nome: {dados[nome]} </li>
        <li> Cidade: {dados[cidade]} </li>
    </ul>
</body>
</html>
"""

# renderizar

for item in dados:
    print(template.format(dados=item))
