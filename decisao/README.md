### Modo de uso API's


#### Geral

Para ambas é necessário rodar os seguintes comandos para o funcionamento correto do código:

``` bash
docker-compose build
docker-compose up
```

Atualmente são necessários os seguintes campos para a obtenção de um resultado:

 - taxa\_de\_sucesso        : número de respostas corretas / número total de respostas;
 - velocidade\_de\_resposta : número de respostas / tempo total;
 - npower                   : quantidade de power up's utilizados;
 - level                    : nível da fase;


##### Métodos
    
    GET
- Padrão    : Retorna todos os registros do banco;
- ID        : Id correspondente ao registro de interesse;

    POST    
- Padrão    : Adiciona o json atribuído ao banco;


    PREDICT 
- Padrão    : Utiliza o json atribuído para fazer a predição;
- ID        : Realiza a predição usando um dos registros do banco, caso ID = 0, faz a predição de todos os dados presentes no banco;

#### Cluster

Utiliza a port 3310 para comunicação externa.

#### Predict 

Utiliza a port 3308 para comunicação externa.
