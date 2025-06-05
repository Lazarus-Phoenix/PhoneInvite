# Реферальная система с авторизацией по телефону

## Установка проекта

1. Клонировать репозиторий:
```bash
git clone https://github.com/your-repo/referral-system.git
cd referral-system
```

2. Запустить Docker контейнеры:
```bash
docker-compose up --build
```

## API Endpoints

### Авторизация по телефону

#### Отправка OTP
```http
POST /auth/login/
Content-Type: application/json

{
    "phone": "+79999999999"
}
```

#### Проверка OTP
```http
POST /auth/verify/
Content-Type: application/json

{
    "phone": "+79999999999",
    "otp": "1234"
}
```

### Профиль пользователя

#### Получение профиля
```http
GET /profile/
Authorization: Bearer your_token
```

#### Использование инвайт-кода
```http
POST /profile/
Content-Type: application/json
Authorization: Bearer your_token

{
    "referrer_invite_code": "ABC123"
}
```

## Тестирование

Запуск тестов:
```bash
docker-compose exec web python manage.py test
```

## Документация API

Доступна по адресу: http://localhost:8000/docs/

## Postman коллекция.

Доступна в корне проекта: postman_collection.json