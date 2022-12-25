from __future__ import annotations
from datetime import date, datetime
from typing import List, Optional
from datetime import date, datetime
from typing import List

from pydantic import BaseModel
from sqlalchemy import Column, UniqueConstraint, select, insert, or_, ForeignKey
from sqlalchemy import Column, UniqueConstraint, select, or_, ForeignKey
from sqlalchemy import Boolean, DateTime, Integer, String, Index, BigInteger
from sqlalchemy.dialects import postgresql
from sqlalchemy import exc as SQLAlchemyExceptions
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import func, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import relationship
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

Base = declarative_base()


class TrainStation(BaseModel):
    name: str
    symbol: str
    routes: List[str]
    connecting_nodes: dict


d = {
    "name": "Newton",
    "symbol": "NS21/DT11",
    "routes": ["Downtown Line", "North-South Line"],
    "connecting_nodes": {
        "Novena": {"time_taken": 2},
        "Orchard": {"time_taken": 2},
        "Stevens": {"time_taken": 2},
        "Little India": {"time_taken": 3},
    },
}

d2 = {
    "name": "Novena",
    "symbol": "NS20",
    "routes": ["North-South Line"],
    "connecting_nodes": {
        "Newton": {"time_taken": 2},
        "Toa Payoh": {"time_taken": 2},
    },
}

d3 = {
    "name": "Stevens",
    "symbol": "DT10/TE11",
    "routes": ["Thomson East Coast Line", "Downtown Line"],
    "connecting_nodes": {
        "Newton": {"time_taken": 2},
        "Botanic Gardens": {"time_taken": 2},
    },
}

d4 = {
    "name": "Orchard",
    "symbol": "NS22",
    "routes": ["Thomson East Coast Line", "North-South Line"],
    "connecting_nodes": {
        "Newton": {"time_taken": 2},
        "Somerset": {"time_taken": 2},
        "Orchard Boulevard": {"time_taken": 2},
        "Great World": {"time_taken": 2}
    },
}

newton = TrainStation(**d)
print(newton)
novena = TrainStation(**d2)
print(novena)
stevens = TrainStation(**d3)
print(stevens)
orchard = TrainStation(**d4)
print(orchard)


class TravelState:
    def __init__(
            self,
            current_station: TrainStation,
            next_station: TrainStation = None,
            current_route=None,
            steps: int = 0,
            time_spent: int = 0,
    ):
        self.current_station = current_station
        self.previous_station = None
        self.next_station = next_station
        self.current_route = current_route
        self.steps = steps
        self.time_spent = time_spent

    def travel_one_station(self):
        self.previous_station = self.current_station
        self.current_station = self.next_station
        self.time_spent += self.previous_station.connecting_nodes[self.current_station.name]['time_taken']

    def set_starting_route(self, next_station: TrainStation):
        self.current_route = list(set(next_station.routes).intersection(
            self.current_station.routes
        ))[0]
        self.next_station = next_station
        return self.current_route

    def check_transfer_route(self):
        transfer = False
        if self.previous_station:
            if not any(route in self.previous_station.routes for route in self.next_station.routes):
                self.current_route = list(set(self.next_station.routes).intersection(
                    self.current_station.routes
                ))[0]
                transfer = True
        return transfer, self.current_route


travel = TravelState(novena)
print(travel.set_starting_route(newton))
travel.travel_one_station()
print(travel.time_spent)
travel.next_station = orchard
print(travel.check_transfer_route())

# class TrainStation(Base):
#     __tablename__ = "mrt_station"
#     station_id = Column(
#         Integer,
#         primary_key=True,
#     )
#     name = Column(String, nullable=False, unique=True)
#     symbol = Column(String, nullable=False)
#     routes = Column(postgresql.ARRAY(String, dimensions=1), nullable=False)
#     connecting_nodes = Column(JSONB, nullable=False)
#
#     __table_args__ = UniqueConstraint("name", "content", name="_train_station_name_uc")


stations = {
    "Newton": {
        "Novena": {"time_taken": 2},
        "Orchard": {"time_taken": 2},
        "Stevens": {"time_taken": 2},
        "Little India": {"time_taken": 3},
    },
    "Novena": {"Newton": {"time_taken": 2}, "Toa Payoh": {"time_taken": 2}},
}
