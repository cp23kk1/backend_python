from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import api


# def get_application() -> FastAPI:


# app = get_application()

app = FastAPI()

origins = [
    "http://localhost:8080",
    "http://localhost:3000",
    "https://stackpython.co",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
