from pydantic import BaseModel
from typing import List, Optional, Dict


class TrainStationSchema(BaseModel):
    id: str
    name: str
    interchange: bool


class ConnectingStationSchema(BaseModel):
    id: Optional[str]
    connecting_id: str
    distance: int
    transit_time: Optional[int]

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


