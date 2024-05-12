# Проект YaMDb
API для хранилища отзывов пользователей на произведения (учебный проект).

### Авторы
Евгений Москалянов 
Ксения Иванова
Сергей Филатов

### Технологии
Python 3.9,
Django 3.2.16,
Django REST Framework 4.7.2

### Запуск проекта в dev-режиме
Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/eugemos/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

* Если у вас Linux/macOS

    ```
    source env/bin/activate
    ```

* Если у вас windows

    ```
    source env/scripts/activate
    ```

Обновить утилиту pip:

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Перейти в папку yatube_api

```
cd api_yamdb
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

### Использование
Документацию к API можно посмотреть в браузере по адресу http://127.0.0.1:8000/redoc/

Для обращения к эндпойнтам API следует использовать утилиту для обмена данными
по протоколу HTTP.
Например, **postman** https://www.postman.com
