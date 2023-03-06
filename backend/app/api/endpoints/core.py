from fastapi import APIRouter, Depends, Query
from app.api.deps import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.core import (
    TrainStationSchema,
    ConnectingStationSchema,
    TrainStationWithConnectionSchema,
)
from app.models.core import Station, ConnectingStation
from typing import List
from app.exceptions import AppError
from sqlalchemy import exc as SQLAlchemyExceptions


router = APIRouter()


@router.post("/station", response_model=TrainStationSchema)
async def add_station(
    data: TrainStationSchema, session: AsyncSession = Depends(get_session)
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

    except SQLAlchemyExceptions.NoResultFound:
        raise AppError.STATION_NOT_FOUND_ERROR

    return res


@router.get("/all_stations", response_model=List[TrainStationWithConnectionSchema])
async def get_all_stations(session: AsyncSession = Depends(get_session)):
    res = await Station.get_all(session)

    return [i for i in res]


@router.put("/station", response_model=TrainStationWithConnectionSchema)
async def update_station_name(
    data: TrainStationSchema, session: AsyncSession = Depends(get_session)
):
    res = await Station.update(session, data)
    return res


@router.post("/connecting_station", response_model=ConnectingStationSchema)
async def add_connecting_station(
    data: ConnectingStationSchema, session: AsyncSession = Depends(get_session)
):
    res = await ConnectingStation(**dict(data)).insert(session)
    return res

@router.post("/update-connecting_station", response_model=ConnectingStationSchema)
async def add_connecting_station(id: str, data: ConnectingStationSchema, session: AsyncSession = Depends(get_session)
):
    res = await ConnectingStation.update(session, data)
    return res


# @router.post("/connecting_station_script", response_model=List[ConnectingStationSchema])
# async def add_connecting_stations(session: AsyncSession = Depends(get_session)
#                                   ):
#     graph = load_graph('station.json')
#     lst = []
#     for parent_station, value in graph.items():
#         for adjacent, distance in value.items():
#             data = {
#                 "id": parent_station,
#                 "connecting_id": adjacent,
#                 "distance": distance,
#                 "transit_time": 0 if '/' in parent_station else None
#             }
#             res = await ConnectingStation(**dict(ConnectingStationSchema(**data))).insert(session)
#             lst.append(res)
#
#     # import pdb
#     # pdb.set_trace()
#
#     return [i.__dict__ for i in lst]
