import uvicorn
from app.database.engine import create_db_and_tables
from fastapi import FastAPI
from app.routers import status, users

app = FastAPI()
app.include_router(status.router)
app.include_router(users.router)

if __name__ == "__main__":
    create_db_and_tables()
    uvicorn.run(app, host="0.0.0.0", port=8000)
