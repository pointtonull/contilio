from modern_di import BaseGraph, Scope, providers

from app import repositories
from app.resources.db import create_sa_engine, create_session


class Dependencies(BaseGraph):
    database_engine = providers.Resource(Scope.APP, create_sa_engine)
    session = providers.Resource(Scope.REQUEST, create_session, engine=database_engine.cast)

    routes_service = providers.Factory(Scope.REQUEST, repositories.RoutesService, session=session.cast, auto_commit=True)
