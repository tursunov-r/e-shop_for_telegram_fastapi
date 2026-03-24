# Файл src/services/log_service.py
from pymongo import MongoClient
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

# Подключение к MongoDB
client = MongoClient(
    host=os.getenv("MONGO_HOST", "localhost"),
    port=int(os.getenv("MONGO_PORT", 27017)),
)

db = client["sfmshop_logs"]
logs_collection = db["logs"]


def save_log(log_data):
    """Сохранение лога в MongoDB"""
    # Добавление timestamp если его нет
    if "timestamp" not in log_data:
        log_data["timestamp"] = datetime.now()

    result = logs_collection.insert_one(log_data)
    return result.inserted_id


def get_logs_by_type(log_type):
    """Получение логов по типу"""
    logs = logs_collection.find({"type": log_type})
    return list(logs)


def get_error_logs():
    """Получение всех ошибок"""
    logs = logs_collection.find({"type": "error"})
    return list(logs)


# Использование
# Лог ошибки
error_log = {
    "type": "error",
    "message": "Ошибка подключения к БД",
    "stack_trace": "...",
}
print(save_log(error_log))

# Лог доступа
access_log = {
    "type": "access",
    "ip": "192.168.1.1",
    "endpoint": "/api/products",
    "method": "GET",
    "status_code": 200,
}
print(save_log(access_log))
print(get_error_logs())

# Разные структуры - нет проблем!


def get_logs_by_status(status_code: int):
    """Поиск логов по статус-коду"""
    logs = logs_collection.find({"status_code": status_code})
    return list(logs)


def get_logs_by_date_range(start_date: datetime, end_date: datetime):
    """Поиск логов по диапазону дат"""
    logs = logs_collection.find(
        {"timestamp": {"$gte": start_date, "$lte": end_date}}
    )
    return list(logs)


def get_logs_by_ip(ip_address):
    """Поиск логов по IP адресу"""
    logs = logs_collection.find({"ip": ip_address})
    return list(logs)


yesterday = datetime.now() - timedelta(days=1)
today = datetime.now()

print(get_logs_by_ip("192.168.1.1"))
print(get_logs_by_status(200))
print(get_logs_by_date_range(yesterday, today))
