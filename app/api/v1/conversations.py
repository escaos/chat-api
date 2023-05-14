# app/api/v1/conversations.py
from fastapi import APIRouter
from app.db.session import supabase

router = APIRouter()


async def read_conversations(
    user_id: int,
):  # Removed the router decorator, this is now a helper function
    response = (
        await supabase.table("conversations_users")
        .select()
        .filter("user_id", eq=user_id)
        .execute()
    )
    return response
