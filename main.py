from typing import List
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from routers import persons, create_record, email, address, phone_number
app = FastAPI()

app.include_router(email.router)
app.include_router(address.router)
app.include_router(phone_number.router)
app.include_router(persons.router)
app.include_router(create_record.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}
