from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
import sqlalchemy as _sal
import datetime as dt
from app.database import Base


class Phone(Base):
    __tablename__ = "phonebook"

    name = Column(String, primary_key=True,index=True)
    phone_number = Column(String, unique=True, index=True)
    record_date_created=Column(_sal.DateTime,default=dt.datetime.utcnow)
    record_date_updated=Column(_sal.DateTime,default=dt.datetime.utcnow)





