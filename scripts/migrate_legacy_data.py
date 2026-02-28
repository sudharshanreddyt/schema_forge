import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

def get_connection():
    return psycopg2.connect(
        dbname=os.getenv("PG_DB"),
        user=os.getenv("PG_USER"),
        password=os.getenv("PG_PASSWORD"),
        host=os.getenv("PG_HOST"),
        port=os.getenv("PG_PORT")
    )

def clean_list_string(raw_string):
    """
    Cleans legacy string like:
    "'Fraud','Housing'"
    into:
    ['Fraud', 'Housing']
    """
    if not raw_string:
        return []
    return [item.strip().replace("'", "") for item in raw_string.split(",")]

def migrate_case_metadata(case_id, legacy_areas, legacy_orgs):
    conn = get_connection()
    cur = conn.cursor()

    areas = clean_list_string(legacy_areas)

    for area in areas:
        cur.execute("""
            INSERT INTO areas_of_application (name)
            VALUES (%s)
            ON CONFLICT (name) DO NOTHING
        """, (area,))

        cur.execute("""
            INSERT INTO case_areas (case_id, area_id)
            SELECT %s, area_id
            FROM areas_of_application
            WHERE name = %s
            ON CONFLICT DO NOTHING
        """, (case_id, area))

    orgs = [o.strip() for o in legacy_orgs.split(",")] if legacy_orgs else []

    for org in orgs:
        cur.execute("""
            INSERT INTO organizations (name)
            VALUES (%s)
            ON CONFLICT (name) DO NOTHING
        """, (org,))

        cur.execute("""
            INSERT INTO case_organizations (case_id, organization_id)
            SELECT %s, organization_id
            FROM organizations
            WHERE name = %s
            ON CONFLICT DO NOTHING
        """, (case_id, org))

    conn.commit()
    cur.close()
    conn.close()

    print(f"Migration complete for case_id={case_id}")


if __name__ == "__main__":
    case_id = 1
    legacy_areas = "'Fraud','Housing'"
    legacy_orgs = "Asian News International, Open AI Inc."

    migrate_case_metadata(case_id, legacy_areas, legacy_orgs)