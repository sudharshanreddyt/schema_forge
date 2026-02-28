from sqlalchemy import (
    Column, Integer, String, Text, Boolean, Date, ForeignKey, Table, CheckConstraint
)
from sqlalchemy.orm import relationship
from app.core.database import Base

# Junction Tables
case_areas = Table(
    "case_areas",
    Base.metadata,
    Column("case_id", Integer, ForeignKey("cases.case_id", ondelete="CASCADE"), primary_key=True),
    Column("area_id", Integer, ForeignKey("areas_of_application.area_id", ondelete="CASCADE"), primary_key=True),
)

case_issues = Table(
    "case_issues",
    Base.metadata,
    Column("case_id", Integer, ForeignKey("cases.case_id", ondelete="CASCADE"), primary_key=True),
    Column("issue_id", Integer, ForeignKey("issues.issue_id", ondelete="CASCADE"), primary_key=True),
)

case_causes = Table(
    "case_causes",
    Base.metadata,
    Column("case_id", Integer, ForeignKey("cases.case_id", ondelete="CASCADE"), primary_key=True),
    Column("cause_id", Integer, ForeignKey("causes_of_action.cause_id", ondelete="CASCADE"), primary_key=True),
)

case_algorithms = Table(
    "case_algorithms",
    Base.metadata,
    Column("case_id", Integer, ForeignKey("cases.case_id", ondelete="CASCADE"), primary_key=True),
    Column("algorithm_id", Integer, ForeignKey("algorithms.algorithm_id", ondelete="CASCADE"), primary_key=True),
)

case_organizations = Table(
    "case_organizations",
    Base.metadata,
    Column("case_id", Integer, ForeignKey("cases.case_id", ondelete="CASCADE"), primary_key=True),
    Column("organization_id", Integer, ForeignKey("organizations.organization_id", ondelete="CASCADE"), primary_key=True),
)


class Jurisdiction(Base):
    __tablename__ = "jurisdictions"

    jurisdiction_id = Column(Integer, primary_key=True, index=True)
    court_name = Column(Text)
    jurisdiction_type = Column(
        Text, 
        CheckConstraint("jurisdiction_type IN ('U.S. State','U.S. Federal','International')")
    )
    jurisdiction_name = Column(Text)

    cases = relationship("Case", back_populates="jurisdiction")


class Case(Base):
    __tablename__ = "cases"

    case_id = Column(Integer, primary_key=True, index=True)
    slug = Column(Text, unique=True, index=True)
    record_number = Column(Integer, unique=True)
    caption = Column(Text)
    brief_description = Column(Text)
    filing_date = Column(Date)
    status_disposition = Column(Text)
    published_opinion_flag = Column(Boolean)
    class_action_status = Column(Text)
    researcher = Column(Text)
    summary_of_significance = Column(Text)
    summary_facts_activity = Column(Text)
    most_recent_activity = Column(Text)
    most_recent_activity_date = Column(Date)
    date_added = Column(Date)
    last_update = Column(Date)
    jurisdiction_id = Column(Integer, ForeignKey("jurisdictions.jurisdiction_id"))

    jurisdiction = relationship("Jurisdiction", back_populates="cases")
    dockets = relationship("Docket", back_populates="case", cascade="all, delete-orphan")
    secondary_sources = relationship("SecondarySource", back_populates="case", cascade="all, delete-orphan")
    
    areas = relationship("AreaOfApplication", secondary=case_areas, back_populates="cases")
    issues = relationship("Issue", secondary=case_issues, back_populates="cases")
    causes = relationship("CauseOfAction", secondary=case_causes, back_populates="cases")
    algorithms = relationship("Algorithm", secondary=case_algorithms, back_populates="cases")
    organizations = relationship("Organization", secondary=case_organizations, back_populates="cases")


class Docket(Base):
    __tablename__ = "dockets"

    docket_id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("cases.case_id", ondelete="CASCADE"))
    court = Column(Text)
    docket_number = Column(Text)
    link = Column(Text)

    case = relationship("Case", back_populates="dockets")
    documents = relationship("Document", back_populates="docket", cascade="all, delete-orphan")


class Document(Base):
    __tablename__ = "documents"

    document_id = Column(Integer, primary_key=True, index=True)
    docket_id = Column(Integer, ForeignKey("dockets.docket_id", ondelete="CASCADE"))
    document_type = Column(Text)
    filing_date = Column(Date)
    link = Column(Text)
    citation = Column(Text)

    docket = relationship("Docket", back_populates="documents")


class SecondarySource(Base):
    __tablename__ = "secondary_sources"

    source_id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("cases.case_id", ondelete="CASCADE"))
    title = Column(Text)
    link = Column(Text)

    case = relationship("Case", back_populates="secondary_sources")


class AreaOfApplication(Base):
    __tablename__ = "areas_of_application"

    area_id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, unique=True, index=True)

    cases = relationship("Case", secondary=case_areas, back_populates="areas")


class Issue(Base):
    __tablename__ = "issues"

    issue_id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, unique=True, index=True)

    cases = relationship("Case", secondary=case_issues, back_populates="issues")


class CauseOfAction(Base):
    __tablename__ = "causes_of_action"

    cause_id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, unique=True, index=True)

    cases = relationship("Case", secondary=case_causes, back_populates="causes")


class Algorithm(Base):
    __tablename__ = "algorithms"

    algorithm_id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, unique=True, index=True)

    cases = relationship("Case", secondary=case_algorithms, back_populates="algorithms")


class Organization(Base):
    __tablename__ = "organizations"

    organization_id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, unique=True, index=True)

    cases = relationship("Case", secondary=case_organizations, back_populates="organizations")
