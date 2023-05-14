from fastapi import APIRouter
from app.api.db.session import supabase

router = APIRouter()


@router.get("/{conversation_id}/messages/")
def read_messages_by_conversation(user_id: int, conversation_id: int):
    # Query messages table
    response = (
        supabase.table("messages")
        .select("*")
        .eq("user_id", str(user_id))
        .eq("conversation_id", str(conversation_id))
        .order("created_at", ascending=True)
        .execute()
    )

    return response


@router.get("/{conversation_id}/messages/{message_id}")
def read_message_by_id(user_id: int, conversation_id: int, message_id: int):
    response = (
        supabase.table("messages")
        .select("*")
        .eq("user_id", str(user_id))
        .eq("conversation_id", str(conversation_id))
        .eq("id", str(message_id))
        .execute()
    )

    return response
