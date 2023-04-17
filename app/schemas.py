import pydantic as py
import datetime as dt

class _PhoneBookBase(py.BaseModel):
    name : str
    phone_number:str

class PhoneBookCreate(_PhoneBookBase):
    pass

class PhoneBook(_PhoneBookBase):
    name:str
    phone_number: str
    record_date_created : dt.datetime
    record_date_updated : dt.datetime

    class Config:
        orm_mode =True
class PhoneBookDelete(py.BaseModel):
      name : str