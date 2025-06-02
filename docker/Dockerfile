FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Важно! Указываем правильный путь к manage.py
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


# FROM python:3.10-slim
#
#
# WORKDIR /code
#
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1
#
# RUN apt-get update && apt-get install -y \
#     gcc \
#     python3-dev \
#     libpq-dev
#
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt
#
# COPY . .
#
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]