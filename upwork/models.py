from pydantic import BaseModel, EmailStr, HttpUrl


class Address(BaseModel):
    line1: str
    line2: str
    city: str
    state: str
    postal_code: str
    country: str


class Profile(BaseModel):
    full_name: str
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    picture_url: HttpUrl
    address: Address
