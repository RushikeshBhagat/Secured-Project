from fastapi import Depends,FastAPI
from fastapi.responses import JSONResponse
from app import models
from app import schemas as schema
from app import utils as service
from app.database import engine
from sqlalchemy.orm import Session
from typing import List
import logging

app = FastAPI()

debug_logger = logging.getLogger(__name__)
debug_logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')
file_handler = logging.FileHandler('auditlog.log')
file_handler.setFormatter(formatter)
debug_logger.addHandler(file_handler)

models.Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"CSE-5328":"Secured Programming"}

#list records
@app.get("/PhoneBook/list",response_model=List[schema.PhoneBook])
def list_records(db: Session = Depends(service.get_database)):
    users = service.get_all_records(db)
    debug_logger.debug("List of all users returned")
    return users

#add record
@app.post("/PhoneBook/add",response_model=schema.PhoneBook)
def add_phoneBook_record(user:schema.PhoneBookCreate,db: Session = Depends(service.get_database)):
    if(len(user.name) == 0  or len(user.phone_number)==0): 
        return JSONResponse (status_code=400,content="The inputs are not in the appropriate format. Try again")
    db_usr = service.get_record_by_name(db=db,name=user.name)
    db_phone = service.get_record_by_phone_number(db=db,phone_number=user.phone_number)
    if db_usr:
        debug_logger.debug("User already exists"+ user.name)
        return JSONResponse(status_code=404, content="User already exists")
    if db_phone:
        debug_logger.debug("Phone number already exists "+ user.phone_number)
        return JSONResponse(status_code=404, content="Phone number already exists for a different user")
    return service.create_phonebook_record(db=db,user=user)

#delete record using number    
@app.put("/PhoneBook/deleteByNumber/{phonenumber}")
def delete_record_by_number(phonenumber=str,db: Session = Depends(service.get_database)):
    if(len(phonenumber)==0):
        return JSONResponse (status_code=400,content="The inputs are not in the appropriate format. Try again")
 
    if(service.validate_phone_number(phonenumber)):
        db_user_details = service.get_record_by_phone_number(db=db, phone_number=phonenumber)
        if not db_user_details:
            debug_logger.exception("This phone number does not exist.")
            return JSONResponse(status_code=404, content="No record found to delete")

        try:
            service.delete_record_by_phone_number(db=db, phone_number=phonenumber)
        except Exception as e:
            return JSONResponse(status_code=400, content="Unable to delete the record")
    else:
        debug_logger.exception("Invalid Phone Number. Use correct format")
        return JSONResponse(status_code=400,content="The phone number is not in the appropriate format. Try again")

    return JSONResponse(status_code=200, content="Success.The record is deleted")

#delete record using name
@app.put("/PhoneBook/deleteByName/{name}")
def delete_record_by_name(name=str, db: Session = Depends(service.get_database)):
    if(len(name)==0):
        return JSONResponse (status_code=400,content="The inputs are not in the appropriate format. Try again")
 
    if(service.validate_name(name)):
        db_user_details = service.get_record_by_name(db=db, name=name)
        if not db_user_details:
            debug_logger.exception("User not found")
            return JSONResponse(status_code=404, content="No record found to delete. Unable to delete")

        try:
            service.delete_record_by_name(db=db, name=name)
            debug_logger.debug("User is deleted " +name)
        except Exception as e:
            debug_logger.exception("Exception occured")
            return JSONResponse(status_code=400, content="Unable to delete the record")
    else:
        debug_logger.exception("Error with the name .Try with the appropriate format")
        return JSONResponse(status_code=400,content="The name is not in the appropriate format. Try again")
   
    return JSONResponse(status_code=200, content="Success.The record is deleted")
    
