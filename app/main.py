from fastapi import FastAPI

from app.api.v1 import auth
from app.api.v1 import users
from app.api.v1 import conversations
from app.api.v1 import messages

app = FastAPI()

prefix = "/api/v1"


@app.get("/api", tags=["core"])
def health():
    return "API working!!!"


app.include_router(auth.router, prefix=prefix, tags=["authentication"])
app.include_router(users.router, prefix=prefix, tags=["users"])
app.include_router(conversations.router, prefix=prefix, tags=["conversations"])
app.include_router(messages.router, prefix=prefix, tags=["messages"])
