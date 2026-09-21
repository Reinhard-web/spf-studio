from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth.current_user import get_current_user
from app.db.models import Build, Test, User
from app.db.session import get_db
from app.schemas.test import TestCreate, TestResponse, TestUpdate
from app.tenants.context import CurrentOrganization


router = APIRouter(prefix="/tests", tags=["Tests"])


@router.post("", response_model=TestResponse, status_code=status.HTTP_201_CREATED)
def create_test(
    data: TestCreate,
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

    test = Test(
        organization_id=organization.id,
        build_id=data.build_id,
        name=data.name,
        test_type=data.test_type,
        status=data.status,
        environment=data.environment,
        command=data.command,
        results=data.results,
        logs=data.logs,
        started_at=data.started_at,
        completed_at=data.completed_at,
    )

    db.add(test)
    db.commit()
    db.refresh(test)

    return test


@router.get("", response_model=list[TestResponse])
def list_tests(
    organization: CurrentOrganization,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    result = db.execute(
        select(Test)
        .where(Test.organization_id == organization.id)
        .order_by(Test.created_at.desc())
    )

    return result.scalars().all()


@router.get("/{test_id}", response_model=TestResponse)
def get_test(
    test_id: int,
    organization: CurrentOrganization,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    test = db.scalar(
        select(Test).where(
            Test.id == test_id,
            Test.organization_id == organization.id,
        )
    )

    if test is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Test not found",
        )

    return test


@router.patch("/{test_id}", response_model=TestResponse)
def update_test(
    test_id: int,
    data: TestUpdate,
    organization: CurrentOrganization,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    test = db.scalar(
        select(Test).where(
            Test.id == test_id,
            Test.organization_id == organization.id,
        )
    )

    if test is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Test not found",
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
        setattr(test, field, value)

    db.commit()
    db.refresh(test)

    return test