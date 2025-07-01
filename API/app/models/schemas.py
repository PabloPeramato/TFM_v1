from pydantic import BaseModel
from typing import List


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
