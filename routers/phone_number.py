from fastapi import FastAPI, Depends, HTTPException, APIRouter, Body
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import exc, select
from database import get_db
from psycopg2.errors import UniqueViolation

import crud, models, schemas

router = APIRouter()

@router.post("/persons/{id}/phone_number")
def create_phone_number(id: int, phone_number: schemas.PhoneNumberCreate ,db: Session = Depends(get_db)):
    person = crud.get_person(db, id)
    if person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    try:
        crud.create_phone_number(db, phone_number, id)
    except exc.IntegrityError as e:
        if isinstance(e.orig, UniqueViolation):
            raise HTTPException(status_code=400, detail='Phone number already exists for person')
    return person.phone_numbers

@router.patch("/persons/{id}/phone_number")
def update_phone_number(id: int, phone_number: schemas.PhoneNumberUpdate, db: Session = Depends(get_db)):
    person = crud.get_person(db, id)
    if person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    try:
        p = crud.update_phone_number(db, phone_number, person)
        if p is None:
            raise HTTPException(status_code=404, detail="Phone Number not found")
    except exc.IntegrityError as e:
        if isinstance(e.orig, UniqueViolation):
            raise HTTPException(status_code=400, detail='Phone Number already exists for person')
    return person.phone_numbers

@router.delete("/persons/{id}/phone_number/{phone_number_id}")
def delete_phone_number(id: int, phone_number_id: int, db: Session = Depends(get_db)):
    person = crud.get_person(db, id)
    if person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    p = crud.delete_phone_number(db, phone_number_id)
    if p is None:
        raise HTTPException(status_code=404, detail="Phone Number not found")
    return person.phone_numbers