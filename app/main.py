from fastapi import FastAPI

from app.controllers.auth import router as auth_router
from app.controllers.profile import router as profile_router
from app.controllers.recipe import router as recipe_router
from app.controllers.pantry import router as pantry_router
from app.controllers.suggestion import router as suggestion_router
def create_app() -> FastAPI:
    app = FastAPI(title="Recipe Book")
    app.include_router(auth_router)
    app.include_router(profile_router)
    app.include_router(recipe_router)
    app.include_router(pantry_router)
    app.include_router(suggestion_router)
    return app


app = create_app()