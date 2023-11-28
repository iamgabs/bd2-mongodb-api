## GABRIEL CARVALHO

> API DISPONÍVEL ATÉ O DIA 02/12/2023

link http://34.133.167.201/

banco de dados = mongodb

servidor = nginx

backend = python/flask

cloud = google cloud platform


rotas => 

cadastrar = /register

pegar um usuário = /user=?username=

pegar todos os usuários / users

atualizar /user

deletar /user/id

exemplo de objeto:
{
    "name": "",
    "age": 0,
    "nacionality": "",
    "username": "",
    "password": ""
}

## Executar no windows => 
~~~bash
python -m venv venv

./venv/Scripts/activate

pip install ./requirements.txt

python ./app.py
~~~


## Executar no mac/linux => 
~~~bash
python3 -m venv venv

source ./venv/bin/activate

pip3 install ./requirements.txt

python3 ./app.py
~~~
