from fastapi import APIRouter, Response, HTTPException, Depends
from src.schemas.schemas import UserLoginSchema
from src.utils.auth import security, config

router_v1 = APIRouter(prefix="/api/v1/users", tags=["auth"])


@router_v1.post("/login")
def login(credentials: UserLoginSchema, response: Response):
    """Авторизация на сайте
    эндпоинт передает токен в cookie"""
    if credentials.username == "test" and credentials.password == "test":
        token = security.create_access_token(uid="12345")
        response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
        return {"access_token": token}
    raise HTTPException(status_code=401, detail="Invalid credentials")


@router_v1.get(
    "/protected", dependencies=[Depends(security.access_token_required)]
)
def test_token():
    return {"secret": "TOP SECRET"}
