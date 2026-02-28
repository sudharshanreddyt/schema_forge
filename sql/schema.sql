DROP TABLE IF EXISTS case_organizations CASCADE;
DROP TABLE IF EXISTS case_algorithms CASCADE;
DROP TABLE IF EXISTS case_causes CASCADE;
DROP TABLE IF EXISTS case_issues CASCADE;
DROP TABLE IF EXISTS case_areas CASCADE;
DROP TABLE IF EXISTS organizations CASCADE;
DROP TABLE IF EXISTS algorithms CASCADE;
DROP TABLE IF EXISTS causes_of_action CASCADE;
DROP TABLE IF EXISTS issues CASCADE;
DROP TABLE IF EXISTS areas_of_application CASCADE;
DROP TABLE IF EXISTS secondary_sources CASCADE;
DROP TABLE IF EXISTS documents CASCADE;
DROP TABLE IF EXISTS dockets CASCADE;
DROP TABLE IF EXISTS cases CASCADE;
DROP TABLE IF EXISTS jurisdictions CASCADE;

CREATE TABLE jurisdictions (
    jurisdiction_id SERIAL PRIMARY KEY,
    court_name TEXT NOT NULL,
    jurisdiction_type TEXT CHECK (
        jurisdiction_type IN ('U.S. State','U.S. Federal','International')
    ),
    jurisdiction_name TEXT NOT NULL,
    UNIQUE (court_name, jurisdiction_type, jurisdiction_name)
);

CREATE TABLE cases (
    case_id SERIAL PRIMARY KEY,
    slug TEXT UNIQUE,
    record_number INT UNIQUE,
    caption TEXT NOT NULL,
    brief_description TEXT,
    filing_date DATE,
    status_disposition TEXT,
    published_opinion_flag BOOLEAN,
    class_action_status TEXT,
    researcher TEXT,
    summary_of_significance TEXT,
    summary_facts_activity TEXT,
    most_recent_activity TEXT,
    most_recent_activity_date DATE,
    date_added DATE,
    last_update DATE,
    jurisdiction_id INT REFERENCES jurisdictions(jurisdiction_id)
        ON DELETE SET NULL
);

CREATE TABLE dockets (
    docket_id SERIAL PRIMARY KEY,
    case_id INT REFERENCES cases(case_id)
        ON DELETE CASCADE,
    court TEXT,
    docket_number TEXT,
    link TEXT
);

CREATE TABLE documents (
    document_id SERIAL PRIMARY KEY,
    docket_id INT REFERENCES dockets(docket_id)
        ON DELETE CASCADE,
    document_type TEXT,
    filing_date DATE,
    link TEXT,
    citation TEXT
);

CREATE TABLE secondary_sources (
    source_id SERIAL PRIMARY KEY,
    case_id INT REFERENCES cases(case_id)
        ON DELETE CASCADE,
    title TEXT,
    link TEXT
);

CREATE TABLE areas_of_application (
    area_id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE issues (
    issue_id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE causes_of_action (
    cause_id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE algorithms (
    algorithm_id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE organizations (
    organization_id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE case_areas (
    case_id INT REFERENCES cases(case_id) ON DELETE CASCADE,
    area_id INT REFERENCES areas_of_application(area_id) ON DELETE CASCADE,
    PRIMARY KEY (case_id, area_id)
);

CREATE TABLE case_issues (
    case_id INT REFERENCES cases(case_id) ON DELETE CASCADE,
    issue_id INT REFERENCES issues(issue_id) ON DELETE CASCADE,
    PRIMARY KEY (case_id, issue_id)
);

CREATE TABLE case_causes (
    case_id INT REFERENCES cases(case_id) ON DELETE CASCADE,
    cause_id INT REFERENCES causes_of_action(cause_id) ON DELETE CASCADE,
    PRIMARY KEY (case_id, cause_id)
);

CREATE TABLE case_algorithms (
    case_id INT REFERENCES cases(case_id) ON DELETE CASCADE,
    algorithm_id INT REFERENCES algorithms(algorithm_id) ON DELETE CASCADE,
    PRIMARY KEY (case_id, algorithm_id)
);

CREATE TABLE case_organizations (
    case_id INT REFERENCES cases(case_id) ON DELETE CASCADE,
    organization_id INT REFERENCES organizations(organization_id) ON DELETE CASCADE,
    PRIMARY KEY (case_id, organization_id)
);