from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine, select

from config import dbname, vin, rf
from orm import Temps

import math

def adctoc(adc):
    # Initial simple ADU to degC conversion
    # Rt = Rf * Vout / (Vin - Vout)
    # Note gpiozero adc values are in range [0..1] - ie Vout/Vin
    vout = vin * adc
    rt = rf * vout / (vin - vout)

    # Simplistic Rt = Ro exp(Beta * (S1 - S0)) where S = 1/T
    beta = 4000
    r0 = 10000
    t0 = 25 + 273  # in K

    # ln (Rt/R0) = Beta * (S1 - S0)

    s1ms0 = math.log(rt/r0) / beta
    s0 = 1.0 / t0

    s1 = s1ms0 + s0

    t1 = 1.0 / s1

    t = t1 - 273  # in C

    return t

if __name__ == "__main__":
    engine = create_engine(dbname, echo=False)
    stmt = select(Temps).filter(Temps.temp0.is_(None)).limit(1)
    done = False
    with Session(engine) as session:
        while not done:
            temp = session.execute(stmt).scalar_one_or_none()
            if temp is None:
                done = True
            else:
                print(f"Calibrating {temp.datetime}")
                temp.temp0 = adctoc(temp.adc0)
                temp.temp1 = adctoc(temp.adc1)
                temp.temp2 = adctoc(temp.adc2)
                temp.temp3 = adctoc(temp.adc3)
                session.commit()


