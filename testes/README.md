# mysql-flaskdb
REST API - Docker
python - flask

## Requisitos

Para Linux:
```bash
sudo docker-compose build

```
Para Windows:
```bash
docker-compose build
```

Certifique que as portas (3000, 5000, 3307 e 3306) estejam livres, uma vez que essas são utilizadas pelo docker para fazer a conexão.


Também é necessário um arquivo ".env" com as seguintes informações:
- MYSQL_HOST=seu_host
- MYSQL_ROOT_PASSWORD=sua_senha
- MYSQL_DATABASE=seu_db

Para utilizar o docker, é necessário que:
- MYSQL_HOST=db
- a porta a ser utilizada deve ser: 3000

## Como Usar
No seu terminal, rode:

Para Linux:
```bash
sudo docker-compose up
```
Para Windows:
```bash
docker-compose up
```

Utilize um Postman, seguindo as instruções abaixo:

- configure a função desejada;
- caso necessário, configure o body (raw, JSON);
- utilize a seguinte URL: http://localhost:3000/api

Caso prefira usar um terminal para fazer as requisições, utilize:

```bash
curl -X [FUNÇÃO] -H 'Content-Type: application/json' -d \'[DADOS]\' http://localhost:3000/api
```

FUNÇÃO:
- GET, GET (id)
- POST
- PUT (id)
- DELETE (id)

DADOS, exemplo:
(seguindo os atributos de cada tipo de mensagem)

- {
    "message_type": "PlayGameMessage",
    "time": 40,
    "id_jogador": 2,
    "gameID": 100,
    "resourceID": 3,
    "timeType": 32
}
