FROM python:3.11

WORKDIR /app

# Копируем файл зависимостей
COPY requirements.txt /app/

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код проекта
COPY . /app/

 # Открываем порт, на котором будет работать приложение
 EXPOSE 8000

# Важно! Указываем правильный путь к manage.py
# CMD ["python", "src/manage.py", "runserver", "0.0.0.0:8000"]
