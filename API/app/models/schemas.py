from pydantic import BaseModel
from typing import List
from sqlalchemy import Column, Integer, String
from app.core.database import Base
from app.core.config import settings


class StatusOK(BaseModel):
    status: int
    message: str


class RpiStatus(BaseModel):
    serial: str
    os: str
    user: str


class RpiPowerStatus(BaseModel):
    serial: str
    os: str
    power_status: str
    ip: str


class HardwareAvailability(BaseModel):
    available: List[str]
    unavailable: List[RpiStatus]


class SoftwareAvailability(BaseModel):
    operating_systems: List[str]


class OSMetadata(BaseModel):
    name: str
    serials: List[str]


class UserMetadata(BaseModel):
    user: str
    operating_systems: List[OSMetadata]


class PowerStatus(BaseModel):
    power_status: List[RpiPowerStatus]


class ListSerials(BaseModel):
    serial: str
    os: str


class Token(BaseModel):
    access_token: str
    token_type: str


class UserStored(BaseModel):
    username: str
    hashed_password: str


class User(Base):
    __tablename__ = settings.TABLE_NAME

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
