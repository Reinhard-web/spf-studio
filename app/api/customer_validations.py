from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth.current_user import get_current_user
from app.tenants.context import CurrentOrganization
from app.db.session import get_db
from app.models.customer_validation import CustomerValidation
from app.models.experiment import Experiment
from app.models.user import User
from app.schemas.customer_validation import (
    CustomerValidationCreate,
    CustomerValidationResponse,
    CustomerValidationUpdate,
)

router = APIRouter(
    prefix="/innovation/customer-validations",
    tags=["Customer Validation"],
)


@router.post(
    "",
    response_model=CustomerValidationResponse,
)
def create_customer_validation(
    data: CustomerValidationCreate,
    organization: CurrentOrganization,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if data.experiment_id is not None:
        experiment = db.scalar(
            select(Experiment).where(
                Experiment.id == data.experiment_id,
                Experiment.organization_id == organization.id,
            )
        )

        if experiment is None:
            raise HTTPException(
                status_code=404,
                detail="Experiment not found",
            )

    validation = CustomerValidation(
        organization_id=organization.id,
        experiment_id=data.experiment_id,
        title=data.title,
        participant_type=data.participant_type,
        participant_count=data.participant_count,
        method=data.method,
        objective=data.objective,
        findings=data.findings,
        customer_feedback=data.customer_feedback,
        validation_result=data.validation_result,
        notes=data.notes,
        validated_at=data.validated_at,
    )

    db.add(validation)
    db.commit()
    db.refresh(validation)

    return validation


@router.get(
    "",
    response_model=list[CustomerValidationResponse],
)
def list_customer_validations(
    organization: CurrentOrganization,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return db.scalars(
        select(CustomerValidation)
        .where(CustomerValidation.organization_id == organization.id)
        .order_by(CustomerValidation.id)
    ).all()


@router.get(
    "/{validation_id}",
    response_model=CustomerValidationResponse,
)
def get_customer_validation(
    validation_id: int,
    organization: CurrentOrganization,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    validation = db.scalar(
        select(CustomerValidation).where(
            CustomerValidation.id == validation_id,
            CustomerValidation.organization_id == organization.id,
        )
    )

    if validation is None:
        raise HTTPException(
            status_code=404,
            detail="Customer validation not found",
        )

    return validation


@router.patch(
    "/{validation_id}",
    response_model=CustomerValidationResponse,
)
def update_customer_validation(
    validation_id: int,
    data: CustomerValidationUpdate,
    organization: CurrentOrganization,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    validation = db.scalar(
        select(CustomerValidation).where(
            CustomerValidation.id == validation_id,
            CustomerValidation.organization_id == organization.id,
        )
    )

    if validation is None:
        raise HTTPException(
            status_code=404,
            detail="Customer validation not found",
        )

    updates = data.model_dump(exclude_unset=True)

    for field, value in updates.items():
        setattr(validation, field, value)

    db.commit()
    db.refresh(validation)

    return validation
