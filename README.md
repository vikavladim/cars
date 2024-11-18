**Инструкция по запуску проекта**

**Шаг 1: Создание виртуальной среды**

```bash
python -m venv .venv
```

**Шаг 2: Активация виртуальной среды**

```bash
.\.venv\Scripts\activate
```

**Шаг 3: Установка зависимостей**

```bash
pip install -r requirements.txt
```

**Шаг 4: Переход в рабочую папку**

```bash
cd cars_project
```

**Шаг 5: Создание миграций**

```bash
python manage.py makemigrations
python manage.py migrate
```

**Шаг 6: Создание суперпользователя**

```bash
python manage.py createsuperuser
```

**Шаг 7: Запуск приложения**

```bash
python manage.py runserver
```

**Шаг 8: Запуск тестов**

```bash
python manage.py test
```