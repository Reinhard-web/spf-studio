from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth.current_user import get_current_user
from app.db.models import Evidence, Experiment, User
from app.db.session import get_db
from app.schemas.evidence import EvidenceCreate, EvidenceResponse, EvidenceUpdate
from app.tenants.context import CurrentOrganization

router = APIRouter(
    prefix="/innovation/evidence",
    tags=["Innovation - Evidence"],
)


@router.post(
    "",
    response_model=EvidenceResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_evidence(
    data: EvidenceCreate,
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
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Experiment not found in this organization",
            )

    evidence = Evidence(
        organization_id=organization.id,
        experiment_id=data.experiment_id,
        title=data.title,
        description=data.description,
        evidence_type=data.evidence_type,
        source_type=data.source_type,
        source_reference=data.source_reference,
        status=data.status,
        observed_at=data.observed_at,
    )

    db.add(evidence)
    db.commit()
    db.refresh(evidence)

    return evidence


@router.get(
    "",
    response_model=list[EvidenceResponse],
)
def list_evidence(
    organization: CurrentOrganization,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    result = db.execute(
        select(Evidence)
        .where(Evidence.organization_id == organization.id)
        .order_by(Evidence.created_at.desc())
    )

    return result.scalars().all()


@router.get(
    "/{evidence_id}",
    response_model=EvidenceResponse,
)
def get_evidence(
    evidence_id: int,
    organization: CurrentOrganization,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    evidence = db.scalar(
        select(Evidence).where(
            Evidence.id == evidence_id,
            Evidence.organization_id == organization.id,
        )
    )

    if evidence is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evidence not found",
        )

    return evidence


@router.patch(
    "/{evidence_id}",
    response_model=EvidenceResponse,
)
def update_evidence(
    evidence_id: int,
    data: EvidenceUpdate,
    organization: CurrentOrganization,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    evidence = db.scalar(
        select(Evidence).where(
            Evidence.id == evidence_id,
            Evidence.organization_id == organization.id,
        )
    )

    if evidence is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evidence not found",
        )

    updates = data.model_dump(exclude_unset=True)

    for field, value in updates.items():
        setattr(evidence, field, value)

    db.commit()
    db.refresh(evidence)

    return evidence