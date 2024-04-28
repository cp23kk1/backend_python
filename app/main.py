from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.exceptions.http_error import http_error_handler
from app.routes import api
from .config.database import engine_app, engine_cms
from .config.resource import Config
from app.models import app_models, cms_models

app_models.Base.metadata.create_all(bind=engine_app)
cms_models.Base.metadata.create_all(bind=engine_cms)


def get_application() -> FastAPI:
    app = FastAPI(title=Config.PROJECT_NAME, version=Config.VERSION)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Add exception handler
    app.add_exception_handler(HTTPException, http_error_handler)
    # Include routers
    print(Config.ENV)
    app.include_router(
        api.router,
        prefix="" if (Config.ENV == "prod") else f"/{Config.ENV}" + "/cms/api",
    )
    return app


# Load environment variables
Config.load_config()
app = get_application()


@app.get("/" + Config.ENV + "/cms/api/ping")
async def root():
    return {"message": "pong"}


@app.get("/terminate-request/")
async def terminate_request():
    # Add condition to terminate the request
    raise HTTPException(status_code=400, detail="Request terminated")
