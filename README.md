<img src="https://www.laura-br.com/wp-content/themes/Laura/images/logo.png" height="100"/>

# API Laura


## Começando
Essas instruções farão com que você tenha uma cópia do projeto em execução na sua máquina local para fins de desenvolvimento e teste.

## Pré-requisitos

Primeiramente clone o projeto usando o seguinte comando:

```git
git clone https://github.com/leonardomaier/laura-api
```

Navegue até a pasta criada e lá você encontrará o arquivo .env.example onde contém todas as variáveis de ambiente necessárias para executar o projeto. Crie uma cópia desse arquivo, renomeie para .env e configure as variáveis de acordo com seu ambiente.

As variáveis abaixo configuradas de acordo com o padrão do Mongo DB

```git
MONGO_DB_HOST=localhost
MONGO_DB_PORT=27017
MONGO_DB_DATABASE=laura_challenge
MONGO_DB_COLLECTION=estudantes
```


Após isso, rode o seguinte comando para instalar as dependências do projeto:

```git
pip install -r requirements.txt
```

Com tudo configurado, rode o comando abaixo para criar o database e popular a collection no Mongo DB:

```git
python import_data.py
```

Caso dê mensagem de sucesso, inicie o servidor com o comando:

```git
python server.py
```
## Documentação da API

A documentação da API está disponível no link abaixo, caso esteja usando o Postman para testar, é só importá-la:

[Clique aqui para acessar a documentaçãoI](https://documenter.getpostman.com/view/2227148/T1LLE81Y?version=latest#80471504-f2a9-4f3f-ad33-3971f512a6a7).
