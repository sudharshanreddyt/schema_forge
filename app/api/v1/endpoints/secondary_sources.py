from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.crud import crud
from app.schemas import schemas
from app.core.database import get_db

router = APIRouter()


@router.get("/", response_model=List[schemas.SecondarySource])
def read_secondary_sources(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 3,
) -> Any:
    return crud.secondary_source.get_multi(db, skip=skip, limit=limit)


@router.get("/search/", response_model=List[schemas.SecondarySource])
def search_secondary_sources(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 3,
    source_id: Optional[int] = None,
    case_id: Optional[int] = None,
    title: Optional[str] = None,
) -> Any:
    """
    Search secondary sources with filters.
    """
    filters = {
        "source_id": source_id,
        "case_id": case_id,
        "title": title,
    }
    return crud.secondary_source.get_multi_filtered(db, skip=skip, limit=limit, **filters)


@router.post("/", response_model=schemas.SecondarySource)
def create_secondary_source(
    *,
    db: Session = Depends(get_db),
    source_in: schemas.SecondarySourceCreate,
) -> Any:
    try:
        return crud.secondary_source.create(db, obj_in=source_in)
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Integrity Error: {str(e.orig) if hasattr(e, 'orig') else str(e)}"
        )


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
    try:
        return crud.secondary_source.update(db, db_obj=source, obj_in=source_in)
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Integrity Error: {str(e.orig) if hasattr(e, 'orig') else str(e)}"
        )


    try:
        crud.secondary_source.remove(db, id=id)
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Integrity Error: {str(e.orig) if hasattr(e, 'orig') else str(e)}"
        )
    return {"message": "Secondary source deleted successfully", "id": id}
