from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import time
import spidev

from config import dbname
from orm import Temps

import datetime
engine = create_engine(dbname, echo=False)

spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 1500000 # 1.5MHz
spi.mode = 0

def readadc(adcnum):
    # read SPI data from the MCP3008, 1 channel
    # This takes about 150us
    # Byte 1: 0b00000001
    # Byte 2: S/D D2 D1 D0 X X X X 
    # Byte 3: X X X X X X X X
    # r = spi.xfer2([1, 8 + adcnum << 4, 0])

    # read SPI data from MCP3208, 1 channel
    # Byte 1: 0b 00000 1 S/D D2
    # Byte 2: 0b D1 D0 X X X X X X
    # Byte 3: X X X X X X X X

    # S/D = 1 (Single ended)
    # D2 D1 D0 = channel number
    d2 = (adcnum & 4) >> 2
    d1 = (adcnum & 2) >> 1
    d0 = adcnum & 1
    r = spi.xfer2([6+d2, (d1 << 7) + (d0 << 6), 0])
    #data = ((r[1] & 3) << 8) + r[2]
    data = ((r[1] & 15) << 8) + r[2]
    return data


with Session(engine) as session:
    while True:
        t = Temps()
        t.datetime = datetime.datetime.now()
        t.adu0 = readadc(0)
        t.adu1 = readadc(1)
        t.adu2 = readadc(2)
        t.adu3 = readadc(3)
        print(f"{t.datetime} {t.adu0} {t.adu1} {t.adu2} {t.adu3}")
        session.add(t)
        session.commit()
        time.sleep(10)
