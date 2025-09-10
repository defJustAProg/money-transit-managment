# Быстрый запуск

## 1. Установка зависимостей
```bash
uv sync
```

## 2. Настройка базы данных
```bash
uv run python manage.py migrate
uv run python manage.py load_initial_data
uv run python manage.py create_sample_transactions
```

## 3. Создание суперпользователя (опционально)
```bash
uv run python manage.py createsuperuser
```

## 4. Запуск сервера
```bash
uv run python manage.py runserver
```

## 5. Открытие в браузере
- **Главная страница**: http://127.0.0.1:8000/
- **Админ-панель**: http://127.0.0.1:8000/backend/admin/
- **API документация**: http://127.0.0.1:8000/backend/swagger/

## Готово! 🎉

Теперь вы можете:
- Просматривать транзакции на главной странице
- Добавлять новые транзакции
- Фильтровать данные
- Управлять справочниками
- Использовать REST API

## Примеры API запросов

### Получить все транзакции
```bash
curl http://127.0.0.1:8000/backend/api/transactions/
```

### Создать новую транзакцию
```bash
curl -X POST http://127.0.0.1:8000/backend/api/transactions/ \
  -H "Content-Type: application/json" \
  -d '{
    "date": "2025-01-10T10:00:00Z",
    "status": 1,
    "transaction_type": 2,
    "category": 5,
    "amount": 1000.00,
    "comment": "Тестовая транзакция"
  }'
```

### Получить статистику
```bash
curl http://127.0.0.1:8000/backend/api/transactions/stats/
```
