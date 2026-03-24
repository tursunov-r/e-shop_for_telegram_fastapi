import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

load_dotenv()


engine = create_engine(
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}",
    echo=True,
    pool_size=5,
    max_overflow=2,
)


session_maker = sessionmaker(bind=engine)


@contextmanager
def get_session():
    with session_maker() as session:
        yield session


def try_connection():
    with get_session() as session:
        print({"message": "success"})
        return session


if __name__ == "__main__":
    try_connection()
