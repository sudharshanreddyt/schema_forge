from datetime import date
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, HttpUrl


# --- Taxonomy Schemas ---

class TaxonomyBase(BaseModel):
    name: str

class TaxonomyCreate(TaxonomyBase):
    pass

class TaxonomyUpdate(BaseModel):
    name: Optional[str] = None

class Taxonomy(TaxonomyBase):
    model_config = ConfigDict(from_attributes=True)

class AreaOfApplication(Taxonomy):
    area_id: int

class Issue(Taxonomy):
    issue_id: int

class CauseOfAction(Taxonomy):
    cause_id: int

class Algorithm(Taxonomy):
    algorithm_id: int

class Organization(Taxonomy):
    organization_id: int


# --- Secondary Source Schemas ---

class SecondarySourceBase(BaseModel):
    title: str
    link: Optional[str] = None

class SecondarySourceCreate(SecondarySourceBase):
    case_id: int

class SecondarySourceUpdate(BaseModel):
    title: Optional[str] = None
    link: Optional[str] = None

class SecondarySource(SecondarySourceBase):
    source_id: int
    case_id: int
    model_config = ConfigDict(from_attributes=True)


# --- Document Schemas ---

class DocumentBase(BaseModel):
    document_type: str
    filing_date: Optional[date] = None
    link: Optional[str] = None
    citation: Optional[str] = None

class DocumentCreate(DocumentBase):
    docket_id: int

class DocumentUpdate(BaseModel):
    document_type: Optional[str] = None
    filing_date: Optional[date] = None
    link: Optional[str] = None
    citation: Optional[str] = None

class Document(DocumentBase):
    document_id: int
    docket_id: int
    model_config = ConfigDict(from_attributes=True)


# --- Docket Schemas ---

class DocketBase(BaseModel):
    court: Optional[str] = None
    docket_number: Optional[str] = None
    link: Optional[str] = None

class DocketCreate(DocketBase):
    case_id: int

class DocketUpdate(BaseModel):
    court: Optional[str] = None
    docket_number: Optional[str] = None
    link: Optional[str] = None

class Docket(DocketBase):
    docket_id: int
    case_id: int
    documents: List[Document] = []
    model_config = ConfigDict(from_attributes=True)


# --- Jurisdiction Schemas ---

class JurisdictionBase(BaseModel):
    court_name: Optional[str] = None
    jurisdiction_type: Optional[str] = None
    jurisdiction_name: Optional[str] = None

class JurisdictionCreate(JurisdictionBase):
    pass

class JurisdictionUpdate(BaseModel):
    court_name: Optional[str] = None
    jurisdiction_type: Optional[str] = None
    jurisdiction_name: Optional[str] = None

class Jurisdiction(JurisdictionBase):
    jurisdiction_id: int
    model_config = ConfigDict(from_attributes=True)


# --- Case Schemas ---

class CaseBase(BaseModel):
    slug: str
    record_number: Optional[int] = None
    caption: Optional[str] = None
    brief_description: Optional[str] = None
    filing_date: Optional[date] = None
    status_disposition: Optional[str] = None
    published_opinion_flag: Optional[bool] = None
    class_action_status: Optional[str] = None
    researcher: Optional[str] = None
    summary_of_significance: Optional[str] = None
    summary_facts_activity: Optional[str] = None
    most_recent_activity: Optional[str] = None
    most_recent_activity_date: Optional[date] = None
    date_added: Optional[date] = None
    last_update: Optional[date] = None
    jurisdiction_id: Optional[int] = None

class CaseCreate(CaseBase):
    area_ids: List[int] = []
    issue_ids: List[int] = []
    cause_ids: List[int] = []
    algorithm_ids: List[int] = []
    organization_ids: List[int] = []

class CaseUpdate(BaseModel):
    slug: Optional[str] = None
    record_number: Optional[int] = None
    caption: Optional[str] = None
    brief_description: Optional[str] = None
    filing_date: Optional[date] = None
    status_disposition: Optional[str] = None
    published_opinion_flag: Optional[bool] = None
    class_action_status: Optional[str] = None
    researcher: Optional[str] = None
    summary_of_significance: Optional[str] = None
    summary_facts_activity: Optional[str] = None
    most_recent_activity: Optional[str] = None
    most_recent_activity_date: Optional[date] = None
    date_added: Optional[date] = None
    last_update: Optional[date] = None
    jurisdiction_id: Optional[int] = None
    
    area_ids: Optional[List[int]] = None
    issue_ids: Optional[List[int]] = None
    cause_ids: Optional[List[int]] = None
    algorithm_ids: Optional[List[int]] = None
    organization_ids: Optional[List[int]] = None

class Case(CaseBase):
    case_id: int
    jurisdiction: Optional[Jurisdiction] = None
    dockets: List[Docket] = []
    secondary_sources: List[SecondarySource] = []
    
    areas: List[AreaOfApplication] = []
    issues: List[Issue] = []
    causes: List[CauseOfAction] = []
    algorithms: List[Algorithm] = []
    organizations: List[Organization] = []
    
    model_config = ConfigDict(from_attributes=True)
