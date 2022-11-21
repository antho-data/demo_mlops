import pytest
from app.database.database_init import get_engine, get_user_session, init_databases
from app.data_mappers.data_mappers import User

init_databases("test", True)    

@pytest.fixture(autouse=True)
def create_dummy_user(tmpdir):
    """Fixture to execute asserts before and after a test is run"""
    # Setup: fill with any logic you want
    # No longer needed the database is always initiliazed with 3 default users "admin", "francois" and "noel"

    yield  # this is where the testing happens

    # Teardown : fill with any logic you want
