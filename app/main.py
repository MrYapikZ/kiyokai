from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routers.v1.routers import api_router
from app.core import prisma

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🔌 Connecting to Prisma...")
    await prisma.connect_db()
    yield
    print("🔌 Disconnecting from Prisma...")
    await prisma.disconnect_db()

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Kiyokai API is running!"}

app.include_router(api_router, prefix="/api/v1")

