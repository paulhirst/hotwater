from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import time
import gpizero

from config import dbname
from orm import Temps

import datetime
engine = create_engine(dbname, echo=False)

adc0 = gpizero.MCP3208(channel=0)
adc1 = gpizero.MCP3208(channel=1)
adc2 = gpizero.MCP3208(channel=2)
adc3 = gpizero.MCP3208(channel=3)

with Session(engine) as session:
    while True:
        t = Temps()
        t.datetime = datetime.datetime.now()
        t.adc0 = adc0.value
        t.adc1 = adc1.value
        t.adc2 = adc2.value
        t.adc3 = adc3.value
        print(f"{t.datetime} {t.adc0} {t.adc1} {t.adc2} {t.adc3}")
        session.add(t)
        session.commit()
        time.sleep(10)
