from fastapi import Depends, HTTPException, APIRouter, Body
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import exc, select
from database import get_db

import crud, schemas

router = APIRouter()

@router.get("/persons")
def read_persons(db: Session = Depends(get_db)):
    persons = crud.get_persons(db)
    return persons

@router.get("/persons/{person_id}")
def read_person(person_id: int, db: Session = Depends(get_db)):
    person = crud.get_person(db, person_id)
    if person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    return person

@router.post("/persons/{id}")
def update_person(id: int, person: schemas.PersonCreate, db: Session = Depends(get_db)):
    db_person = crud.get_person(db, id)
    if db_person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    db_person.name = person.name
    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    return db_person