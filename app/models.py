import typing
import datetime

from sqlalchemy import Integer, String, DateTime, Index
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, DeclarativeBase
from advanced_alchemy.base import orm_registry, BigIntAuditBase


METADATA: typing.Final = orm_registry.metadata
DeclarativeBase.metadata = METADATA


class Stop(BigIntAuditBase):
    __tablename__ = "stops"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(256), nullable=False)


class Route(BigIntAuditBase):
    __tablename__ = "routes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    hashed: Mapped[str] = mapped_column(String(256), nullable=False)
    departure_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    arrival_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)

    __table_args__ = (Index("idx_hashed_departure_at", "hashed", "departure_at"),)
