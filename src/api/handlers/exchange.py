from fastapi import APIRouter, HTTPException
from src.services.multy_exchange_client import MultyExchangeClient

router = APIRouter(prefix="/api/v1/exchange", tags=["exchange"])


@router.get("/")
async def get_exchange(
    price: float,
    base_currency: str,
    target_currency: str,
):
    result = MultyExchangeClient().get_response(
        price=price, from_currency=base_currency, to_currency=target_currency
    )
    if result is None:
        raise HTTPException(status_code=404, detail="No exchange found")
    return result
