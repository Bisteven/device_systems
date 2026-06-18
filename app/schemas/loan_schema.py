from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class LoanStatusEnum(str, Enum):
    active = "active"
    returned = "returned"
    overdue = "overdue"


# Nested summaries for LoanDetailResponse
class UserSummary(BaseModel):
    id: int
    name: str
    email: str

    model_config = {"from_attributes": True}


class DeviceSummary(BaseModel):
    id: int
    name: str
    serial_number: str
    device_type: str

    model_config = {"from_attributes": True}


class LoanCreate(BaseModel):
    user_id: int = Field(..., examples=[1])
    device_id: int = Field(..., examples=[1])
    status: LoanStatusEnum = Field(default=LoanStatusEnum.active)


class LoanUpdate(BaseModel):
    status: LoanStatusEnum
    return_date: Optional[datetime] = None


class LoanResponse(BaseModel):
    id: int
    user_id: int
    device_id: int
    loan_date: datetime
    return_date: Optional[datetime]
    status: LoanStatusEnum

    model_config = {"from_attributes": True}


class LoanDetailResponse(BaseModel):
    loan_id: int
    status: LoanStatusEnum
    loan_date: datetime
    return_date: Optional[datetime]
    user: UserSummary
    device: DeviceSummary

    model_config = {"from_attributes": True}
