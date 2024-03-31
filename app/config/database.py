from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config.resource import Config

config = Config.load_config()


class MySQL:
    # Configure database connection
    DATABASE_URL_APP = f"mysql+mysqldb://{config.DB_USERNAME}:{config.DB_PASSWORD}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_APP_NAME}"
    DATABASE_URL_CMS = f"mysql+mysqldb://{config.DB_USERNAME}:{config.DB_PASSWORD}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_APP_NAME}"
    # Create SQLAlchemy engine
    engine_app = create_engine(DATABASE_URL_APP)
    engine_cms = create_engine(DATABASE_URL_CMS)

    engine_app.connect

    # Create a sessionmaker
    SessionLocalApp = sessionmaker(autocommit=False, autoflush=False, bind=engine_app)
    SessionLocalCms = sessionmaker(autocommit=False, autoflush=False, bind=engine_cms)

    # Base class for declarative models
    Base = declarative_base()

    def get_app_database_session(self):
        try:
            db = self.SessionLocalApp()
            yield db
        finally:
            db.close()

    def get_cms_database_session(self):
        try:
            db = self.SessionLocalCms()
            yield db
        finally:
            db.close()
