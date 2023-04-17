import app.database as datab
import sqlalchemy.orm as _orm
from app import models as _mls
from app import schemas as schema
from fastapi.responses import JSONResponse
import re
import logging
from fastapi import HTTPException
debug_logger = logging.getLogger(__name__)
debug_logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')

file_handler = logging.FileHandler('auditlog.log')
file_handler.setFormatter(formatter)


debug_logger.addHandler(file_handler)

def check_space(name):
    count = 0
    for i in range(0, len(name)):
        if name[i] == " ":
            count += 1
    if count>3:
        return True

def get_database():
    db=datab.SessionLocal()
    debug_logger.debug("Creating session with database ")
    try:
        yield db
        debug_logger.debug("Session Created")
    except:
        raise HTTPException(status_code=500, detail="Unable to connect to database")
    finally:
        logging.debug("Session closed ")
        db.close()

def validate_phone_number(phone_number):
    
    if(str(phone_number).startswith('(') or str(phone_number).startswith('+')):
        if(str(phone_number[1]=='0' and str(phone_number[2]=='1'))):
            if(str(phone_number).endswith('123-1234')):
            
                return False
    if(len(phone_number)==5):
        return True
    if (len(phone_number)<4):
        return False 
    if "<Script>" in phone_number or "<script>" in phone_number or "string" in phone_number:
        return False
    if(str(phone_number).isalpha()==True):
        return False
    rx = re.compile('^(\\+?\\d{1,3}( )?)?((\\(\\d{1,3}\\))|\\d{1,3})[- .]?\\d{1,3}[- .]?\\d{4}$') 
    check_digit = [(k) for k in list(phone_number) if k.isalpha()]

    dot_regex=re.compile('[.]')
    if((dot_regex.search(phone_number)!=None) and len(phone_number)>4): 
        old_phone_number= str(phone_number).replace(".", "")
        print(phone_number)
        if(str(old_phone_number).isnumeric()):
            new_phone_number=list(phone_number)
            d={}
            for i in range(len(new_phone_number)):
                d[new_phone_number[i]]=d.get(new_phone_number[i],0)+1
            print(d)
            for key,value in d.items():
                if(key=="." and value<2):
                    return True
    if(bool(re.search(r"\s", phone_number))==True and len(phone_number)>4): 
        phone_number= str(phone_number).replace(" ", "")
        if(str(phone_number).isnumeric()):
            return True
    if(rx.search(phone_number) == None or  len(check_digit)>0):
        print("Hello")
        return False
    debug_logger.debug("Phone Number validation successful")
    return True

def validate_name(name):
    if "<Script>" in name or "<script>" in name or "string" in name or check_space(name)==True:
        return False
    check_num = [int(k) for k in list(name) if k.isdigit()]
    new_name=name.strip().replace(" ","")
    pattern=r'^[@ _!#$%^&*()<>?[/\|}{~:]+$'
    #regex = re.compile('^[@ _!#$%^&*()<>?[/\|}{~:]+$')  
    regex=re.compile(pattern)
    if(regex.search(new_name) != None or len(check_num)>0):
        return False
    name=name.split()
    if(len(name)>3):
        return False
    new_name=list(new_name)
    d={}
    for i in range(len(new_name)):
        d[new_name[i]]=d.get(new_name[i],0)+1
    print(d)
    for key,value in d.items():
        if (key=='-' and value>1) or (key=='_' and value>0) or (key=="'" and value>1) or (key==',' and value>1) or (key==" " and value>4) or (key=='’' and value>1):
            return False
    debug_logger.debug("Name validation is successful")
    return True


def create_phonebook_record(db:_orm.Session,user:schema.PhoneBookCreate):
    debug_logger.debug("Validating name and phone_number before inserting in database.")
    if(validate_name(user.name) and validate_phone_number(user.phone_number)):
        debug_logger.debug("Name and phone_number correct. Creating database object")

        db_phonebook_user= _mls.Phone(name=user.name,phone_number=user.phone_number)
        debug_logger.debug("Database object created")

        db.add(db_phonebook_user)
        debug_logger.debug("Adding to the database")
        db.commit()
        debug_logger.debug("Record successfully added name: "+user.name+" and phone_number: "+user.phone_number)

        db.refresh(db_phonebook_user)
        return JSONResponse(status_code=200, content=" Success. The record is inserted")

    else:
        return JSONResponse(status_code=400,content="The inputs are not in the appropriate format. Try again")


def get_record_by_phone_number(db:_orm.Session,phone_number:str):
    return db.query(_mls.Phone).filter(_mls.Phone.phone_number==phone_number).first()

def get_record_by_name(db:_orm.Session,name:str):
    return db.query(_mls.Phone).filter(_mls.Phone.name==name).first()

def get_all_records(db:_orm.Session):
    return db.query(_mls.Phone).all()


def delete_record_by_phone_number(db:_orm.Session,phone_number:str):
    try:
        
        db.query(_mls.Phone).filter(_mls.Phone.phone_number == phone_number).delete()
        db.commit()
    except Exception as e:
        raise Exception(e)
    
def delete_record_by_name(db:_orm.Session,name:str):
    try:
            db.query(_mls.Phone).filter(_mls.Phone.name == name).delete()
            db.commit()
    except Exception as e:
        raise Exception(e)
