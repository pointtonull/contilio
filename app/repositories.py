from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from app import models


class RoutesRepository(SQLAlchemyAsyncRepository[models.Route]):
    model_type = models.Route


class RoutesService(SQLAlchemyAsyncRepositoryService[models.Route]):
    repository_type = RoutesRepository
