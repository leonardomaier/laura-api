# API Laura


## Começando
Essas instruções farão com que você tenha uma cópia do projeto em execução na sua máquina local para fins de teste.

## Pré-requisitos

Para continuar é necessário ter instalado os seguintes requisitos:

- Python 3.8.5

Primeiramente clone o projeto usando o seguinte comando:

```git
git clone https://github.com/leonardomaier/laura-api
```

Navegue até a pasta criada e lá você encontrará o arquivo .env.example onde contém todas as variáveis de ambiente necessárias para executar o projeto. Crie uma cópia desse arquivo, renomeie para .env e configure as variáveis de acordo com seu ambiente.

As variáveis abaixo estão configuradas de acordo com o valores padrões do Mongo DB:

```git
MONGO_DB_HOST=localhost
MONGO_DB_PORT=27017
MONGO_DB_DATABASE=laura_challenge
MONGO_DB_COLLECTION=estudantes
```


Após isso, execute o seguinte comando para instalar as dependências do projeto:

```git
pip install -r requirements.txt
```

Com tudo configurado, execute o comando abaixo para criar o database e popular a collection no Mongo DB:

```git
python import_data.py
```

Caso tudo tenha dado certo, você pode iniciar o servidor com o comando:

```git
python server.py
```
## Documentação da API

A documentação da API está disponível no link abaixo, caso esteja usando o Postman para testar, é só importá-la:

[Clique aqui para acessar a documentação](https://documenter.getpostman.com/view/2227148/T1LLE81Y?version=latest#80471504-f2a9-4f3f-ad33-3971f512a6a7).
