from fastapi import FastAPI

# from app.api.v1 import users
app = FastAPI()


@app.get("/api")
def health():
    return "API working!!!"
