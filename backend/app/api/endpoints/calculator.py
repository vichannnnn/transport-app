from fastapi import APIRouter, Depends
from fastapi.security.api_key import APIKey
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_session
from app.schemas.core import TrainStationWithConnectionSchema, ShortestPathSchema
from app.models.core import Station
from app.api import auth
from typing import List
import heapq


router = APIRouter()


def shortest_path(graph: List[TrainStationWithConnectionSchema], start: str, end: str):
    node_map = {node.id: node for node in graph}
    distances = {node.id: float("inf") for node in graph}
    distances[start] = 0
    pq = [(0, start)]
    previous_nodes = {node.id: None for node in graph}
    tracked_shortest_path = []

    while pq:
        current_distance, current_node_id = heapq.heappop(pq)

        if current_distance > distances[current_node_id]:
            continue

        current_node = node_map.get(current_node_id)
        if current_node is None:
            continue

        if current_node_id == end:
            while previous_nodes[current_node.id]:
                tracked_shortest_path.append(current_node)
                current_node = previous_nodes[current_node.id]
            tracked_shortest_path.append(node_map[start])
            tracked_shortest_path.reverse()

            return distances[end], tracked_shortest_path

        for station in current_node.connecting_stations or []:
            neighbor_id = station.connecting_id
            neighbor_distance = current_distance + station.distance

            if neighbor_distance < distances[neighbor_id]:
                distances[neighbor_id] = neighbor_distance
                previous_nodes[neighbor_id] = current_node  # type: ignore
                heapq.heappush(pq, (neighbor_distance, neighbor_id))

    return 0, []


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
