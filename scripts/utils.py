import pandas as pd
import numpy as np

def clean_df(df):
    df.columns = df.columns.str.strip()
    df = df.replace({np.nan: None})
    df = df.replace({pd.NaT: None})
    return df

def parse_list(value):
    if not value:
        return []
    cleaned = str(value).replace("'", "")
    items = [x.strip() for x in cleaned.split(",")]
    return list(set([x.title() for x in items if x]))