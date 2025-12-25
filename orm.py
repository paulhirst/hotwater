from typing import Optional
from datetime import datetime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    pass


class Temps(Base):
    __tablename__ = "temps"

    id: Mapped[int] = mapped_column(primary_key=True)
    datetime: Mapped[datetime]
    adu0: Mapped[Optional[float]]
    temp0: Mapped[Optional[float]]
    adu1: Mapped[Optional[float]]
    temp1: Mapped[Optional[float]]
    adu2: Mapped[Optional[float]]
    temp2: Mapped[Optional[float]]
    adu3: Mapped[Optional[float]]
    temp3: Mapped[Optional[float]]

    pump: Mapped[Optional[bool]]
    timer: Mapped[Optional[bool]]
    heater: Mapped[Optional[bool]]

    def __repr__(self):
        return f"{self.datetime}: temp1: {self.temp1}"
