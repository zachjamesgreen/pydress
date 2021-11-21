import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import models
import database
import main

SQLALCHEMY_DATABASE_URL = "postgresql://zach@localhost/pydress_test"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
database.Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

main.app.dependency_overrides[database.get_db] = override_get_db
client = TestClient(main.app)

@pytest.fixture
def clean_db():
    yield
    database.Base.metadata.drop_all(bind=engine)
    database.Base.metadata.create_all(bind=engine)

def create_record():
    return client.post(
        "/create_record",
        json={"name": "zach","phone_numbers": [{"phone_number": "123-456-7890"}],"emails": [{"email": "a@example.com"}],"addresses": [{"street": "123 Main st","city": "Anytown","state_abbr": "CA","zip_code": "90210","apt_number": ""}]}
        )

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

# @router.post("/create_record")
# test if any part of the record is duplicate

def test_create_record(clean_db):
    # person = PersonFactory.build()
    res = create_record()
    assert res.status_code == 200
    assert res.json() == {'id': 1, 'name': 'zach'}

    res = create_record()
    assert res.status_code == 400

def test_get_person(clean_db):
    create_record()
    res = client.get("/persons/1")
    assert res.status_code == 200
    assert res.json()["id"] == 1
    assert res.json()["name"] == "zach"

def test_get_persons(clean_db):
    create_record()
    res = client.post(
        "/create_record",
        json={"name": "matt","phone_numbers": [{"phone_number": "123-456-7890"}],"emails": [{"email": "a@example.com"}],"addresses": [{"street": "123 Main st","city": "Anytown","state_abbr": "CA","zip_code": "90210","apt_number": ""}]}
        )
    assert res.status_code == 200
    res = client.get("/persons")
    assert res.status_code == 200
    assert len(res.json()) == 2
    assert res.json()[0]["name"] == "zach"
    assert res.json()[1]["name"] == "matt"

def test_update_person(clean_db):
    create_record()
    res = client.post(
        "/persons/1",
        json={"name": "zach green"}
    )
    assert res.status_code == 200
    assert res.json()["name"] == "zach green"

def test_create_new_email_for_person(clean_db):
    create_record()
    res = client.post(
        "/persons/1/email",
        json={"email": "a@example.com"}
    )
    assert res.status_code == 400
    assert res.json()["detail"] == "Email already exists"

    res = client.post(
        "/persons/1/email",
        json={"email": "b@example.com"}
    )
    assert res.status_code == 200
    assert res.json()[0]["email"] == "a@example.com"
    assert res.json()[1]["email"] == "b@example.com"

def test_update_person_email(clean_db):
    create_record()
    client.post(
        "/persons/1/email",
        json={"email": "b@example.com"}
    )
    res = client.post("/persons/1/email/1",json={"email": "b@example.com"})
    assert res.status_code == 400
    res = client.get("/persons/1")
    res = client.post("/persons/1/email/1",json={"email": "aa@example.com"})
    assert res.status_code == 200
    assert res.json()[-1]["email"] == "aa@example.com"

def test_delete_person_email(clean_db):
    create_record()
    # returns 404 if email doesn't exist
    res = client.delete("/persons/1/email/500")
    assert res.status_code == 404

    res = client.delete("/persons/1/email/1")
    assert res.status_code == 200
    db = TestingSessionLocal()
    stmt = db.query(models.Email).filter(models.Email.email == "a@example.com").all()
    db.close()
    assert len(stmt) == 0

def test_create_new_phone_number_for_person(clean_db):
    create_record()
    # need to implement parsing ints from phone number
    # so that 123-456-7890 becomes 1234567890 and are the same
    # res = client.post(
    #     "/persons/1/phone_number",
    #     json={"phone_number": "123-456-7890"}
    # )
    # assert res.status_code == 400

    res = client.post("/persons/1/phone_number",json={"phone_number": "123-456-7890"})
    assert res.status_code == 400

    res = client.post("/persons/1/phone_number",json={"phone_number": "123-456-7891"})
    assert res.status_code == 200
    assert res.json()[1]["phone_number"] == "123-456-7891"




# def test_update_person_phone_number(clean_db):
# def test_delete_person_phone_number(clean_db):
# def test_create_new_address_for_person(clean_db):
# def test_update_person_address(clean_db):
# def test_delete_person_address(clean_db):

