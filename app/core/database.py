import os
import logging
import pkgutil
import importlib
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

logger = logging.getLogger("app.database")


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/dados.db")

# normaliza caso venha "postgres://"
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)


connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def criar_bd():
    
    try:
        import app.models as _models_pkg
        for _finder, _name, _ispkg in pkgutil.iter_modules(_models_pkg.__path__):
            importlib.import_module(f"{_models_pkg.__name__}.{_name}")
    except Exception as e:
        logger.exception("Falha ao importar modelos: %s", e)

    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()