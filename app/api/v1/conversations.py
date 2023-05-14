from fastapi import APIRouter
from app.api.db.session import supabase

router = APIRouter()


@router.get("/conversations/")
def read_conversations_by_user(user_id: int):
    # Query conversations_users table
    response = (
        supabase.table("user_conversations")
        .select("conversations(*)")
        .eq("user_id", str(user_id))
        .order("updated_at", ascending=False)
        .execute()
    )

    result = [item["conversations"] for item in response["data"]]

    return result


@router.get("/conversations/{conversation_id}")
def read_conversation_by_id(user_id: int, conversation_id: int):
    response = (
        supabase.table("user_conversations")
        .select("conversations(*)")
        .eq("user_id", str(user_id))
        .eq("conversation_id", str(conversation_id))
        .execute()
    )

    result = [item["conversations"] for item in response["data"]]

    return result
