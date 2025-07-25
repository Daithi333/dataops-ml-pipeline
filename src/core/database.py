from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm.session import sessionmaker

from config import Config


class Database:
    engine: Engine = None
    session_maker: sessionmaker = None

    def __init__(self, url: str, **kwargs):
        self.engine = create_engine(url, **kwargs)
        self.session_maker = sessionmaker(bind=self.engine)

    @contextmanager
    def session(self):
        session = self.session_maker()
        try:
            yield session
        finally:
            session.close()


db = Database(
    Config.DB_URL,
    connect_args={"options": "-c timezone=utc"},
    pool_pre_ping=True,
    pool_size=Config.DB_POOL_SIZE,
    max_overflow=Config.DB_MAX_OVERFLOW,
)
