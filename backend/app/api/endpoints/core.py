import pydantic
from fastapi import APIRouter, Depends, Query
from fastapi.security.api_key import APIKey
from app.api.deps import get_session
from app.schemas.core import (
    TrainStationSchema,
    ConnectingStationSchema,
    TrainStationWithConnectionSchema,
)
from app.models.core import Station, ConnectingStation
from app.exceptions import AppError
from app.api import auth
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import exc as SQLAlchemyExceptions
from typing import List

router = APIRouter()


@router.post("/station", response_model=TrainStationSchema)
async def add_station(
    data: TrainStationSchema,
    session: AsyncSession = Depends(get_session),
    api_key: APIKey = Depends(auth.get_api_key),
):
    res = await Station(**dict(data)).insert(session)
    return res


@router.get("/station", response_model=TrainStationWithConnectionSchema)
async def get_station(
    name: str = Query(None),
    id: str = Query(None),
    session: AsyncSession = Depends(get_session),
):
    if not name and not id:
        raise AppError.STATION_QUERY_PARAMETERS_ERROR

    try:
        res = await Station.get(session, name, id)

    except SQLAlchemyExceptions.NoResultFound as e:
        raise AppError.STATION_NOT_FOUND_ERROR from e

    return res


@router.get("/all_stations", response_model=List[TrainStationWithConnectionSchema])
async def get_all_stations(session: AsyncSession = Depends(get_session)):
    res = await Station.get_all(session)
    return list(res)


@router.put("/station", response_model=TrainStationWithConnectionSchema)
async def update_station(
    id: str,
    data: TrainStationSchema,
    session: AsyncSession = Depends(get_session),
    api_key: APIKey = Depends(auth.get_api_key),
):
    try:
        res = await Station.update_by_id(session, id, data)
        return res

    except pydantic.ValidationError as e:
        raise AppError.STATION_NOT_FOUND_ERROR from e


@router.post("/connecting_station", response_model=ConnectingStationSchema)
async def add_connecting_station(
    data: ConnectingStationSchema,
    session: AsyncSession = Depends(get_session),
    api_key: APIKey = Depends(auth.get_api_key),
):
    res = await ConnectingStation(**dict(data)).insert(session)
    return res


@router.put("/connecting_station", response_model=ConnectingStationSchema)
async def update_connecting_station_by_id(
    id: str,
    data: ConnectingStationSchema,
    session: AsyncSession = Depends(get_session),
    api_key: APIKey = Depends(auth.get_api_key),
):
    try:
        res = await ConnectingStation.update_by_id(session, id, data)
        return res

    except pydantic.ValidationError as e:
        raise AppError.STATION_NOT_FOUND_ERROR from e
