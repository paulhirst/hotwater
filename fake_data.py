from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select

from hotwater.config import dbname
from orm import Temps

import datetime
engine = create_engine(dbname, echo=False)

start = datetime.datetime(2025, 1, 1, 9, 0, 0)
end = datetime.datetime(2025, 1, 1, 19, 0, 0)
sec = datetime.timedelta(seconds=1)
foo = 30.1

with Session(engine) as session:
    while start < end:
        start += sec
        foo += 0.001
        t = Temps()
        t.datetime = start
        t.temp1 = foo
        session.add(t)
    session.commit()
