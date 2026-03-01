from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.crud import crud
from app.schemas import schemas
from app.core.database import get_db

router = APIRouter()


@router.get("/", response_model=List[schemas.Jurisdiction])
def read_jurisdictions(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 3,
) -> Any:
    return crud.jurisdiction.get_multi(db, skip=skip, limit=limit)


@router.get("/search/", response_model=List[schemas.Jurisdiction])
def search_jurisdictions(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 3,
    jurisdiction_id: Optional[int] = None,
    court_name: Optional[str] = None,
    jurisdiction_type: Optional[str] = None,
    jurisdiction_name: Optional[str] = None,
) -> Any:
    """
    Search jurisdictions with filters.
    """
    filters = {
        "jurisdiction_id": jurisdiction_id,
        "court_name": court_name,
        "jurisdiction_type": jurisdiction_type,
        "jurisdiction_name": jurisdiction_name,
    }
    return crud.jurisdiction.get_multi_filtered(db, skip=skip, limit=limit, **filters)


@router.post("/", response_model=schemas.Jurisdiction)
def create_jurisdiction(
    *,
    db: Session = Depends(get_db),
    jurisdiction_in: schemas.JurisdictionCreate,
) -> Any:
    try:
        return crud.jurisdiction.create(db, obj_in=jurisdiction_in)
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Integrity Error: {str(e.orig) if hasattr(e, 'orig') else str(e)}"
        )


@router.get("/{id}", response_model=schemas.Jurisdiction)
def read_jurisdiction(
    *,
    db: Session = Depends(get_db),
    id: int,
) -> Any:
    jurisdiction = crud.jurisdiction.get(db, id=id)
    if not jurisdiction:
        raise HTTPException(status_code=404, detail="Jurisdiction not found")
    return jurisdiction
