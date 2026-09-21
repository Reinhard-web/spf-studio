from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.build import Build
from app.models.deployment import Deployment


def execute_deployment(
    deployment: Deployment,
    db: Session,
) -> Deployment:
    build = db.scalar(
        select(Build).where(
            Build.id == deployment.build_id,
            Build.organization_id == deployment.organization_id,
        )
    )

    if not build:
        deployment.status = "failed"
        deployment.error_message = "Build not found"
        deployment.completed_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(deployment)
        return deployment

    deployment.status = "deploying"
    deployment.started_at = datetime.now(timezone.utc)
    deployment.error_message = None

    db.commit()
    db.refresh(deployment)

    # Temporary execution layer.
    # A real deployment provider will be connected here later.
    deployment.status = "deployed"
    deployment.url = build.preview_url
    deployment.logs = (
        f"Deployment executed successfully for build {build.id}."
    )
    deployment.completed_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(deployment)

    return deployment