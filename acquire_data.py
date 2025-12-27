from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import time
import gpiozero

from config import dbname
from orm import Temps

import datetime
engine = create_engine(dbname, echo=False)

adc0 = gpiozero.MCP3208(channel=0)
adc1 = gpiozero.MCP3208(channel=1)
adc2 = gpiozero.MCP3208(channel=2)
adc3 = gpiozero.MCP3208(channel=3)

pump = gpiozero.LineSensor(pin=17, pull_up=None, active_state=False)
heater = gpiozero.LineSensor(pin=23, pull_up=True)
timer = gpiozero.LineSensor(pin=27, pull_up=True)

with Session(engine) as session:
    while True:
        t = Temps()
        t.datetime = datetime.datetime.now()
        t.adc0 = adc0.value
        t.adc1 = adc1.value
        t.adc2 = adc2.value
        t.adc3 = adc3.value
        t.pump = pump.value
        t.timer = timer.value
        t.heater = heater.value
        print(f"{t.datetime} {t.adc0} {t.adc1} {t.adc2} {t.adc3} {t.pump} {t.timer} {t.heater}")
        session.add(t)
        session.commit()
        time.sleep(10)
