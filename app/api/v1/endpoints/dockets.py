from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.crud import crud
from app.schemas import schemas
from app.core.database import get_db

router = APIRouter()


@router.get("/", response_model=List[schemas.Docket])
def read_dockets(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 3,
) -> Any:
    return crud.docket.get_multi(db, skip=skip, limit=limit)


@router.get("/search/", response_model=List[schemas.Docket])
def search_dockets(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 3,
    docket_id: Optional[int] = None,
    case_id: Optional[int] = None,
    court: Optional[str] = None,
    docket_number: Optional[str] = None,
) -> Any:
    """
    Search dockets with filters.
    """
    filters = {
        "docket_id": docket_id,
        "case_id": case_id,
        "court": court,
        "docket_number": docket_number,
    }
    return crud.docket.get_multi_filtered(db, skip=skip, limit=limit, **filters)


@router.post("/", response_model=schemas.Docket)
def create_docket(
    *,
    db: Session = Depends(get_db),
    docket_in: schemas.DocketCreate,
) -> Any:
    try:
        return crud.docket.create(db, obj_in=docket_in)
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Integrity Error: {str(e.orig) if hasattr(e, 'orig') else str(e)}"
        )


@router.get("/{id}", response_model=schemas.Docket)
def read_docket(
    *,
    db: Session = Depends(get_db),
    id: int,
) -> Any:
    docket = crud.docket.get(db, id=id)
    if not docket:
        raise HTTPException(status_code=404, detail="Docket not found")
    return docket


@router.put("/{id}", response_model=schemas.Docket)
def update_docket(
    *,
    db: Session = Depends(get_db),
    id: int,
    docket_in: schemas.DocketUpdate,
) -> Any:
    docket = crud.docket.get(db, id=id)
    if not docket:
        raise HTTPException(status_code=404, detail="Docket not found")
    try:
        return crud.docket.update(db, db_obj=docket, obj_in=docket_in)
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Integrity Error: {str(e.orig) if hasattr(e, 'orig') else str(e)}"
        )


    try:
        crud.docket.remove(db, id=id)
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Integrity Error: {str(e.orig) if hasattr(e, 'orig') else str(e)}"
        )
    return {"message": "Docket deleted successfully", "id": id}
