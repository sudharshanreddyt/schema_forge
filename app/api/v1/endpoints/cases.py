from datetime import date
from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.crud import crud
from app.schemas import schemas
from app.core.database import get_db

router = APIRouter()


@router.get("/", response_model=List[schemas.Case])
def read_cases(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 3,
) -> Any:
    """
    Retrieve cases.
    """
    cases = crud.case.get_multi(db, skip=skip, limit=limit)
    return cases


@router.get("/search/", response_model=List[schemas.Case])
def search_cases(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 3,
    case_id: Optional[int] = None,
    slug: Optional[str] = None,
    record_number: Optional[int] = None,
    caption: Optional[str] = None,
    filing_date: Optional[date] = None,
    status_disposition: Optional[str] = None,
    published_opinion_flag: Optional[bool] = None,
    class_action_status: Optional[str] = None,
    researcher: Optional[str] = None,
    jurisdiction_id: Optional[int] = None,
    most_recent_activity_date: Optional[date] = None,
) -> Any:
    """
    Search cases with filters.
    """
    filters = {
        "case_id": case_id,
        "slug": slug,
        "record_number": record_number,
        "caption": caption,
        "filing_date": filing_date,
        "status_disposition": status_disposition,
        "published_opinion_flag": published_opinion_flag,
        "class_action_status": class_action_status,
        "researcher": researcher,
        "jurisdiction_id": jurisdiction_id,
        "most_recent_activity_date": most_recent_activity_date,
    }
    return crud.case.get_multi_filtered(db, skip=skip, limit=limit, **filters)


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
    try:
        case = crud.case.create(db, obj_in=case_in)
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Integrity Error: {str(e.orig) if hasattr(e, 'orig') else str(e)}"
        )
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
    try:
        case = crud.case.update(db, db_obj=case, obj_in=case_in)
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Integrity Error: {str(e.orig) if hasattr(e, 'orig') else str(e)}"
        )
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


@router.delete("/{id}")
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
    try:
        crud.case.remove(db, id=id)
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Integrity Error: {str(e.orig) if hasattr(e, 'orig') else str(e)}"
        )
    return {"message": "Case deleted successfully", "id": id}
