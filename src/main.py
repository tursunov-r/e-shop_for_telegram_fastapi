import time
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded

from src.core.settings import settings
from src.core.limiter import limiter
from src.api.handlers.products import router_v1
from src.api.handlers.orders import router as orders_router_v1
from src.api.handlers.user import router as user_router
from src.api.handlers.exchange import router as exchange_router

# from src.database.insert_for_test import create_data
from src.database.queries import create_tables
from src.core.db_connect import db_pool, http_client, get_pool, async_session
from src.api.exception_handlers import register_exception_handlers
from src.repositories.user_repository import UserRepository

# Анализ требований проекта SFMShop:
# - Нужен REST API для мобильного приложения, телеграм бота
# - Высокая производительность важна
# - Нужна автоматическая документация
# - Используется async/await для работы с БД
# - Не нужна админ-панель из коробки

# Выбор: FastAPI
# Обоснование:
# 1. FastAPI отлично подходит для REST API
# 2. Высокая производительность (async/await)
# 3. Автоматическая документация (Swagger)
# 4. Простой синтаксис
# 5. Поддержка async/await из коробки


@asynccontextmanager
async def lifespan(app: FastAPI):
    await get_pool()
    await create_tables()
    async with async_session() as session:
        await UserRepository.create_admin_query(session)
    # await create_data()
    yield
    await http_client.aclose()
    await db_pool.close()


app = FastAPI(lifespan=lifespan)
register_exception_handlers(app)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)
ALLOWED_ORIGINS = settings.cors_origins

routers = [router_v1, orders_router_v1, user_router, exchange_router]
for router in routers:
    app.include_router(router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Middleware для логирования запросов"""
    start_time = time.time()

    # Логирование запроса

    # Обработка запроса
    response = await call_next(request)

    # Логирование ответа
    process_time = time.time() - start_time

    # Добавление заголовка с временем обработки
    response.headers["X-Process-Time"] = str(process_time)

    return response


if __name__ == "__main__":
    uvicorn.run(
        "main:app", host="0.0.0.0", port=8000, reload=True, access_log=False
    )
