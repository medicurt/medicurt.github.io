from fastapi import APIRouter

#This file sets up the pathing for the api by importing routers from the different endpoint files
#and then assigning them to a url path in order to access the endpoint's functionality.

from app.api.endpoints import(
    event
)

api_router = APIRouter()

api_router.include_router(
    event.router, prefix="/event",
    tags = ["event"]
)