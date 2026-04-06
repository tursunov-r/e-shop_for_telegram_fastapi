# Архитектура микросервисов для проекта SFMShop

## payment-service
Сервис для приема и обработки платежа
### Структура:  
order-service/  
    ├── src/  
    │   ├── api/  
    │   │   ├── main.py              # FastAPI приложение  
    │   │   └── routes/  
    │   │       └── payments.py        # Endpoints для заказов
    │   ├── services/  
    │   │   ├── payments_service.py     # Бизнес-логика  
    │   │   └── payment_client.py     # Клиент для payment-service  
    │   ├── database/   
    │   └── config.py                # Конфигурация  
    ├── tests/  
    │   └── test_payments.py           # Тесты  
    ├── requirements.txt  
    ├── Dockerfile  
    └── README.md  
### Endpoints:
- POST /payments - создание платежа
- GET /payments/{payment_id} - получение информации о платеже

### Взаимодействие:
Через HTTP запросы