# YaMDb

## Описание проекта

Проект `YaMDb` собирает различные произведения (фильмы, книги, музыка) и отзывы пользователей на них.
Произведения можно найти по категориям и жанрам. В финальной версии проекта настроены также Continuous Integration и Continuous Deployment:
* автоматический запуск тестов,
* обновление образов на Docker Hub,
* автоматический деплой на боевой сервер при пуше в главную ветку main,
* отправка сообщения телеграм-боту об успешном выполнении.

## Технологии

* Python 3.8.5

* Django 3.0.5

* Django Rest Framework 3.11.0

* Django Rest Framework Simple JWT 4.3.0

* Postgres 12.4

* Gunicorn 20.0.4

* Psycopg2-binary 2.8.6

* Nginx 1.19.3

* Docker 20.10.8

* docker-compose 1.29.2


## Установка

* Клонировать этот репозиторий:

    ```bash
    git clone https://github.com/elenashipkova/infra_sp2.git
    ```

* Создать в корне проекта файл .env с константами:

    ```text
    DB_ENGINE=django.db.backends.postgresql
    DB_NAME=postgres
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=postgres   # пароль для подключения к БД (установите свой)
    DB_HOST=db   # название сервиса (контейнера)
    DB_PORT=5432   # порт для подключения к БД
    ```

* Запуск на основе контейнеров Docker (выполнить в терминале в директории проекта):
    
    ```bash
    docker-compose up -d --build
    ```

* Применить миграции:

    ```bash
    docker-compose exec web python3 manage.py migrate --noinput
    ```

* Создать суперпользователя:
    
    ```bash
    docker-compose exec web python3 manage.py createsuperuser
    ```

* Заполнить базу данных:

    ```bash
    docker-compose exec web python3 manage.py loaddata fixtures.json
    ```


**Полная документация по API доступна здесь** _http://127.0.0.1/redoc/_

## Бейдж

![master](https://github.com/elenashipkova/yamdb_final/workflows/yamdb_workflow.yml/badge.svg)


## Автор

* Елена Шипкова
