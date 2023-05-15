from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from app.api.db.session import supabase
from app.api.core.config import settings
from auth0.management import Auth0
import http.client
import json

router = APIRouter()


class UserBase(BaseModel):
    email: str
    password: str


@router.post("/signup", tags=["authentication"])
async def signup(new_user: UserBase):
    # Fetch Management API Token
    conn = http.client.HTTPSConnection(settings.AUTH0_DOMAIN)
    payload = json.dumps(
        {
            "client_id": settings.AUTH0_CLIENT_ID,
            "client_secret": settings.AUTH0_CLIENT_SECRET,
            "audience": f"https://{settings.AUTH0_DOMAIN}/api/v2/",
            "grant_type": "client_credentials",
        }
    )
    headers = {"content-type": "application/json"}
    conn.request("POST", "/oauth/token", payload, headers)
    res = conn.getresponse()
    data = json.loads(res.read().decode("utf-8"))
    auth0_token = data.get("access_token")

    # Instantiate an Auth0 API client using the fetched token
    auth0 = Auth0(domain=settings.AUTH0_DOMAIN, token=auth0_token)

    # Create a new user in Auth0
    user_info = {
        "connection": "Username-Password-Authentication",  # or your connection type
        "email": new_user.email,
        "password": new_user.password,
        "email_verified": False,
    }
    try:
        auth0_user = auth0.users.create(body=user_info)

    except Exception as e:
        print("Exception = ", e)
        # Handle exceptions raised when creating the user
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    identity = auth0_user["identities"][0]
    user = {
        "id": identity["user_id"],
        "email": auth0_user["email"],
    }

    response = supabase.table("users").insert(user).execute()

    print("response = ", response)

    if "error" in response:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=response["error"]["message"],
        )

    return {"msg": "User created successfully."}


@router.post("/signin", tags=["authentication"])
async def signin(user: UserBase):
    conn = http.client.HTTPSConnection(settings.AUTH0_DOMAIN)
    payload = json.dumps(
        {
            "client_id": settings.AUTH0_CLIENT_ID,
            "client_secret": settings.AUTH0_CLIENT_SECRET,
            "audience": f"https://{settings.AUTH0_DOMAIN}/userinfo",
            "grant_type": "password",
            "username": user.email,
            "password": user.password,
            "scope": "openid profile email",
        }
    )
    headers = {"content-type": "application/json"}
    conn.request("POST", "/oauth/token", payload, headers)
    res = conn.getresponse()
    data = json.loads(res.read().decode("utf-8"))

    if "error" in data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=data["error_description"],
        )

    return data
