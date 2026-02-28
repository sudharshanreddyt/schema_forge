from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud import crud
from app.schemas import schemas
from app.core.database import get_db

router = APIRouter()


@router.get("/", response_model=List[schemas.Docket])
def read_dockets(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    return crud.docket.get_multi(db, skip=skip, limit=limit)


@router.post("/", response_model=schemas.Docket)
def create_docket(
    *,
    db: Session = Depends(get_db),
    docket_in: schemas.DocketCreate,
) -> Any:
    return crud.docket.create(db, obj_in=docket_in)


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
    return crud.docket.update(db, db_obj=docket, obj_in=docket_in)


@router.delete("/{id}", response_model=schemas.Docket)
def delete_docket(
    *,
    db: Session = Depends(get_db),
    id: int,
) -> Any:
    docket = crud.docket.get(db, id=id)
    if not docket:
        raise HTTPException(status_code=404, detail="Docket not found")
    return crud.docket.remove(db, id=id)
