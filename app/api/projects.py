from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth.current_user import get_current_user
from app.db.models import Product, Project, User
from app.db.session import get_db
from app.schemas.project import ProjectCreate, ProjectResponse, ProjectUpdate
from app.tenants.context import CurrentOrganization


router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(
    data: ProjectCreate,
    organization: CurrentOrganization,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    product = db.scalar(
        select(Product).where(
            Product.id == data.product_id,
            Product.organization_id == organization.id,
        )
    )

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    project = Project(
        organization_id=organization.id,
        product_id=data.product_id,
        name=data.name,
        slug=data.slug,
        description=data.description,
        project_type=data.project_type,
        status=data.status,
        repository_url=data.repository_url,
        environment=data.environment,
        current_version=data.current_version,
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    return project


@router.get("", response_model=list[ProjectResponse])
def list_projects(
    organization: CurrentOrganization,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    result = db.execute(
        select(Project)
        .where(Project.organization_id == organization.id)
        .order_by(Project.created_at.desc())
    )

    return result.scalars().all()


@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(
    project_id: int,
    organization: CurrentOrganization,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    project = db.scalar(
        select(Project).where(
            Project.id == project_id,
            Project.organization_id == organization.id,
        )
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    return project


@router.patch("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: int,
    data: ProjectUpdate,
    organization: CurrentOrganization,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    project = db.scalar(
        select(Project).where(
            Project.id == project_id,
            Project.organization_id == organization.id,
        )
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    if data.product_id is not None:
        product = db.scalar(
            select(Product).where(
                Product.id == data.product_id,
                Product.organization_id == organization.id,
            )
        )

        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found",
            )

    updates = data.model_dump(exclude_unset=True)

    for field, value in updates.items():
        setattr(project, field, value)

    db.commit()
    db.refresh(project)

    return project