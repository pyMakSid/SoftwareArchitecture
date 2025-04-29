from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine(
    URL.create(
        drivername='postgresql',
        username='admin',
        password='secret',
        host='postgres',
        port='5432',
        database='messanger',
    )
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db_connection():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()