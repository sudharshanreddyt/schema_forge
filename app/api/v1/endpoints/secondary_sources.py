from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud import crud
from app.schemas import schemas
from app.core.database import get_db

router = APIRouter()


@router.get("/", response_model=List[schemas.SecondarySource])
def read_secondary_sources(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    return crud.secondary_source.get_multi(db, skip=skip, limit=limit)


@router.post("/", response_model=schemas.SecondarySource)
def create_secondary_source(
    *,
    db: Session = Depends(get_db),
    source_in: schemas.SecondarySourceCreate,
) -> Any:
    return crud.secondary_source.create(db, obj_in=source_in)


@router.get("/{id}", response_model=schemas.SecondarySource)
def read_secondary_source(
    *,
    db: Session = Depends(get_db),
    id: int,
) -> Any:
    source = crud.secondary_source.get(db, id=id)
    if not source:
        raise HTTPException(status_code=404, detail="Secondary source not found")
    return source


@router.put("/{id}", response_model=schemas.SecondarySource)
def update_secondary_source(
    *,
    db: Session = Depends(get_db),
    id: int,
    source_in: schemas.SecondarySourceUpdate,
) -> Any:
    source = crud.secondary_source.get(db, id=id)
    if not source:
        raise HTTPException(status_code=404, detail="Secondary source not found")
    return crud.secondary_source.update(db, db_obj=source, obj_in=source_in)


@router.delete("/{id}", response_model=schemas.SecondarySource)
def delete_secondary_source(
    *,
    db: Session = Depends(get_db),
    id: int,
) -> Any:
    source = crud.secondary_source.get(db, id=id)
    if not source:
        raise HTTPException(status_code=404, detail="Secondary source not found")
    return crud.secondary_source.remove(db, id=id)
