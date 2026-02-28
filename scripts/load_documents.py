import pandas as pd
from db import get_connection
from utils import clean_df

def load_documents(record_map):

    df = clean_df(
        pd.read_excel(
            "data/document_table.xlsx",
            sheet_name="Document_Table"
        )
    )

    conn = get_connection()
    cur = conn.cursor()

    for _, row in df.iterrows():
        case_id = record_map.get(row.get("Case_Number"))
        if case_id:
            cur.execute("SELECT docket_id FROM dockets WHERE case_id = %s LIMIT 1", (case_id,))
            result = cur.fetchone()
            if result:
                docket_id = result[0]
                cur.execute("""
                    INSERT INTO documents (docket_id, document_type, filing_date, link, citation)
                    VALUES (%s,%s,%s,%s,%s)
                """, (
                    docket_id,
                    row.get("document"),
                    row.get("date"),
                    row.get("link"),
                    row.get("cite_or_reference")
                ))

    conn.commit()
    cur.close()
    conn.close()

    print("Documents loaded")