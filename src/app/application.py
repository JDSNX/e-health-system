from fastapi import FastAPI
from app.database.core import Base
from app.database.session import engine
from app.users.routers import router as user_router

Base.metadata.create_all(bine=engine)

app = FastAPI()

app.include_router(user_router)

@app.get("/")
async def root():
    return {"message": "hello"}