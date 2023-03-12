from pydantic import BaseModel
from typing import List, Optional


class TrainStationSchema(BaseModel):
    id: str
    name: str
    interchange: bool


class ConnectingStationSchema(BaseModel):
    id: str
    connecting_id: str
    distance: int
    transit_time: Optional[int]
    waiting_time: Optional[int]
    line: Optional[str]

    class Config:
        orm_mode = True


class TrainStationWithConnectionSchema(TrainStationSchema):
    connecting_stations: Optional[List[ConnectingStationSchema]]

    class Config:
        orm_mode = True


class ShortestPathSchema(BaseModel):
    distance: int
    stations: List[TrainStationWithConnectionSchema]

    class Config:
        orm_mode = True
