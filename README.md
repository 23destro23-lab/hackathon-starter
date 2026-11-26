## Локальный запуск тестового проекта

1. Создайте базу данных. Например, из `psql` под администратором:

```sql
CREATE DATABASE hackathon_db OWNER postgres;
```

2. Проверьте `DATABASE_URL` и укажите свои параметры PostgreSQL:

```env
DATABASE_URL=postgresql+psycopg://admin:postgres@localhost:5432/hackathon_db
```

3. Примените миграции и запустите сервер:

```bash
alembic upgrade head
uvicorn app.main:app --reload
```

Откройте http://localhost:8000.

## Загрузка БД студентов из файла excel

1. Установите дополнительные библиотеки:

```bash
pip install openpyxl, pandas
```

2. Создайте базу данных. Например, из `psql` под администратором:

```sql
create database test;
```

3. Примените миграции и запустите скрипт:

```bash
alembic upgrade head
python .\load_db\main.py
```



## Примеры API

| Метод | URL | Назначение |
|---|---|---|
| GET | `/api/items` | Получить все элементы |
| POST | `/api/items` | Создать элемент |
| GET | `/api/items/{id}` | Получить элемент |
| PATCH | `/api/items/{id}` | Обновить элемент |
| DELETE | `/api/items/{id}` | Удалить элемент |


## Как добавить свою сущность

1. Создайте модель в `app/models/event.py`, унаследовав её от `Base`.
2. Создайте Pydantic-схемы в `app/schemas/event.py`.
3. Добавьте функции доступа к данным в `app/crud/event.py`.
4. Создайте маршруты в `app/routers/events.py`.
5. Подключите router в `app/main.py`.
6. Импортируйте модель в `app/models/__init__.py`, чтобы Alembic увидел её metadata.
7. Создайте миграцию:

```bash
alembic revision --autogenerate -m "add events"
alembic upgrade head
```

8. Добавьте или измените Jinja2-шаблоны в `app/templates/`.

## Структура

```text
app/
  core/       # настройки и подключение к БД
  models/     # SQLAlchemy-модели
  schemas/    # Pydantic-схемы запросов и ответов
  crud/       # операции чтения и записи в БД
  routers/    # HTTP API и HTML-страницы
  templates/  # Jinja2-шаблоны
  static/     # CSS и JavaScript
alembic/      # миграции БД
```

## Полезные команды

```bash
# Запуск dev-сервера
uvicorn app.main:app --reload

# Создать новую миграцию
alembic revision --autogenerate -m "описание изменений"

# Применить миграции
alembic upgrade head

# Посмотреть текущую ревизию
alembic current

# Откатить одну миграцию
alembic downgrade -1
```
