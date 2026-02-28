from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud import crud
from app.schemas import schemas
from app.core.database import get_db

router = APIRouter()


@router.get("/", response_model=List[schemas.Document])
def read_documents(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    return crud.document.get_multi(db, skip=skip, limit=limit)


@router.post("/", response_model=schemas.Document)
def create_document(
    *,
    db: Session = Depends(get_db),
    document_in: schemas.DocumentCreate,
) -> Any:
    return crud.document.create(db, obj_in=document_in)


@router.get("/{id}", response_model=schemas.Document)
def read_document(
    *,
    db: Session = Depends(get_db),
    id: int,
) -> Any:
    document = crud.document.get(db, id=id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document


@router.put("/{id}", response_model=schemas.Document)
def update_document(
    *,
    db: Session = Depends(get_db),
    id: int,
    document_in: schemas.DocumentUpdate,
) -> Any:
    document = crud.document.get(db, id=id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return crud.document.update(db, db_obj=document, obj_in=document_in)


@router.delete("/{id}", response_model=schemas.Document)
def delete_document(
    *,
    db: Session = Depends(get_db),
    id: int,
) -> Any:
    document = crud.document.get(db, id=id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return crud.document.remove(db, id=id)
