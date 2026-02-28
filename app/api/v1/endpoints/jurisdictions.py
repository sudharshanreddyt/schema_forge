from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud import crud
from app.schemas import schemas
from app.core.database import get_db

router = APIRouter()


@router.get("/", response_model=List[schemas.Jurisdiction])
def read_jurisdictions(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    return crud.jurisdiction.get_multi(db, skip=skip, limit=limit)


@router.post("/", response_model=schemas.Jurisdiction)
def create_jurisdiction(
    *,
    db: Session = Depends(get_db),
    jurisdiction_in: schemas.JurisdictionCreate,
) -> Any:
    return crud.jurisdiction.create(db, obj_in=jurisdiction_in)


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
