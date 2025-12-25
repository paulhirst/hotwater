import time
import spidev

import datetime

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

    # read SPI data from MCP3108, 1 channel
    # Byte 1: 0b 00000 1 S/D D2
    # Byte 2: 0b D1 D0 X X X X X X
    # Byte 3: X X X X X X X X

    # S/D = 1 (Single ended)
    # D2 D1 D0 = channel number
    d2 = (adcnum & 4) >> 2
    d1 = (adcnum & 2) >> 1
    d0 = adcnum & 1
    byte1 = d2 + 2 + 4
    byte2 = (d1 << 7) + (d0 << 6)
    r = spi.xfer2([byte1, byte2, 0])
    #data = ((r[1] & 3) << 8) + r[2]
    data = ((r[1] & 15) << 8) + r[2]
    return data


while True:
    adu0 = readadc(0)
    adu1 = readadc(1)
    adu2 = readadc(2)
    adu3 = readadc(3)
    adu4 = readadc(4)
    adu5 = readadc(5)
    adu6 = readadc(6)
    adu7 = readadc(7)
    print(f"{adu0} {adu1} {adu2} {adu3} {adu4} {adu5} {adu6} {adu7}")
    time.sleep(1)
