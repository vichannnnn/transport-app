from datetime import datetime
from typing import List
import json
from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi_pagination import Page
from datetime import datetime
from sqlalchemy import update, select, literal_column
from sqlalchemy.exc import NoResultFound


train_router = APIRouter()


@train_router.get("/hello")
async def sanity_check():
    return {"Hello": "World!"}