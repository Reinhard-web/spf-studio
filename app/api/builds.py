from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth.current_user import get_current_user
from app.db.models import Build, Project, User
from app.db.session import get_db
from app.schemas.build import BuildCreate, BuildResponse, BuildUpdate
from app.tenants.context import CurrentOrganization

router = APIRouter(prefix="/builds", tags=["Builds"])


@router.post("", response_model=BuildResponse, status_code=status.HTTP_201_CREATED)
def create_build(
    data: BuildCreate,
    organization: CurrentOrganization,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    project = db.scalar(
        select(Project).where(
            Project.id == data.project_id,
            Project.organization_id == organization.id,
        )
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    build = Build(
        organization_id=organization.id,
        project_id=data.project_id,
        name=data.name,
        version=data.version,
        build_number=data.build_number,
        status=data.status,
        environment=data.environment,
        branch=data.branch,
        commit_sha=data.commit_sha,
        preview_url=data.preview_url,
        logs=data.logs,
        started_at=data.started_at,
        completed_at=data.completed_at,
    )

    db.add(build)
    db.commit()
    db.refresh(build)

    return build


@router.get("", response_model=list[BuildResponse])
def list_builds(
    organization: CurrentOrganization,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    result = db.execute(
        select(Build)
        .where(Build.organization_id == organization.id)
        .order_by(Build.created_at.desc())
    )

    return result.scalars().all()


@router.get("/{build_id}", response_model=BuildResponse)
def get_build(
    build_id: int,
    organization: CurrentOrganization,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    build = db.scalar(
        select(Build).where(
            Build.id == build_id,
            Build.organization_id == organization.id,
        )
    )

    if build is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Build not found",
        )

    return build


@router.patch("/{build_id}", response_model=BuildResponse)
def update_build(
    build_id: int,
    data: BuildUpdate,
    organization: CurrentOrganization,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    build = db.scalar(
        select(Build).where(
            Build.id == build_id,
            Build.organization_id == organization.id,
        )
    )

    if build is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Build not found",
        )

    if data.project_id is not None:
        project = db.scalar(
            select(Project).where(
                Project.id == data.project_id,
                Project.organization_id == organization.id,
            )
        )

        if project is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found",
            )

    updates = data.model_dump(exclude_unset=True)

    for field, value in updates.items():
        setattr(build, field, value)

    db.commit()
    db.refresh(build)

    return build