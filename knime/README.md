# flaskdb-knime

MYSQL db - docker
knime

## Requisitos

Para a inserção automática do backup no mysql é necessário:
    um diretório "dump" ao lado de docker-compose.yml, que possua o backup.sql 

```bash
mkdir dump
cp ~/caminho/backup.sql ./dump/.
```

Baixe o Knime em: https://www.knime.com/downloads

Certifique que as portas (3306 e 3307) estão livres, umas vez que são utilizadas para a conexão docker (db) - knime

Também é necessário um arquivo ".env" com as seguintes informações:
- MYSQL_HOST=seu_host
- MYSQL_ROOT_PASSWORD=sua_senha
- MYSQL_DATABASE=seu_db

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

