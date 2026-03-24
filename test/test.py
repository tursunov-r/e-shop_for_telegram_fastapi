import time
import requests


def diagnose_page_loading(url):
    """Диагностика процесса загрузки страницы"""
    results = {}

    # 1. Измерение DNS-запроса
    import socket
    # start = time.time()
    # hostname = url.split('/')[2]
    # ip = socket.gethostbyname(hostname)
    # dns_time = time.time() - start
    # results['dns'] = dns_time

    # 2. Измерение времени подключения
    start = time.time()
    response = requests.get(url)
    total_time = time.time() - start
    results['total'] = total_time

    # 3. Анализ времени ответа сервера
    server_time = response.elapsed.total_seconds()
    results['server'] = server_time

    # 4. Размер ответа
    results['size'] = len(response.content)

    return results


# Использование
url = "http://0.0.0.0:8000/products"
diagnosis = diagnose_page_loading(url)
# print(f"DNS: {diagnosis['dns']} сек")
print(f"Сервер: {diagnosis['server']} сек")
print(f"Всего: {diagnosis['total']} сек")
print(f"Размер: {diagnosis['size']} байт")