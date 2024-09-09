import os

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

from tests.utils.database_utils import migrate_to_db
from tests.utils.docker_utils import start_database_container
from app.main import app

@pytest.fixture(scope="session")
def db_session():
    container = start_database_container()

    engine = create_engine(os.getenv("TEST_DATABASE_URL"))

    with engine.begin() as connection:
        migrate_to_db("migrations", "alembic.ini", connection)

    SesssionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)

    yield SesssionLocal

    container.stop()
    container.remove()
    engine.dispose()

@pytest.fixture(scope="function")
def client():
    with TestClient(app) as _client:
        yield _client