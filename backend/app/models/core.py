from app.db.base_class import Base
from app.exceptions import AppError
from app.schemas.core import (
    TrainStationSchema,
    TrainStationWithConnectionSchema,
    ConnectingStationSchema,
)
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    UniqueConstraint,
    select,
    update,
    literal_column,
)
from sqlalchemy.orm import relationship, selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import exc as SQLAlchemyExceptions
from typing import List, Optional


class Station(Base):
    __tablename__ = "train_station"
    row_id = Column(Integer, primary_key=True, nullable=False)
    id = Column(String, unique=True, nullable=False)
    name = Column(String, unique=True, nullable=False)
    interchange = Column(Boolean)

    connecting_stations: "ConnectingStation" = relationship(
        "ConnectingStation",
        foreign_keys="ConnectingStation.id",
        cascade="all, delete-orphan",
    )

    __table_args__ = (UniqueConstraint("id", "name"),)

    async def insert(self, session: AsyncSession) -> TrainStationSchema:
        try:
            session.add(self)
            await session.commit()
            await session.refresh(self)
            return TrainStationSchema(**self.__dict__)

        except SQLAlchemyExceptions.IntegrityError as exc:
            await session.rollback()
            raise AppError.STATION_ALREADY_EXISTS_ERROR from exc

    @classmethod
    async def get(
        cls, session: AsyncSession, name: Optional[str] = None, id: Optional[str] = None
    ) -> TrainStationWithConnectionSchema:

        stmt = select(Station).options(selectinload(Station.connecting_stations))
        if name:
            stmt = stmt.where(Station.name == name)
        if id:
            stmt = stmt.where(Station.id == id)
        res = await session.execute(stmt)
        return res.scalars().one()

    @classmethod
    async def get_all(
        cls, session: AsyncSession
    ) -> List[TrainStationWithConnectionSchema]:
        res = await session.execute(
            select(Station).options(selectinload(Station.connecting_stations))
        )
        return res.scalars().all()

    @classmethod
    async def update_by_id(
        cls, session: AsyncSession, id: str, data: TrainStationSchema
    ) -> TrainStationWithConnectionSchema:

        stmt = (
            update(Station)
            .returning(literal_column("*"))
            .where(Station.id == id)
            .values(**dict(data))
        )
        await session.execute(stmt)
        await session.commit()
        result = await Station.get(session=session, id=data.id)
        # result = TrainStationWithConnectionSchema.from_orm(res.fetchone())
        return result


class ConnectingStation(Base):
    __tablename__ = "connecting_station"

    row_id = Column(Integer, primary_key=True, nullable=False)
    id = Column(
        String,
        ForeignKey("train_station.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    connecting_id = Column(
        String,
        ForeignKey("train_station.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    distance = Column(Integer, nullable=False)
    transit_time = Column(Integer, nullable=True)
    __table_args__ = (UniqueConstraint("id", "connecting_id"),)

    async def insert(self, session: AsyncSession):
        try:
            session.add(self)
            await session.commit()
            await session.refresh(self)
            return self

        except SQLAlchemyExceptions.IntegrityError as exc:
            await session.rollback()
            raise AppError.STATION_NOT_FOUND_ERROR from exc

    @classmethod
    async def update_by_id(
        cls, session: AsyncSession, id: str, data: ConnectingStationSchema
    ) -> ConnectingStationSchema:

        stmt = (
            update(ConnectingStation)
            .returning(literal_column("*"))
            .where(ConnectingStation.id == id)
            .where(ConnectingStation.connecting_id == data.connecting_id)
            .values(**dict(data))
        )

        res = await session.execute(stmt)
        await session.commit()
        result = ConnectingStationSchema.from_orm(res.fetchone())
        return result
