from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.crud import crud
from app.schemas import schemas
from app.core.database import get_db

router = APIRouter()

# --- Areas of Application ---

@router.get("/areas/", response_model=List[schemas.AreaOfApplication], tags=["taxonomies"])
def read_areas(db: Session = Depends(get_db), skip: int = 0, limit: int = 100) -> Any:
    return crud.area.get_multi(db, skip=skip, limit=limit)

@router.post("/areas/", response_model=schemas.AreaOfApplication, tags=["taxonomies"])
def create_area(*, db: Session = Depends(get_db), area_in: schemas.TaxonomyCreate) -> Any:
    try:
        return crud.area.create(db, obj_in=area_in)
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Integrity Error: {str(e.orig) if hasattr(e, 'orig') else str(e)}"
        )

# --- Issues ---

@router.get("/issues/", response_model=List[schemas.Issue], tags=["taxonomies"])
def read_issues(db: Session = Depends(get_db), skip: int = 0, limit: int = 100) -> Any:
    return crud.issue.get_multi(db, skip=skip, limit=limit)

@router.post("/issues/", response_model=schemas.Issue, tags=["taxonomies"])
def create_issue(*, db: Session = Depends(get_db), issue_in: schemas.TaxonomyCreate) -> Any:
    try:
        return crud.issue.create(db, obj_in=issue_in)
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Integrity Error: {str(e.orig) if hasattr(e, 'orig') else str(e)}"
        )

# --- Causes of Action ---

@router.get("/causes/", response_model=List[schemas.CauseOfAction], tags=["taxonomies"])
def read_causes(db: Session = Depends(get_db), skip: int = 0, limit: int = 100) -> Any:
    return crud.cause.get_multi(db, skip=skip, limit=limit)

@router.post("/causes/", response_model=schemas.CauseOfAction, tags=["taxonomies"])
def create_cause(*, db: Session = Depends(get_db), cause_in: schemas.TaxonomyCreate) -> Any:
    try:
        return crud.cause.create(db, obj_in=cause_in)
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Integrity Error: {str(e.orig) if hasattr(e, 'orig') else str(e)}"
        )

# --- Algorithms ---

@router.get("/algorithms/", response_model=List[schemas.Algorithm], tags=["taxonomies"])
def read_algorithms(db: Session = Depends(get_db), skip: int = 0, limit: int = 100) -> Any:
    return crud.algorithm.get_multi(db, skip=skip, limit=limit)

@router.post("/algorithms/", response_model=schemas.Algorithm, tags=["taxonomies"])
def create_algorithm(*, db: Session = Depends(get_db), algorithm_in: schemas.TaxonomyCreate) -> Any:
    try:
        return crud.algorithm.create(db, obj_in=algorithm_in)
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Integrity Error: {str(e.orig) if hasattr(e, 'orig') else str(e)}"
        )

# --- Organizations ---

@router.get("/organizations/", response_model=List[schemas.Organization], tags=["taxonomies"])
def read_organizations(db: Session = Depends(get_db), skip: int = 0, limit: int = 100) -> Any:
    return crud.organization.get_multi(db, skip=skip, limit=limit)

@router.post("/organizations/", response_model=schemas.Organization, tags=["taxonomies"])
def create_organization(*, db: Session = Depends(get_db), org_in: schemas.TaxonomyCreate) -> Any:
    try:
        return crud.organization.create(db, obj_in=org_in)
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Integrity Error: {str(e.orig) if hasattr(e, 'orig') else str(e)}"
        )
