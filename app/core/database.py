import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv("postgresql://database_0vfg_user:WIzzUQWD1sAb5NMwZZWqY6nIUjXn78ZM@dpg-d2iu9jur433s73e9048g-a.oregon-postgres.render.com/database_0vfg", "sqlite:///./dados.db")

# sqlite needs special connect_args
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
