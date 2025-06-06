# Указываем базовый образ
FROM python:3.12-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app
# Явно устанавливаем django
# RUN pip install django
# Обновляемся
RUN apt-get update && \
       # apt-get install -y gcc libpq-dev && \
       apt-get install -y --no-install-recommends gcc libpq-dev && \
       apt-get clean && \
       rm -rf /var/lib/apt/lists/*

# Устанавливаем Poetry
RUN pip install poetry && poetry --version

# Копируем файлы зависимостей
COPY poetry.lock pyproject.toml ./

# Устанавливаем зависимости с помощью Poetry (исправленная часть)
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root

# Копируем остальные файлы проекта в контейнер
COPY . .

# Настройка переменных окружения
# ENV PYTHONUNBUFFERED=1
# ENV PYTHONDONTWRITEBYTECODE=1
ENV POETRY_VIRTUALENVS_CREATE=false

# Создаем директорию для статики
# Если Nginx не используется, эта директория может быть не нужна на этапе сборки Dockerfile.
# Django collectstatic создаст STATIC_ROOT при необходимости.
# RUN mkdir -p /app/staticfiles && chmod -R 755 /app/staticfiles

# Открываем порт 8000 для взаимодействия с приложением
EXPOSE 8000

# Запуск команды
# CMD ["poetry", "run", "gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]

# Определяем команду для запуска приложения
# CMD ["poetry", "run", "python", "src/manage.py", "runserver", "0.0.0.0:8000"]