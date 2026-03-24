import uvicorn
from fastapi import FastAPI
from src.api.handlers.products import router as product_router

app = FastAPI()


def main():
    routers = [product_router]
    for router in routers:
        app.include_router(router)


main()
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
