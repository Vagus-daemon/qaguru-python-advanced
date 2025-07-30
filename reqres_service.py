from fastapi import FastAPI
from utils import load_users_data

app = FastAPI()


@app.get("/api/users/{user_id}", status_code=200)
def get_user():
    return {
        "data": {
            "id": 2,
            "email": "janet.weaver@reqres.in",
            "first_name": "Janet",
            "last_name": "Weaver",
            "avatar": "https://reqres.in/img/faces/2-image.jpg"
        },
        "support": {
            "url": "https://contentcaddy.io?utm_source=reqres&utm_medium=json&utm_campaign=referral",
            "text": "Tired of writing endless social media content? Let Content Caddy generate it for you."
        }
    }


@app.post("/api/login", status_code=200)
def login_user():
    return {"token": "QpwL5tke4Pnpja7X5"}


@app.post("/api/register", status_code=200)
def register_user():
    return {"id": "5", "token": "QpwL5tke4Pnpja7X5"}


@app.get("/api/users", status_code=200)
def users_list():
    """
    Возвращает список пользователей из файла users.json
    """
    users_data = load_users_data()
    return users_data


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
