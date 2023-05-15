# app/api/v1/users.py
from fastapi import APIRouter, Depends, HTTPException
from app.api.db.session import supabase
from fastapi.security import HTTPBearer

from app.api.services.utils import VerifyToken

router = APIRouter()


token_auth_scheme = HTTPBearer()


@router.get("/users/")
def read_users(token: str = Depends(token_auth_scheme)):
    result = VerifyToken(token.credentials).verify()
    print("result = ", result)
    if result.get("status"):
        raise HTTPException(status_code=401, detail=result.get("msg"))

    response = supabase.table("users").select("*").execute()
    return response


@router.get("/users/{user_id}")
def read_user(user_id: int, token: str = Depends(token_auth_scheme)):
    if str(user_id) != token:
        raise HTTPException(status_code=401, detail="User not authorized")

    user_response = supabase.table("users").select("*").eq("id", user_id).execute()
    return user_response
