## Описание проекта.
Данный проект поможет вам сгенерировать или создать вашу собственную короткую ссылку на любой существующий ресурс.
## Стек технологий.
Python, FastAPI, SQLite
## Автор.
https://github.com/SkullPiercer/

Клонировать репозиторий и перейти в него в командной строке:

```
git clone 
```

```
cd cat_charity_fund
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Запустить проект и создать БД:
```
uvicorn app.main:app --reload
```
Остановить сервер сочетанием клавиш Ctrl + c и выполнить миграции
```
alembic upgrade head
```
Перезапустить проект:
```
uvicorn app.main:app --reload
```