from sqlalchemy import Column, Integer, String, ForeignKey, select
from sqlalchemy.orm import relationship, validates
from sqlalchemy.sql.schema import UniqueConstraint

from database import Base, get_db


class Person(Base):

    __tablename__ = "persons"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)

    addresses = relationship("Address", back_populates="person")
    emails = relationship("Email", back_populates="person")
    phone_numbers = relationship("PhoneNumber", back_populates="person")

    @validates("name")
    def validate_name(self, key, name):
        return name.lower()



class Address(Base):
    __tablename__ = "addresses"
    __table_args__ = (UniqueConstraint('person_id', 'street'),)

    id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, ForeignKey("persons.id"))
    street = Column(String, nullable=False)
    apt_number = Column(String)
    zip_code = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state_abbr = Column(String, nullable=False)

    person = relationship("Person", back_populates="addresses")

    @validates("street")
    def validate_street(self, key, street):
        return street.lower()
    


class Email(Base):
    __tablename__ = "emails"
    __table_args__ = (UniqueConstraint('person_id', 'email'),)

    id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, ForeignKey("persons.id"))
    email = Column(String, nullable=False)

    person = relationship("Person", back_populates="emails")

    @validates("email")
    def validate_email(self, key, email):
        return email.lower()



class PhoneNumber(Base):
    __tablename__ = "phone_numbers"
    __table_args__ = (UniqueConstraint('person_id', 'phone_number'),)

    id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, ForeignKey("persons.id"))
    phone_number = Column(String, nullable=False)

    person = relationship("Person", back_populates="phone_numbers")
