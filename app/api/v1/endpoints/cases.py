from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud import crud
from app.schemas import schemas
from app.core.database import get_db

router = APIRouter()


@router.get("/", response_model=List[schemas.Case])
def read_cases(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve cases.
    """
    cases = crud.case.get_multi(db, skip=skip, limit=limit)
    return cases


@router.post("/", response_model=schemas.Case)
def create_case(
    *,
    db: Session = Depends(get_db),
    case_in: schemas.CaseCreate,
) -> Any:
    """
    Create new case.
    """
    case = crud.case.get_by_slug(db, slug=case_in.slug)
    if case:
        raise HTTPException(
            status_code=400,
            detail="The case with this slug already exists in the system.",
        )
    case = crud.case.create(db, obj_in=case_in)
    return case


@router.put("/{id}", response_model=schemas.Case)
def update_case(
    *,
    db: Session = Depends(get_db),
    id: int,
    case_in: schemas.CaseUpdate,
) -> Any:
    """
    Update a case.
    """
    case = crud.case.get(db, id=id)
    if not case:
        raise HTTPException(
            status_code=404,
            detail="Case not found",
        )
    case = crud.case.update(db, db_obj=case, obj_in=case_in)
    return case


@router.get("/{id}", response_model=schemas.Case)
def read_case(
    *,
    db: Session = Depends(get_db),
    id: int,
) -> Any:
    """
    Get case by ID.
    """
    case = crud.case.get(db, id=id)
    if not case:
        raise HTTPException(
            status_code=404,
            detail="Case not found",
        )
    return case


@router.delete("/{id}", response_model=schemas.Case)
def delete_case(
    *,
    db: Session = Depends(get_db),
    id: int,
) -> Any:
    """
    Delete a case.
    """
    case = crud.case.get(db, id=id)
    if not case:
        raise HTTPException(
            status_code=404,
            detail="Case not found",
        )
    case = crud.case.remove(db, id=id)
    return case
