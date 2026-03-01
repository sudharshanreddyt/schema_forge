"""
Docket Data Migration Script.

Loads docket information and associates each docket
with its corresponding case using foreign key relationships.
"""

import pandas as pd
from db import get_connection
from utils import clean_df

def load_dockets(record_map):
    """
    Insert docket records linked to existing cases.

    Args:
        record_map (dict): Mapping of record_number to case_id.
    """

    df = clean_df(
        pd.read_excel(
            "data/docket_table.xlsx",
            sheet_name="Docket_Table"
        )
    )

    conn = get_connection()
    cur = conn.cursor()

    for _, row in df.iterrows():
        case_id = record_map.get(row.get("Case_Number"))
        if case_id:
            cur.execute("""
                INSERT INTO dockets (case_id, court, docket_number, link)
                VALUES (%s,%s,%s,%s)
            """, (
                case_id,
                row.get("court"),
                row.get("number"),
                row.get("link")
            ))

    conn.commit()
    cur.close()
    conn.close()

    print("Dockets loaded")