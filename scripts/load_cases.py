import pandas as pd
from db import get_connection
from utils import clean_df, parse_list


def load_cases():

    df = clean_df(
        pd.read_excel(
            "data/case_table.xlsx",
            sheet_name="Case_Table_2026-Feb-21_1952"
        )
    )

    conn = get_connection()
    cur = conn.cursor()

    record_to_case_id = {}

    for _, row in df.iterrows():

        slug = row.get("Case_snug")

        if not slug:
            continue

        court_name = row.get("Jurisdiction_Filed")
        jurisdiction_type = row.get("Jurisdiction_Type_Text")
        jurisdiction_name = row.get("Jurisdiction_Name")

        if not court_name or not jurisdiction_type or not jurisdiction_name:
            continue

        cur.execute("""
            INSERT INTO jurisdictions (court_name, jurisdiction_type, jurisdiction_name)
            VALUES (%s, %s, %s)
            ON CONFLICT DO NOTHING
        """, (
            court_name,
            jurisdiction_type,
            jurisdiction_name
        ))

        cur.execute("""
            SELECT jurisdiction_id FROM jurisdictions
            WHERE court_name = %s
              AND jurisdiction_type = %s
              AND jurisdiction_name = %s
        """, (
            court_name,
            jurisdiction_type,
            jurisdiction_name
        ))

        jurisdiction_row = cur.fetchone()
        if not jurisdiction_row:
            continue

        jurisdiction_id = jurisdiction_row[0]

        slug = row.get("Case_snug")

        cur.execute("""
            INSERT INTO cases (
                slug,
                record_number,
                caption,
                brief_description,
                filing_date,
                status_disposition,
                published_opinion_flag,
                class_action_status,
                researcher,
                summary_of_significance,
                summary_facts_activity,
                most_recent_activity,
                most_recent_activity_date,
                date_added,
                last_update,
                jurisdiction_id
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (slug) DO NOTHING
            RETURNING case_id
        """, (
            slug,
            row.get("Record_Number"),
            row.get("Caption"),
            row.get("Brief_Description"),
            row.get("Date_Action_Filed"),
            row.get("Status_Disposition"),
            bool(row.get("Published_Opinions_binary")),
            row.get("Class_Action_list"),
            row.get("Researcher"),
            row.get("Summary_of_Significance"),
            row.get("Summary_Facts_Activity_to_Date"),
            row.get("Most_Recent_Activity"),
            row.get("Most_Recent_Activity_Date"),
            row.get("Date_Added"),
            row.get("Last_Update"),
            jurisdiction_id
        ))

        result = cur.fetchone()

        if result:
            case_id = result[0]
        else:
            cur.execute("SELECT case_id FROM cases WHERE slug = %s", (slug,))
            case_id = cur.fetchone()[0]

        record_to_case_id[row.get("Record_Number")] = case_id

        multi_map = {
            "Area_of_Application_List": ("areas_of_application", "case_areas", "area_id"),
            "Issue_List": ("issues", "case_issues", "issue_id"),
            "Cause_of_Action_List": ("causes_of_action", "case_causes", "cause_id"),
            "Name_of_Algorithm_List": ("algorithms", "case_algorithms", "algorithm_id"),
            "Organizations_involved": ("organizations", "case_organizations", "organization_id"),
        }

        for col, (ref_table, bridge_table, id_column) in multi_map.items():
            values = parse_list(row.get(col))

            for val in values:
                cur.execute(f"""
                    INSERT INTO {ref_table} (name)
                    VALUES (%s)
                    ON CONFLICT (name) DO NOTHING
                """, (val,))

                cur.execute(f"""
                    INSERT INTO {bridge_table} (case_id, {id_column})
                    SELECT %s, {id_column}
                    FROM {ref_table}
                    WHERE name = %s
                    ON CONFLICT DO NOTHING
                """, (case_id, val))

    conn.commit()
    cur.close()
    conn.close()

    print("Cases loaded successfully.")
    return record_to_case_id