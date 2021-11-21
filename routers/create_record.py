from fastapi import FastAPI, Depends, HTTPException, APIRouter, Body
from sqlalchemy.orm import Session
from sqlalchemy import exc
from typing import List #, Optional
from psycopg2.errors import UniqueViolation
from database import get_db


import crud, models, schemas

router = APIRouter()

@router.post("/create_record")
def create_record(person: schemas.PersonCreate, db: Session = Depends(get_db)):
    try:
        p = crud.create_record(db, person)
    except exc.IntegrityError as e:
        assert isinstance(e.orig, UniqueViolation)
        raise HTTPException(status_code=400, detail=str(e))
    # db.add(p)
    # db.commit()
    db.refresh(p)
    return p