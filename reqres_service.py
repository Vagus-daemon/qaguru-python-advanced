import uvicorn
import os
from fastapi import FastAPI
from utils import load_users_data
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

token = os.getenv("TOKEN")
@app.get("/api/users/{user_id}", status_code=200)
def get_user(user_id: int):
    users_data = load_users_data()
    for user in users_data["data"]:
        if user["id"] == user_id:
            return user


@app.post("/api/login", status_code=200)
def login_user():
    return {"token": token}


@app.post("/api/register", status_code=200)
def register_user():
    return {"token": token}


@app.get("/api/users", status_code=200)
def users_list():
    """
    Возвращает список пользователей из файла users.json
    """
    users_data = load_users_data()
    return users_data


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
