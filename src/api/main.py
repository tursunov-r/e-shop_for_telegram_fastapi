from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.api.handlers.products import router_v1, router_v2
from src.api.handlers.auth import router_v1 as auth_v1
from src.database.insert_for_test import create_data
from src.database.queries import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    await create_data()
    routers = [router_v1, router_v2, auth_v1]
    for router in routers:
        app.include_router(router)
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
