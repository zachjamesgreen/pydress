from fastapi import FastAPI, Depends, HTTPException, APIRouter, Body
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import exc, select
from database import get_db
from psycopg2.errors import UniqueViolation

import crud, models, schemas

router = APIRouter()

@router.post("/persons/{id}/address")
def create_person_address(id: int, address: schemas.AddressCreate, db: Session = Depends(get_db)):
    person = crud.get_person(db, id)
    if person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    try:
        crud.create_address(db, address, id)
    except exc.IntegrityError as e:
        if isinstance(e.orig, UniqueViolation):
            raise HTTPException(status_code=400, detail='Address already exists for person')
    return person.addresses

@router.patch("/persons/{id}/address")
def update_person_address(id: int, address: schemas.AddressUpdate, db: Session = Depends(get_db)):
    person = crud.get_person(db, id)
    if person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    try:
        db_address = crud.update_address(db, address)
        if db_address is None:
            raise HTTPException(status_code=404, detail="Address not found")
    except exc.IntegrityError as e:
        if isinstance(e.orig, UniqueViolation):
            raise HTTPException(status_code=400, detail='Address already exists for person')
    return person.addresses

@router.delete("/persons/{id}/address/{address_id}")
def delete_person_address(id: int, address_id: int, db: Session = Depends(get_db)):
    person = crud.get_person(db, id)
    if person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    db_address = crud.delete_address(db, address_id)
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    return person.addresses
