## Реферальная система

### Установка
1. Установите Docker и Docker Compose
2. Клонируйте репозиторий
3. Запустите `docker-compose up --build`

### API Endpoints

#### Авторизация
- POST `/api/auth/`
  Тело запроса:
  ```json
  {
      "phone": "+79991234567"
  }