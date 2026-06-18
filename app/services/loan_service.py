from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_
from app.models.loan_model import Loan
from app.models.user_model import User
from app.models.device_model import Device
from app.schemas.loan_schema import LoanCreate, LoanDetailResponse, UserSummary, DeviceSummary


def create_loan(db: Session, data: LoanCreate) -> Loan:
    user = db.query(User).filter(User.id == data.user_id).first()
    if not user:
        raise LookupError(f"Usuario con id={data.user_id} no encontrado.")

    device = db.query(Device).filter(Device.id == data.device_id).first()
    if not device:
        raise LookupError(f"Dispositivo con id={data.device_id} no encontrado.")

    if not device.is_available:
        raise ValueError(f"El dispositivo '{device.name}' no está disponible para préstamo.")

    loan = Loan(
        user_id=data.user_id,
        device_id=data.device_id,
        status="active",
        loan_date=datetime.utcnow(),
    )
    device.is_available = False
    db.add(loan)
    db.commit()
    db.refresh(loan)
    return loan


def get_loan_by_id(db: Session, loan_id: int) -> Optional[Loan]:
    return db.query(Loan).filter(Loan.id == loan_id).first()


def get_loans(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    user_id: Optional[int] = None,
    device_id: Optional[int] = None,
    user_email: Optional[str] = None,
    device_type: Optional[str] = None,
) -> List[Loan]:
    query = db.query(Loan).join(Loan.user).join(Loan.device)

    if status:
        query = query.filter(Loan.status == status)
    if user_id:
        query = query.filter(Loan.user_id == user_id)
    if device_id:
        query = query.filter(Loan.device_id == device_id)
    if user_email:
        query = query.filter(User.email.ilike(f"%{user_email}%"))
    if device_type:
        query = query.filter(Device.device_type == device_type)

    return query.offset(skip).limit(limit).all()


def get_loans_detail(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    user_email: Optional[str] = None,
    device_type: Optional[str] = None,
) -> List[LoanDetailResponse]:
    query = (
        db.query(Loan)
        .join(Loan.user)
        .join(Loan.device)
        .options(joinedload(Loan.user), joinedload(Loan.device))
    )

    if status:
        query = query.filter(Loan.status == status)
    if user_email:
        query = query.filter(User.email.ilike(f"%{user_email}%"))
    if device_type:
        query = query.filter(Device.device_type == device_type)

    loans = query.offset(skip).limit(limit).all()

    return [
        LoanDetailResponse(
            loan_id=loan.id,
            status=loan.status,
            loan_date=loan.loan_date,
            return_date=loan.return_date,
            user=UserSummary(id=loan.user.id, name=loan.user.name, email=loan.user.email),
            device=DeviceSummary(
                id=loan.device.id,
                name=loan.device.name,
                serial_number=loan.device.serial_number,
                device_type=loan.device.device_type,
            ),
        )
        for loan in loans
    ]


def return_loan(db: Session, loan_id: int) -> Loan:
    loan = db.query(Loan).options(joinedload(Loan.device)).filter(Loan.id == loan_id).first()
    if not loan:
        raise LookupError(f"Préstamo con id={loan_id} no encontrado.")
    if loan.status == "returned":
        raise ValueError(f"El préstamo con id={loan_id} ya fue devuelto.")

    loan.status = "returned"
    loan.return_date = datetime.utcnow()
    loan.device.is_available = True
    db.commit()
    db.refresh(loan)
    return loan


def get_loans_by_user(db: Session, user_id: int) -> List[Loan]:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise LookupError(f"Usuario con id={user_id} no encontrado.")
    return db.query(Loan).filter(Loan.user_id == user_id).all()


def get_loans_by_device(db: Session, device_id: int) -> List[Loan]:
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise LookupError(f"Dispositivo con id={device_id} no encontrado.")
    return db.query(Loan).filter(Loan.device_id == device_id).all()
