# SchemaForge

## Clone the repository
```bash
git clone https://github.com/sudharshanreddyt/schema_forge.git
cd schema_forge
```

## Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate
```

## Install dependencies
```bash
pip install -r requirements.txt
```

## Create .env file
Replace the values in the .env file with your own values
# Database Configuration
PG_DB=<db_name>
PG_USER=<db_user>
PG_PASSWORD=<db_password>
PG_HOST=<db_host>
PG_PORT=<db_port>

# Project Settings
PROJECT_NAME=<project_name>

## How to Run
Run the following command from the **root directory** of the project:
```bash
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

It will start the server at `http://localhost:8000` and the API documentation at `http://localhost:8000/docs`


## API Reference
This document provides a comprehensive overview of the available API endpoints for the SchemaForge Legal Database, including detailed example inputs for **every single** route.

## Base URL
The API is served at: `http://localhost:8000/docs`

---

## 🏛️ Jurisdictions
Manage legal jurisdictions (States, Federal, International).

### List Jurisdictions
- **Endpoint**: `GET /jurisdictions/`
- **Description**: Retrieve a list of jurisdictions.
- **Example Usage**: `GET /jurisdictions/?skip=0&limit=5`

### Create Jurisdiction
- **Endpoint**: `POST /jurisdictions/`
- **Example Input**:
```json
{
  "court_name": "Supreme Court of California",
  "jurisdiction_type": "U.S. State",
  "jurisdiction_name": "California"
}
```

### Get Jurisdiction Detail
- **Endpoint**: `GET /jurisdictions/{id}`
- **Example Usage**: `GET /jurisdictions/1`

---

## ⚖️ Cases
The core entity representing legal cases.

### List Cases
- **Endpoint**: `GET /cases/`
- **Description**: Retrieve a list of cases. Skip is the number of records to skip and limit is the number of records to retrieve.
- **Example Usage**: `GET /cases/?skip=0&limit=10`

### Create Case
- **Endpoint**: `POST /cases/`
- **Example Input**:
```json
{
  "slug": "smith-v-jones-2024",
  "record_number": 123456,
  "caption": "John Smith v. Jane Jones",
  "brief_description": "A landmark case regarding AI ethics and liability.",
  "filing_date": "2024-01-15",
  "status_disposition": "Pending",
  "published_opinion_flag": true,
  "class_action_status": "Individual",
  "researcher": "Dr. Alice Brown",
  "summary_of_significance": "First case to address algorithmic bias directly.",
  "summary_facts_activity": "Facts regarding the deployment of the biased algorithm...",
  "most_recent_activity": "Initial hearing held.",
  "most_recent_activity_date": "2024-02-10",
  "date_added": "2024-01-20",
  "last_update": "2024-02-11",
  "jurisdiction_id": 129,
  "area_ids": [129],
  "issue_ids": [129, 129],
  "cause_ids": [129],
  "algorithm_ids": [129],
  "organization_ids": [129]
}
```

### Get Case Detail
- **Endpoint**: `GET /cases/{id}`
- **Example Usage**: `GET /cases/1`
- **Note**: Returns nested objects for jurisdiction, dockets, documents, and taxonomy associations.

### Update Case
- **Endpoint**: `PUT /cases/{id}`
- **Example Input**:
```json
{
  "status_disposition": "Resolved",
  "most_recent_activity": "Case dismissed with prejudice.",
  "last_update": "2024-03-01",
  "area_ids": [1, 2, 3]
}
```

### Delete Case
- **Endpoint**: `DELETE /cases/{id}`
- **Example Usage**: `DELETE /cases/1`
- **Warning**: This will also delete all associated dockets, documents, and secondary sources due to CASCADE delete.

---

## 📂 Dockets
Court dockets associated with cases.

### List Dockets
- **Endpoint**: `GET /dockets/`
- **Example Usage**: `GET /dockets/`

### Create Docket
- **Endpoint**: `POST /dockets/`
- **Example Input**:
```json
{
  "case_id": 1,
  "court": "California Superior Court",
  "docket_number": "CIV-2024-456",
  "link": "https://court-portal.ca.gov/case/123"
}
```

### Get Docket Detail
- **Endpoint**: `GET /dockets/{id}`
- **Example Usage**: `GET /dockets/1`

### Update Docket
- **Endpoint**: `PUT /dockets/{id}`
- **Example Input**:
```json
{
  "docket_number": "CIV-2024-456-AMENDED",
  "link": "https://court-portal.ca.gov/case/123-revised"
}
```

### Delete Docket
- **Endpoint**: `DELETE /dockets/{id}`
- **Example Usage**: `DELETE /dockets/1`

---

## 📄 Documents
Legal documents linked to dockets.

### List Documents
- **Endpoint**: `GET /documents/`
- **Example Usage**: `GET /documents/`

### Create Document
- **Endpoint**: `POST /documents/`
- **Example Input**:
```json
{
  "docket_id": 1,
  "document_type": "Complaint",
  "filing_date": "2024-01-15",
  "link": "https://storage.ca.gov/docs/complaint.pdf",
  "citation": "2024 Cal. Super. LEXIS 123"
}
```

### Get Document Detail
- **Endpoint**: `GET /documents/{id}`
- **Example Usage**: `GET /documents/1`

### Update Document
- **Endpoint**: `PUT /documents/{id}`
- **Example Input**:
```json
{
  "document_type": "Amended Complaint",
  "link": "https://storage.ca.gov/docs/complaint_v2.pdf"
}
```

### Delete Document
- **Endpoint**: `DELETE /documents/{id}`
- **Example Usage**: `DELETE /documents/1`

---

## 🔗 Secondary Sources
External sources and citations related to cases.

### List Secondary Sources
- **Endpoint**: `GET /secondary-sources/`
- **Example Usage**: `GET /secondary-sources/`

### Create Secondary Source
- **Endpoint**: `POST /secondary-sources/`
- **Example Input**:
```json
{
  "case_id": 1,
  "title": "Analysis of Smith v. Jones: AI Liability Trends",
  "link": "https://lawreview.edu/articles/ai-liability"
}
```

### Get Secondary Source Detail
- **Endpoint**: `GET /secondary-sources/{id}`
- **Example Usage**: `GET /secondary-sources/1`

### Update Secondary Source
- **Endpoint**: `PUT /secondary-sources/{id}`
- **Example Input**:
```json
{
  "title": "Comprehensive Analysis of Smith v. Jones",
  "link": "https://lawreview.edu/articles/ai-liability-v2"
}
```

### Delete Secondary Source
- **Endpoint**: `DELETE /secondary-sources/{id}`
- **Example Usage**: `DELETE /secondary-sources/1`

---

## 🏷️ Taxonomies
Manage categorizations for legal analytics. These categories are linked to Cases.

### Areas of Application
- **GET `/taxonomies/areas/`**: List all areas.
- **POST `/taxonomies/areas/`**: Create area.
  ```json
  { "name": "Consumer Protection" }
  ```

### Issues
- **GET `/taxonomies/issues/`**: List all issues.
- **POST `/taxonomies/issues/`**: Create issue.
  ```json
  { "name": "Algorithmic Bias" }
  ```

### Causes of Action
- **GET `/taxonomies/causes/`**: List all causes.
- **POST `/taxonomies/causes/`**: Create cause.
  ```json
  { "name": "Negligence" }
  ```

### Algorithms
- **GET `/taxonomies/algorithms/`**: List all algorithms.
- **POST `/taxonomies/algorithms/`**: Create algorithm.
  ```json
  { "name": "Predictive Policing Model v1" }
  ```

### Organizations
- **GET `/taxonomies/organizations/`**: List all organizations.
- **POST `/taxonomies/organizations/`**: Create organization.
  ```json
  { "name": "Tech Corp Inc." }
  ```

---

## 🚀 Deployment
- **Render Deployment**: See [render.yaml](render.yaml) and [deployment_guide.md](deployment_guide.md) for instructions.

## 🛠️ Developer Tools
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs) (Best for interactive testing)
