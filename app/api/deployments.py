from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth.current_user import get_current_user
from app.db.models import Build, Deployment, User
from app.db.session import get_db
from app.schemas.deployment import (
    DeploymentCreate,
    DeploymentResponse,
    DeploymentUpdate,
)
from app.services.deployment_service import execute_deployment
from app.tenants.context import CurrentOrganization

router = APIRouter(prefix="/deployments", tags=["Deployments"])


@router.post("", response_model=DeploymentResponse, status_code=status.HTTP_201_CREATED)
def create_deployment(
    data: DeploymentCreate,
    organization: CurrentOrganization,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    build = db.scalar(
        select(Build).where(
            Build.id == data.build_id,
            Build.organization_id == organization.id,
        )
    )

    if build is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Build not found",
        )

    deployment = Deployment(
        organization_id=organization.id,
        build_id=data.build_id,
        name=data.name,
        version=data.version,
        environment=data.environment,
        target=data.target,
        status=data.status,
        url=data.url,
        logs=data.logs,
        error_message=data.error_message,
        started_at=data.started_at,
        completed_at=data.completed_at,
    )

    db.add(deployment)
    db.commit()
    db.refresh(deployment)

    return deployment


@router.get("", response_model=list[DeploymentResponse])
def list_deployments(
    organization: CurrentOrganization,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    result = db.execute(
        select(Deployment)
        .where(Deployment.organization_id == organization.id)
        .order_by(Deployment.created_at.desc())
    )

    return result.scalars().all()


@router.get("/{deployment_id}", response_model=DeploymentResponse)
def get_deployment(
    deployment_id: int,
    organization: CurrentOrganization,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    deployment = db.scalar(
        select(Deployment).where(
            Deployment.id == deployment_id,
            Deployment.organization_id == organization.id,
        )
    )

    if deployment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deployment not found",
        )

    return deployment


@router.patch("/{deployment_id}", response_model=DeploymentResponse)
def update_deployment(
    deployment_id: int,
    data: DeploymentUpdate,
    organization: CurrentOrganization,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    deployment = db.scalar(
        select(Deployment).where(
            Deployment.id == deployment_id,
            Deployment.organization_id == organization.id,
        )
    )

    if deployment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deployment not found",
        )

    if data.build_id is not None:
        build = db.scalar(
            select(Build).where(
                Build.id == data.build_id,
                Build.organization_id == organization.id,
            )
        )

        if build is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Build not found",
            )

    updates = data.model_dump(exclude_unset=True)

    for field, value in updates.items():
        setattr(deployment, field, value)

    db.commit()
    db.refresh(deployment)


@router.post("/{deployment_id}/execute", response_model=DeploymentResponse)
def execute_deployment_api(
    deployment_id: int,
    current_organization: CurrentOrganization,
    db: Session = Depends(get_db),
):
    deployment = db.scalar(
        select(Deployment).where(
            Deployment.id == deployment_id,
            Deployment.organization_id == current_organization.id,
        )
    )

    if not deployment:
        raise HTTPException(status_code=404, detail="Deployment not found")

    return execute_deployment(deployment, db)