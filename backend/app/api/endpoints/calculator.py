from fastapi import APIRouter, Depends
from fastapi.security.api_key import APIKey
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_session
from app.schemas.core import ShortestPathSchema
from app.models.core import Station
from app.api import auth
from app.map_calculator import shortest_path


router = APIRouter()


@router.get("/get_shortest_path_by_id", response_model=ShortestPathSchema)
async def get_shortest_path_by_id(
    start_id: str,
    end_id: str,
    session: AsyncSession = Depends(get_session),
    api_key: APIKey = Depends(auth.get_api_key),
):
    res = await Station.get_all(session)
    distance, stations = shortest_path(res, start_id, end_id)
    resp = {"distance": distance, "stations": stations}
    return resp
