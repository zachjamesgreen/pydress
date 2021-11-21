from fastapi import FastAPI, Depends, HTTPException, APIRouter, Body
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import exc, select
from database import get_db
from psycopg2.errors import UniqueViolation

import crud, models, schemas

router = APIRouter()

@router.post("/persons/{id}/email/{email_id}")
def update_person_email(id: int, email_id: int, email: schemas.EmailCreate ,db: Session = Depends(get_db)):
    person = crud.get_person(db, id)
    if person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    try:
        e = crud.update_email(db, email, email_id, person)
        if e is None:
            raise HTTPException(status_code=404, detail="Email not found")
    except exc.IntegrityError as e:
        if isinstance(e.orig, UniqueViolation):
            raise HTTPException(status_code=400, detail='Email already exists')
    return person.emails

@router.post("/persons/{id}/email")
def update_person_email(id: int, email: schemas.EmailCreate ,db: Session = Depends(get_db)):
    person = crud.get_person(db, id)
    if person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    try:
        crud.create_email(db, email, id)
    except exc.IntegrityError as e:
        if isinstance(e.orig, UniqueViolation):
            raise HTTPException(status_code=400, detail='Email already exists')
    return person.emails

@router.delete("/persons/{id}/email/{email_id}")
def delete_person_email(id: int, email_id: int, db: Session = Depends(get_db)):
    person = crud.get_person(db, id)
    if person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    e = crud.delete_email(db, email_id)
    if e is None:
        raise HTTPException(status_code=404, detail="Email not found")
    return