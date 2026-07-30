from sqlalchemy import create_engine
from sqlalchemy.engine import Engine


def get_engine(connection_string: str) -> Engine:
    return create_engine(connection_string)
