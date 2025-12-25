from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine, select

from config import dbname, vin, rf
from orm import Temps

import math

def adutoc(adu):
    # Initial simple ADU to degC conversion
    # Rt = Rf * Vout / (Vin - Vout)
    vout = vin * adu / 4096.0
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

    t = t1 - 273

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
                temp.temp0 = adutoc(temp.adu0)
                temp.temp1 = adutoc(temp.adu1)
                temp.temp2 = adutoc(temp.adu2)
                temp.temp3 = adutoc(temp.adu3)
                session.commit()


