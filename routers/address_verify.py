from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from database import get_db

from zip_code import ZipCode

router = APIRouter()

@router.get("/verify_address")
def verify_address(street: str, zip: str, db: Session = Depends(get_db)):
    if not street or not zip:
        raise HTTPException(status_code=400, detail="Missing street or zip")
    zip_code, city, state_abbr = ZipCode.get_info(zip)
    address = {
        'apt_number': '',
        'street': street,
        'city': city,
        'state_abbr': state_abbr,
        'zip_code': zip_code
    }
    root = ZipCode.validate_address_xml(address)
    if root.find('Address/Error') is not None:
        raise HTTPException(status_code=400, detail=root.find('Address/Error/Description').text)
    apt = ''
    if root.find('Address/Address1') != None:
        apt = root.find('Address/Address1').text
    return {
        'apt_number': apt,
        'street': root.find('Address/Address2').text,
        'city': root.find('Address/City').text,
        'state_abbr': root.find('Address/State').text,
        'zip_code': root.find('Address/Zip5').text
    }
