from fastapi import FastAPI, Depends, HTTPException, APIRouter, Body
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import exc, select
from database import get_db
from psycopg2.errors import UniqueViolation

import crud, models, schemas

router = APIRouter()

@router.post("/persons/{id}/address")
def update_person_address(id: int, address: schemas.AddressCreate ,db: Session = Depends(get_db)):
    person = crud.get_person(db, id)
    if person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    try:
        crud.create_address(db, address, id)
    except exc.IntegrityError as e:
        if isinstance(e.orig, UniqueViolation):
            raise HTTPException(status_code=400, detail='Address already exists')
    return person.addresses