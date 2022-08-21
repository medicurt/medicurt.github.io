from datetime import datetime, timedelta

import uvicorn

from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.security.api_key import APIKey

from starlette.responses import PlainTextResponse
from fastapi.exceptions import RequestValidationError


#from app.api.api import api_router

from app.core import dependencies
from app.core.config import settings
from app.api.api import api_router



app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_STR}/openapi.json",
    docs_url="/docs",
    redoc_url=None,
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


app.include_router(api_router, prefix=settings.API_STR)


@app.get("/logout")
async def route_logout_and_remove_cookie():
    response = RedirectResponse(url="/")
    response.delete_cookie(dependencies.API_KEY_NAME, domain="localtest.me")
    response.delete_cookie(dependencies.HOST_KEY_NAME, domain="localtest.me")
    return response


# @app.get("/docs", tags=["documentation"], include_in_schema=False)
# async def get_documentation(
#     api_key: APIKey = Depends(dependencies.get_api_key),
#     domain: str = Depends(dependencies.get_api_host),
# ):
#     response = get_swagger_ui_html(openapi_url="/api/openapi.json", title="docs")
#     response.set_cookie(
#         dependencies.API_KEY_NAME,
#         value=api_key,
#         # domain="localtest.me",
#         httponly=True,
#         max_age=1800,
#         expires=1800,
#     )
#     response.set_cookie(
#         dependencies.HOST_KEY_NAME,
#         value=domain,
#         domain="localtest.me",
#         httponly=True,
#         max_age=1800,
#         expires=1800,
#     )
#     return response



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)