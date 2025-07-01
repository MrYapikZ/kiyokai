from fastapi import FastAPI
from app.routers.v1.routers import api_router
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Kiyokai API is running!"}


app.include_router(api_router, prefix="/api/v1")

