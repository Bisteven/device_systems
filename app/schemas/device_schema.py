from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class DeviceTypeEnum(str, Enum):
    laptop = "laptop"
    tablet = "tablet"
    proyector = "proyector"
    camara = "camara"
    router = "router"
    monitor = "monitor"
    otro = "otro"


class DeviceBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=150, examples=["Laptop Lenovo ThinkPad"])
    serial_number: str = Field(..., min_length=3, max_length=100, examples=["LEN-2024-001"])
    device_type: DeviceTypeEnum = Field(..., examples=["laptop"])
    brand: Optional[str] = Field(default=None, max_length=100, examples=["Lenovo"])
    is_available: bool = Field(default=True)


class DeviceCreate(DeviceBase):
    pass


class DeviceUpdate(DeviceBase):
    pass


class DevicePatch(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=150)
    serial_number: Optional[str] = Field(default=None, min_length=3, max_length=100)
    device_type: Optional[DeviceTypeEnum] = None
    brand: Optional[str] = Field(default=None, max_length=100)
    is_available: Optional[bool] = None


class DeviceResponse(DeviceBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}
