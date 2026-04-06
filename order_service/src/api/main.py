import uvicorn
from fastapi import FastAPI
from order_service.src.api.routers.orders import router as orders_router

app = FastAPI()


def main():
    app.include_router(orders_router)


if __name__ == "__main__":
    main()
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
