from fastapi import Depends, HTTPException
from src.utils.auth import security


def require_token(credentials=Depends(security.access_token_required)):
    if not credentials:
        raise HTTPException(status_code=401, detail="Missing or invalid token")
    return credentials
