from fastapi import HTTPException, Security
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jose import JWTError, jwt
from app.api.core.config import settings
from typing import Optional

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/login", scopes={"me": "Read information about the current user."}
)


def decode_token(token: str):
    try:
        payload = jwt.decode(token, settings.AUTH0_CLIENT_SECRET, algorithms=["HS256"])
        return payload
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid authentication token")


def get_current_user(
    security_scopes: SecurityScopes, token: str = Security(oauth2_scheme)
):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = f"Bearer"

    payload = decode_token(token)
    if payload.get("scope") and security_scopes.scope_str not in payload["scope"]:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions",
            headers={"WWW-Authenticate": authenticate_value},
        )
    return payload
