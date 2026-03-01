import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from databases.connection import base
from config import TEST_DATABASE_URL

@pytest.fixture(scope="session")
def engine():
    return create_engine(TEST_DATABASE_URL)

@pytest.fixture(scope="function")
def session(engine):
    connection = engine.connect()
    transacion = connection.begin()
    testing_session_local = sessionmaker(bind=connection)
    session = testing_session_local()
    yield session
    session.close()
    transacion.rollback()
    connection.close()

def test_connection(session):
    result = session.execute(text("SELECT 1")).scalar()
    assert result == 1