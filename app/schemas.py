import pydantic
from pydantic import BaseModel, PositiveInt


class Base(BaseModel):
    model_config = pydantic.ConfigDict(from_attributes=True)


class StopBase(Base):
    front: str
    back: str | None = None
    hint: str | None = None


class StopCreate(StopBase):
    pass


class Stop(StopBase):
    id: PositiveInt
    route_id: PositiveInt | None = None


class Stops(Base):
    items: list[Stop]


class RouteBase(Base):
    name: str
    description: str | None = None


class RouteCreate(RouteBase):
    pass


class Route(RouteBase):
    id: PositiveInt
    stops: list[Stop] | None


class Routes(Base):
    items: list[Route]
