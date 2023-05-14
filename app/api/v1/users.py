# app/api/v1/users.py
from fastapi import APIRouter
from app.api.db.session import supabase
from . import conversations  # Import the conversations microservice

router = APIRouter()


@router.get("/users/")
def read_users():
    response = supabase.table("users").select("*").execute()
    return response


@router.get("/users/{user_id}")
def read_user(user_id: int):
    user_response = (
        supabase.table("users").select("*").filter("id", "eq", user_id).execute()
    )
    return user_response
