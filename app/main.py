from contextlib import asynccontextmanager

import uvicorn
from app.database.engine import create_db_and_tables
from fastapi import FastAPI
from app.routers import status, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("On startup")
    create_db_and_tables()
    yield
    print("On shutdown")


app = FastAPI(lifespan=lifespan)
app.include_router(status.router)
app.include_router(users.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)
