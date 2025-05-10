from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("postgresql://postgres:example@localhost:5432/postgres")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

import logging  # noqa: I001, E402

Base = declarative_base()

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
