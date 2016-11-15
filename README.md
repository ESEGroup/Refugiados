# ProjetoX9
Projeto para a disciplina Engenharia de Software da UFRJ (2016.2)

# Instalar (necessário python3, pip3, recomendado dentro de uma virtualenv)

## Para instalar os requerimentos execute (dentro da virtualenv)

`pip3 install -r requirements.txt`

## Após isso é necessário configurar o servidor
Mova config.py.example da pasta **projetox9** para config.py e configure corretamente com as informações do banco e chaves de API.

## Rodar o servidor
Entre na pasta **projetox9** e execute:
    *nix:
`        env FLASK_APP=server.py flask run`
    Windows:
`        export FLASK_APP=server.py flask run`
