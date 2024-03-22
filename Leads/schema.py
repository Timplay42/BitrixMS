import uuid
from datetime import datetime
from typing import Optional

import phonenumbers
from fastapi import HTTPException
from pydantic import BaseModel, ConfigDict, EmailStr, field_validator


class BitrixBase(BaseModel):
    phone: str
    email: EmailStr
    full_name: str
    product: Optional[str] = None
    where: str


class BitrixUser(BaseModel):
    name: str
    username: str
    telegram_id: str
    phone: str



class BitrixCreate(BitrixBase):
    @field_validator("email")
    def email_to_lower(cls, v):
        if v is not None:
            return v.lower()
        return v

    @field_validator("phone")
    def check_phone(cls, v):
        if v is None:
            return v
        try:
            v = v.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
            number = phonenumbers.parse(v, None)
        except Exception:
            raise HTTPException(400, 'phone not valid')
        if phonenumbers.is_valid_number(number):
            return phonenumbers.format_number(numobj=number, num_format=1)
        else:
            raise HTTPException(400, 'phone not valid')


class BitrixUpdateRecord(BaseModel):
    telegram_id: str
    phone: str


class BitrixUpdateCompany(BaseModel):
    telegram_id: str
    company_link: str = None
    company_name: str = None


class BitrixCreateTarrifPaid(BaseModel):
    telegram_id:str
    tariff:str
    company_name:str
    payment_id:str
    company_link:str
    semantic_words:str
    telegram_username:str