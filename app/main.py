from fastapi import FastAPI

from app.controllers.auth import router as auth_router


def create_app() -> FastAPI:
    app = FastAPI(title="Recipe Book")
    app.include_router(auth_router)
    return app


app = create_app()
