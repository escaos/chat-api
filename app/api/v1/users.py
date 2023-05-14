# app/api/v1/users.py
from fastapi import APIRouter
from app.db.session import supabase
from . import conversations  # Import the conversations microservice

router = APIRouter()


@router.get("/users/")
async def read_users():
    response = await supabase.table("users").select().execute()
    return response


@router.get("/users/{user_id}")
async def read_user(user_id: int):
    user_response = (
        await supabase.table("users").select().filter("id", eq=user_id).execute()
    )
    conversations_response = await conversations.read_conversations(user_id)
    return {**user_response, "conversations": conversations_response}
