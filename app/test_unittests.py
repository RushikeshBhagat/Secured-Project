import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.main import app
from app.utils import get_database

SQLALCHEMY_DATABASE_URL = "sqlite:///./sample1.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_database():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_database] = override_get_database

client =  TestClient(app)


#Test case for valid inputs
def test_add_phoneBook_record():
    response = client.post(
        "/PhoneBook/add",
        json={
            "name": "Bruce",
            "phone_number":"+1 (713)-123-4325"
        }
    )
    msg=" Success. The record is inserted"
    assert response.status_code == 200
    assert response.json()==msg

#Test case for first record given in assignment
def test_add_phoneBook_record_1():
    response = client.post(
        "/PhoneBook/add",
        json={
            "name": "Schneier, Bruce",
            "phone_number":"123-1234"
        }
    )
    msg=" Success. The record is inserted"
    assert response.status_code == 200
    assert response.json()==msg



#Test case for second record given in assignment
def test_add_phoneBook_record_2():
    response = client.post(
        "/PhoneBook/add",
        json={
            "name": "Rushikesh",
            "phone_number":"+32 (21) 212-2324"
        }
    )
    msg=" Success. The record is inserted"
    assert response.status_code == 200
    assert response.json()==msg

#Test case for third record given in assignment
def test_add_phoneBook_record_3():
    response = client.post(
        "/PhoneBook/add",
        json={
            "name": "O’Malley, John F.",
            "phone_number":"011 701 111 1234"
        }
    )
    msg=" Success. The record is inserted"
    assert response.status_code == 200
    assert response.json()==msg

#Test case for fourth record given in assignment
def test_add_phoneBook_record_4():
    response = client.post(
        "/PhoneBook/add",
        json={
            "name": "John O’Malley-Smith",
            "phone_number":"12345.12345"
        }
    )
    msg=" Success. The record is inserted"
    assert response.status_code == 200
    assert response.json()==msg

#Test case for first incorrect name given in assignment
def test_add_phoneBook_record_invalid_name_1():
    response = client.post(
        "/PhoneBook/add",
        json={
            "name": "Ron O’’Henry",
            "phone_number":"+1 (817)-123-4325"
        }
    )
    msg="The inputs are not in the appropriate format. Try again"

    assert response.status_code == 400
    assert response.json()==msg

#Test case for second incorrect name given in assignment
def test_add_phoneBook_record_invalid_name_2():
    response = client.post(
        "/PhoneBook/add",
        json={
            "name": "Ron O’Henry-Smith-Barnes",
            "phone_number":"+1 (817)-123-4325"
        }
    )
    msg="The inputs are not in the appropriate format. Try again"

    assert response.status_code == 400
    assert response.json()==msg


#Test case for third incorrect name given in assignment
def test_add_phoneBook_record_invalid_name_3():
    response = client.post(
        "/PhoneBook/add",
        json={
            "name": "L33t Hacker",
            "phone_number":"+1 (817)-123-4325"
        }
    )
    msg="The inputs are not in the appropriate format. Try again"

    assert response.status_code == 400
    assert response.json()==msg

#Test case for fourth incorrect name given in assignment
def test_add_phoneBook_record_invalid_name_4():
    response = client.post(
        "/PhoneBook/add",
        json={
            "name": "<Script>alert(“XSS”)</Script>",
            "phone_number":"+1 (817)-123-4325"
        }
    )
    msg="The inputs are not in the appropriate format. Try again"

    assert response.status_code == 400
    assert response.json()==msg

#Test case for five incorrect name given in assignment
def test_add_phoneBook_record_invalid_name_5():
    response = client.post(
        "/PhoneBook/add",
        json={
            "name": "select * from users;",
            "phone_number":"+1 (817)-123-4325"
        }
    )
    msg="The inputs are not in the appropriate format. Try again"

    assert response.status_code == 400
    assert response.json()==msg

#Test case for first incorrect number given in assignment
def test_add_phoneBook_record_invalid_phone_number_1():
    response = client.post(
        "/PhoneBook/add",
        json={
            "name": "Cher",
            "phone_number":"123"
        }
    )
    msg="The inputs are not in the appropriate format. Try again"

    assert response.status_code == 400
    assert response.json()==msg


#Test case for second incorrect number given in assignment
def test_add_phoneBook_record_invalid_phone_number_2():
    response = client.post(
        "/PhoneBook/add",
        json={
            "name": "Cher",
            "phone_number":"1/703/123/1234"
        }
    )
    msg="The inputs are not in the appropriate format. Try again"

    assert response.status_code == 400
    assert response.json()==msg

#Test case for third incorrect number given in assignment
def test_add_phoneBook_record_invalid_phone_number_3():
    response = client.post(
        "/PhoneBook/add",
        json={
            "name": "Cher",
            "phone_number":"Nr 102-123-1234"
        }
    )
    msg="The inputs are not in the appropriate format. Try again"

    assert response.status_code == 400
    assert response.json()==msg

#Test case for fourth incorrect number given in assignment
def test_add_phoneBook_record_invalid_phone_number_4():
    response = client.post(
        "/PhoneBook/add",
        json={
            "name": "Cher",
            "phone_number":"<script>alert(“XSS”)</script>"
        }
    )
    msg="The inputs are not in the appropriate format. Try again"

    assert response.status_code == 400
    assert response.json()==msg

#Test case for five incorrect number given in assignment
def test_add_phoneBook_record_invalid_phone_number_5():
    response = client.post(
        "/PhoneBook/add",
        json={
            "name": "Cher",
            "phone_number":"+1234 (201) 123-1234"
        }
    )
    msg="The inputs are not in the appropriate format. Try again"

    assert response.status_code == 400
    assert response.json()==msg

#Test case for sixth incorrect number given in assignment
def test_add_phoneBook_record_invalid_phone_number_6():
    response = client.post(
        "/PhoneBook/add",
        json={
            "name": "Cher",
            "phone_number":"(001) 123-1234"
        }
    )
    msg="The inputs are not in the appropriate format. Try again"

    assert response.status_code == 400
    assert response.json()==msg

#Test case for missing name record
def test_add_phone_missing_record():
    response = client.post(
        "/PhoneBook/add",
        json={
            "name": "",
            "phone_number":"+1 (817)-321-4325"
        }
    )
    msg="The inputs are not in the appropriate format. Try again"
    assert response.status_code == 400
    assert response.json()==msg


#Test case for existing record
def test_add_phone_record_already_exist():
    response = client.post(
        "/PhoneBook/add",
        json={
            "name": "Bruce",
            "phone_number":"+1 (817)-321-4325"
        }
    )
    msg="User already exists"
    assert response.status_code == 404
    assert response.json()==msg

#Test case for invalid format
def test_add_phone_records_exist_invalid_format():
    response = client.post(
        "/PhoneBook/add",
        json={
            "name": "Bruce",
            "phone_number":"123"
        }
    )
    msg="User already exists"
    assert response.status_code == 404
    assert response.json()==msg

#Test case to get the users list   
def test_get_user_list():
    response = client.get(
        "/PhoneBook/list"
    )
    assert response.status_code == 200

#Test case for deleting the user by name
def test_delete_user_by_phone_name():
  
    response = client.put(
        "/PhoneBook/deleteByName/Bruce"
    )
    msg="Success.The record is deleted"
    print(response)
    assert response.status_code == 200
    assert response.json()==msg

#Test case for deleting using the user by name without passing parameter
def test_delete_user_by_phone_name_missing_record():
  
    response = client.put(
        "/PhoneBook/deleteByName/"
   
    )
    assert response.status_code == 404



#Test case for deleting using the user by phone number
def test_delete_user_by_phone_number():
    response = client.post(
        "/PhoneBook/add",
        json={
            "name": "Tom",
            "phone_number":"+1 (817)-324-9876"
        }
    )
    response = client.put(
        "/PhoneBook/deleteByNumber/+1 (817)-324-9876",
   
    )
    msg="Success.The record is deleted"
    print(response)
    assert response.status_code == 200
    assert response.json()==msg

#Test case for deleting using the user by phone number without passing parameter
def test_delete_user_by_phone_number_missing_number():
   
    response = client.put(
        "/PhoneBook/deleteByNumber/"
    )
    assert response.status_code == 404
