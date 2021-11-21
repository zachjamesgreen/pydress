from typing import List, Optional

from pydantic import BaseModel

class AddressBase(BaseModel):
    street: str
    apt_number: Optional[str] = None
    zip_code: str
    city: str
    state_abbr: str

class AddressCreate(AddressBase):
    pass

class Address(AddressBase):
    id: int
    person_id: int

    class Config:
        orm_mode = True



class EmailBase(BaseModel):
    email: str

class EmailCreate(EmailBase):
    pass

class Email(EmailBase):
    id: int
    person_id: int

    class Config:
        orm_mode = True



class PhoneNumberBase(BaseModel):
    phone_number: str

class PhoneNumberCreate(PhoneNumberBase):
    pass

class PhoneNumber(PhoneNumberBase):
    id: int
    person_id: int

    class Config:
        orm_mode = True



class PersonBase(BaseModel):
    name: str
    emails: Optional[List[EmailCreate]] = []
    addresses: Optional[List[AddressCreate]] = []
    phone_numbers: Optional[List[PhoneNumberCreate]] = []


class PersonCreate(PersonBase):
    pass

class Person(PersonBase):
    id: int
    addresses: List[Address] = []
    emails: List[Email] = []
    phone_numbers: List[PhoneNumber] = []

    class Config:
        orm_mode = True