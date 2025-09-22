from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from authlib.integrations.starlette_client import OAuth
from app.api.endpoints import router
from app.settings import settings


def create_app():
    app = FastAPI(debug=settings.debug)

    origins = [
        "http://localhost:5173",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(router)

    @app.get("/")
    async def root():
        return {"message": "Welcome to Git Gud Stats"}

    # shows Authorize button in Swagger UI
    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema
        schema = get_openapi(
            title="GitHub Stats API",
            version="0.1.0",
            description="Fetch GitHub user data with optional Bearer token (PAT).",
            routes=app.routes,
        )
        schema.setdefault("components", {}).setdefault("securitySchemes", {})
        # Define the security scheme that can be used by the operations
        # BETTER TO USE THE DEFAULT
        # schema["components"]["securitySchemes"]["BearerAuth"] = {
        #     "type": "http",
        #     "scheme": "bearer",
        #     "bearerFormat": "JWT",
        #     "description": "Enter your GitHub Personal Access Token"
        # }

        # this security scheme is a global setting but can be overwittern
        schema["security"] = [{"BearerAuth": []}]
        app.openapi_schema = schema
        return schema

    app.openapi = custom_openapi

    oauth = OAuth()
    oauth.register(
        name='oidc',
        authority=settings.oidc_authority,
        client_id=settings.oidc_client_id,
        client_secret=settings.oidc_client_secret,
        server_metadata_url=settings.oidc_server_metadata_url,
        client_kwargs={'scope': settings.oidc_scope}
    )

    return app
