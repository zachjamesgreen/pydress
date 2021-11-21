from typing import List
from sqlalchemy.orm import Session, selectinload

import models, schemas

#######################
# Create record
#######################
def create_record(db: Session, person: schemas.PersonCreate):
    db_person = create_person(db, person)
    db_emails = create_emails(db, person.emails, db_person.id)
    db_addresses = create_addresses(db, person.addresses, db_person.id)
    db_phone_numbers = create_phone_numbers(db, person.phone_numbers, db_person.id)
    return db_person


#######################
# Person CRUD
#######################
def get_person(db: Session, person_id: int):
    return db.query(models.Person).filter(models.Person.id == person_id).options(
        selectinload(models.Person.emails),
        selectinload(models.Person.addresses),
        selectinload(models.Person.phone_numbers)
    ).first()

def get_person_by_name(db: Session, name: str):
    return db.query(models.Person).filter(models.Person.name == name).first()

def get_persons (db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Person).offset(skip).limit(limit).all()

def create_person(db: Session, person: schemas.PersonCreate):
    db_person = models.Person(name=person.name)
    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    return db_person

#######################
# Email CRUD
#######################
def create_email(db: Session, email: schemas.EmailCreate, person_id: int):
    db_email = models.Email(email=email.email, person_id=person_id)
    db.add(db_email)
    db.commit()
    db.refresh(db_email)
    return db_email

def create_emails(db: Session, emails: List[schemas.EmailCreate], person_id: int):
    return [create_email(db, email, person_id) for email in emails]

def update_email(db: Session, email: schemas.EmailCreate, email_id: int, person: models.Person):
    db_email = db.query(models.Email).filter(models.Email.id == email_id).first()
    if db_email is None:
        return None
    db_email.email = email.email
    db.add(db_email)
    db.commit()
    db.refresh(db_email)
    return db_email

def delete_email(db: Session, email_id: int):
    db_email = db.query(models.Email).filter(models.Email.id == email_id).first()
    if db_email is None:
        return None
    db.delete(db_email)
    db.commit()
    return db_email

#######################
# Address CRUD
#######################
def create_address(db: Session, address: schemas.AddressCreate, person_id: int):
    db_address = models.Address(**address.dict(), person_id=person_id)
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address

def create_addresses(db: Session, addresses: List[schemas.AddressCreate], person_id: int):
    return [create_address(db, address, person_id) for address in addresses]

#######################
# PhoneNumber CRUD
#######################
def create_phone_number(db: Session, phone_number: schemas.PhoneNumberCreate, person_id: int):
    db_phone_number = models.PhoneNumber(phone_number=phone_number.phone_number, person_id=person_id)
    db.add(db_phone_number)
    db.commit()
    db.refresh(db_phone_number)
    return db_phone_number

def create_phone_numbers(db: Session, phone_numbers: List[schemas.PhoneNumberCreate], person_id: int):
    return [create_phone_number(db, phone_number, person_id) for phone_number in phone_numbers]