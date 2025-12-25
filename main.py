from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select

from .config import dbname
from orm import Base, Temps

import datetime

engine = create_engine(dbname, echo=True)

Base.metadata.create_all(engine)


with Session(engine) as session:
    t = Temps()
    t.datetime = datetime.datetime.now()
    t.temp1 = 30.2
    session.add(t)
    session.commit()

    stmt = select(Temps)

    for t in session.scalars(stmt):
        print(t)