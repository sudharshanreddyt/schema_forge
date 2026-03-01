from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List, Optional, Generic, TypeVar, Type, Any
from pydantic import BaseModel

from app.models import models
from app.schemas import schemas

# --- Generic CRUD ---
ModelType = TypeVar("ModelType", bound=Any)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(getattr(self.model, f"{self.model.__tablename__[:-1]}_id") == id).first()

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 3) -> List[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def get_multi_filtered(
        self, db: Session, *, skip: int = 0, limit: int = 3, **filters: Any
    ) -> List[ModelType]:
        query = db.query(self.model)
        for field, value in filters.items():
            if value is not None:
                if isinstance(value, str):
                    query = query.filter(getattr(self.model, field).ilike(f"%{value}%"))
                else:
                    query = query.filter(getattr(self.model, field) == value)
        return query.offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = obj_in.model_dump()
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, db_obj: ModelType, obj_in: UpdateSchemaType) -> ModelType:
        obj_data = db_obj.__dict__
        update_data = obj_in.model_dump(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj


# --- Specialized CRUD for Case (to handle relationships) ---

class CRUDCase(CRUDBase[models.Case, schemas.CaseCreate, schemas.CaseUpdate]):
    def create(self, db: Session, *, obj_in: schemas.CaseCreate) -> models.Case:
        obj_in_data = obj_in.model_dump(exclude={
            "area_ids", "issue_ids", "cause_ids", "algorithm_ids", "organization_ids"
        })
        db_obj = models.Case(**obj_in_data)
        
        # Add relationships
        if obj_in.area_ids:
            db_obj.areas = db.query(models.AreaOfApplication).filter(models.AreaOfApplication.area_id.in_(obj_in.area_ids)).all()
        if obj_in.issue_ids:
            db_obj.issues = db.query(models.Issue).filter(models.Issue.issue_id.in_(obj_in.issue_ids)).all()
        if obj_in.cause_ids:
            db_obj.causes = db.query(models.CauseOfAction).filter(models.CauseOfAction.cause_id.in_(obj_in.cause_ids)).all()
        if obj_in.algorithm_ids:
            db_obj.algorithms = db.query(models.Algorithm).filter(models.Algorithm.algorithm_id.in_(obj_in.algorithm_ids)).all()
        if obj_in.organization_ids:
            db_obj.organizations = db.query(models.Organization).filter(models.Organization.organization_id.in_(obj_in.organization_ids)).all()

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, db_obj: models.Case, obj_in: schemas.CaseUpdate) -> models.Case:
        update_data = obj_in.model_dump(exclude_unset=True)
        
        # Handle taxonomy relationships separately
        if "area_ids" in update_data:
            area_ids = update_data.pop("area_ids")
            if area_ids is not None:
                db_obj.areas = db.query(models.AreaOfApplication).filter(models.AreaOfApplication.area_id.in_(area_ids)).all()
        
        if "issue_ids" in update_data:
            issue_ids = update_data.pop("issue_ids")
            if issue_ids is not None:
                db_obj.issues = db.query(models.Issue).filter(models.Issue.issue_id.in_(issue_ids)).all()

        if "cause_ids" in update_data:
            cause_ids = update_data.pop("cause_ids")
            if cause_ids is not None:
                db_obj.causes = db.query(models.CauseOfAction).filter(models.CauseOfAction.cause_id.in_(cause_ids)).all()

        if "algorithm_ids" in update_data:
            algorithm_ids = update_data.pop("algorithm_ids")
            if algorithm_ids is not None:
                db_obj.algorithms = db.query(models.Algorithm).filter(models.Algorithm.algorithm_id.in_(algorithm_ids)).all()

        if "organization_ids" in update_data:
            organization_ids = update_data.pop("organization_ids")
            if organization_ids is not None:
                db_obj.organizations = db.query(models.Organization).filter(models.Organization.organization_id.in_(organization_ids)).all()

        return super().update(db, db_obj=db_obj, obj_in=schemas.CaseUpdate(**update_data))

    def get_by_slug(self, db: Session, slug: str) -> Optional[models.Case]:
        return db.query(models.Case).filter(models.Case.slug == slug).first()


# --- Instantiate CRUD objects ---

case = CRUDCase(models.Case)
jurisdiction = CRUDBase[models.Jurisdiction, schemas.JurisdictionCreate, schemas.JurisdictionUpdate](models.Jurisdiction)
docket = CRUDBase[models.Docket, schemas.DocketCreate, schemas.DocketUpdate](models.Docket)
document = CRUDBase[models.Document, schemas.DocumentCreate, schemas.DocumentUpdate](models.Document)
secondary_source = CRUDBase[models.SecondarySource, schemas.SecondarySourceCreate, schemas.SecondarySourceUpdate](models.SecondarySource)

# Taxonomy CRUDs
area = CRUDBase[models.AreaOfApplication, schemas.TaxonomyCreate, schemas.TaxonomyUpdate](models.AreaOfApplication)
issue = CRUDBase[models.Issue, schemas.TaxonomyCreate, schemas.TaxonomyUpdate](models.Issue)
cause = CRUDBase[models.CauseOfAction, schemas.TaxonomyCreate, schemas.TaxonomyUpdate](models.CauseOfAction)
algorithm = CRUDBase[models.Algorithm, schemas.TaxonomyCreate, schemas.TaxonomyUpdate](models.Algorithm)
organization = CRUDBase[models.Organization, schemas.TaxonomyCreate, schemas.TaxonomyUpdate](models.Organization)
