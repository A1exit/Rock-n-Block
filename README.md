### Rock-n-Block

[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)

#### О проекте
Rock-n-Block - бэкенд-сервис, который взаимодействует с контрактом стандарта ERC-721 в блокчейне Ethereum.

Суть сервиса заключается в том, чтобы производить операции с NFT-токеном, используя REST API. В таком сервисе одна операция на получение информации из блокчейна и ее выдачу в API-ответе, и одна операция, результат которой будет изменять состояние смарт-контракта.

#### Стек реализации:
* Язык: Python 3.9
* Web framework: Django 3.2.12 & DRF 3.13.1
* Database: PostgreSQL
* Blockchain framework: Web3.py
* Blockchain: Ethereum (Rinkeby Testnet)

#### Доступные эндпоинты:

```
/tokens/create
```
Метод запроса: POST

API создает новый уникальный токен в блокчейне и записывать параметры запроса в БД.

Запрос должен принимать:
- media_url - урл с произвольным изображением
- owner - Ethereum-адрес будущего владельца токена

```
/tokens/list
```
Метод запроса: GET

API выдает список всех обьектов модели Token

```
/tokens/total_supply
```
Метод запроса: GET

API обращается к контракту в блокчейне и выдает в ответе информацию о текущем Total supply токена - общем числе находящихся токенов в сети.

Что бы протестировать приложение необходимо:

* клонировать репозиторий
* создать файл .env и вставить в него переменные и добавить к ним необходимые значения
```
SECRET_KEY=
DB_ENGINE=
DB_NAME=
POSTGRES_USER=
POSTGRES_PASSWORD=
DB_HOST=
DB_PORT=
CONTRACT_ADDRESS=
INFURA_KEY=
PRIVATE_KEY=
METAMASK_KEY=
```
* в терминале ввести xcode-select --install, если не устанавливается библиотека web3
* перейти в директорию с файлом docker-compose.yaml
* ввести в терминале: 
```
docker-compose up -d --build
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --no-input 
```

#### Aвтор:

Алексей Останин