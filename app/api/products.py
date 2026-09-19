from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth.current_user import get_current_user
from app.db.models import Idea, Product, User
from app.db.session import get_db
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate
from app.tenants.context import CurrentOrganization


router = APIRouter(prefix="/products", tags=["Products"])


@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    data: ProductCreate,
    organization: CurrentOrganization,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if data.idea_id is not None:
        idea = db.scalar(
            select(Idea).where(
                Idea.id == data.idea_id,
                Idea.organization_id == organization.id,
            )
        )

        if idea is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Idea not found",
            )

    product = Product(
        organization_id=organization.id,
        idea_id=data.idea_id,
        name=data.name,
        slug=data.slug,
        description=data.description,
        product_type=data.product_type,
        studio=data.studio,
        status=data.status,
    )

    db.add(product)
    db.commit()
    db.refresh(product)

    return product


@router.get("", response_model=list[ProductResponse])
def list_products(
    organization: CurrentOrganization,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    result = db.execute(
        select(Product)
        .where(Product.organization_id == organization.id)
        .order_by(Product.created_at.desc())
    )

    return result.scalars().all()


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: int,
    organization: CurrentOrganization,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    product = db.scalar(
        select(Product).where(
            Product.id == product_id,
            Product.organization_id == organization.id,
        )
    )

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    return product


@router.patch("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    data: ProductUpdate,
    organization: CurrentOrganization,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    product = db.scalar(
        select(Product).where(
            Product.id == product_id,
            Product.organization_id == organization.id,
        )
    )

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    if data.idea_id is not None:
        idea = db.scalar(
            select(Idea).where(
                Idea.id == data.idea_id,
                Idea.organization_id == organization.id,
            )
        )

        if idea is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Idea not found",
            )

    updates = data.model_dump(exclude_unset=True)

    for field, value in updates.items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)

    return product