from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("postgresql://postgres:example@localhost:5432/postgres")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

import logging  # noqa: E402

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
