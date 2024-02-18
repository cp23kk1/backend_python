from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import api
from .config.database import models
from .config.database.mysql import MySQL
from .config.resource import Config


models.Base.metadata.create_all(bind=MySQL.engine)


def get_application() -> FastAPI:
    app = FastAPI(title=Config.PROJECT_NAME, version=Config.VERSION)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=Config.ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(api.router, prefix=Config.API_PREFIX)

    return app


# Load environment variables
Config.load_config()
app = get_application()


@app.get("/ping")
async def root():
    return {"message": "pong"}
