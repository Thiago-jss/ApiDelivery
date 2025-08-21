# ...existing code...
import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

logger = logging.getLogger("app.database")
database_url = os.getenv("DATABASE_URL")

if not database_url:
    raise RuntimeError("DATABASE_URL defina")

if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

connect_args = {"check_same_thread": False} if database_url.startswith("sqlite") else {}

engine = create_engine(
    database_url,
    connect_args=connect_args,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def init_db():
    
    try:
        import pkgutil
        import importlib
        import app.models as _models_pkg

        for _finder, _name, _ispkg in pkgutil.iter_modules(_models_pkg.__path__):
            importlib.import_module(f"{_models_pkg.__name__}.{_name}")
    except Exception as e:
        logger.exception("Falha ao importar módulos de models: %s", e)

    
    if os.getenv("FORCE_CREATE_TABLES", "false").lower() == "true":
        Base.metadata.create_all(bind=engine)
        logger.info("Base.metadata.create_all executado")
    else:
        logger.info("create_all pulado (FORCE_CREATE_TABLES != 'true').")