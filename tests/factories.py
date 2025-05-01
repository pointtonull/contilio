from polyfactory.factories.pydantic_factory import ModelFactory
from polyfactory.factories.sqlalchemy_factory import SQLAlchemyFactory

from app import models, schemas


class RouteModelFactory(SQLAlchemyFactory[models.Route]):
    __model__ = models.Route
    id = None


class StopModelFactory(SQLAlchemyFactory[models.Stop]):
    __model__ = models.Stop
    id = None


class StopCreateSchemaFactory(ModelFactory[schemas.StopCreate]):
    __model__ = schemas.StopCreate
