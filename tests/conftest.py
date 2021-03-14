import asyncio

import pytest
import sqlalchemy
from starlette.testclient import TestClient

from app.application import app
from app.db import database
from app.db.models import metadata
from app.settings import settings


@pytest.fixture(autouse=True, scope='session')
def create_test_database():
    engine = sqlalchemy.create_engine(settings.TEST_DB_URL)
    metadata.create_all(engine)
    yield
    metadata.drop_all(engine)


@pytest.fixture(scope='session')
def client():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(database.connect())
    yield TestClient(app)
    loop.run_until_complete(database.disconnect())
