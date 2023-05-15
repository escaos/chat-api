# app/api/services/auth.py
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from .utils import VerifyToken

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user_id(token: str = Depends(oauth2_scheme)):
    token_verifier = VerifyToken(token)
    payload = token_verifier.verify()
    if "status" in payload and payload["status"] == "error":
        raise HTTPException(
            status_code=payload["status_code"],
            detail=payload["msg"],
        )
    return payload.get("sub")  # Assuming 'sub' in your payload is the user ID
