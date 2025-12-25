from sqlalchemy import create_engine

from config import dbname

from orm import Base

engine = create_engine(dbname, echo=True)

Base.metadata.create_all(engine)