# ProjetoX9
Projeto para a disciplina Engenharia de Software da UFRJ (2016.2)

## Instalar: 
*(Necessário python3, pip3, é recomendado executar dentro de uma virtualenv)*

### Para instalar os requerimentos execute 

`pip3 install -r requirements.txt`

### Após isso é necessário configurar o servidor
Renomeie config.py.example para config.py e configure corretamente com as informações do banco de dados e a chave da API do Google Maps.

### Rodar o servidor
Linux:

`env FLASK_APP=projetox9/server.py flask run`
    
Windows:

`export FLASK_APP=projetox9/server.py flask run`
