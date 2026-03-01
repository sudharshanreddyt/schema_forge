"""
Secondary Source Migration Script.

Loads external references such as news articles,
blog posts, and legal commentary linked to cases.
"""

import pandas as pd
from db import get_connection
from utils import clean_df

def load_secondary(record_map):
    """
    Insert secondary source references into the database.

    Args:
        record_map (dict): Mapping of record_number to case_id.
    """

    df = clean_df(
        pd.read_excel(
            "data/secondary_source.xlsx",
            sheet_name="Secondary_Source_Coverage_Table"
        )
    )

    conn = get_connection()
    cur = conn.cursor()

    for _, row in df.iterrows():
        case_id = record_map.get(row.get("Case_Number"))
        if case_id:
            cur.execute("""
                INSERT INTO secondary_sources (case_id, title, link)
                VALUES (%s,%s,%s)
            """, (
                case_id,
                row.get("Secondary_Source_Title"),
                row.get("Secondary_Source_Link")
            ))

    conn.commit()
    cur.close()
    conn.close()

    print("Secondary sources loaded")