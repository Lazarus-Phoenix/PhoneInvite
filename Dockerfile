# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем переменные окружения для Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем зависимости системы, если нужны (например, для psycopg2)
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

# Копируем файлы зависимостей и устанавливаем их
COPY poetry.lock pyproject.toml /app/
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --without dev --no-interaction --no-ansi --no-root

# Копируем исходный код проекта
COPY ./src /app/src

# Копируем статические файлы (если есть)
# COPY ./static /app/static
COPY . /app/

# Открываем порт, на котором будет работать приложение
EXPOSE 8000

# Запускаем приложение
# Команда по умолчанию для запуска приложения (будет переопределена в docker-compose.yml)
# CMD ["python", "src/manage.py", "runserver", "0.0.0.0:8000"]
# CMD ["gunicorn", "PhoneInvite.wsgi:application", "--bind", "0.0.0.0:8000"]