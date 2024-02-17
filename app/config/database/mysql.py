from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config.resource import Config

config = Config.load_config()


class MySQL:
    # Configure database connection
    DATABASE_URL = f"mysql+mysqldb://{config.DB_USERNAME}:{config.DB_PASSWORD}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}"
    # Create SQLAlchemy engine
    engine = create_engine(DATABASE_URL)

    # Create a sessionmaker
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Base class for declarative models
    Base = declarative_base()

    def get_database_session(self):
        try:
            db = self.SessionLocal()
            yield db
        finally:
            db.close()
