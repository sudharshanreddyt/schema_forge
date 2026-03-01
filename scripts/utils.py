"""
Utility Functions for Data Cleaning and Transformation.

Contains helper functions used during the ETL process
to normalize raw dataset inputs before inserting them
into the relational database.
"""

import pandas as pd
import numpy as np

def clean_df(df):
    """
    Clean a pandas DataFrame prior to database insertion.

    Operations performed:
    - Strip whitespace from column names
    - Replace NaN values with None
    - Replace NaT timestamps with None

    Args:
        df (pandas.DataFrame): Raw input DataFrame.

    Returns:
        pandas.DataFrame: Cleaned DataFrame.
    """
        
    df.columns = df.columns.str.strip()
    df = df.replace({np.nan: None})
    df = df.replace({pd.NaT: None})
    return df


def parse_list(value):
    """
    Parse a multi-value text field into a normalized list.

    Handles:
    - Removal of single quotes
    - Splitting on commas
    - Whitespace trimming
    - Title-case normalization
    - Duplicate removal

    Args:
        value (str): Raw multi-value string.

    Returns:
        list[str]: Cleaned and deduplicated list of values.
    """
    
    if not value:
        return []
    cleaned = str(value).replace("'", "")
    items = [x.strip() for x in cleaned.split(",")]
    return list(set([x.title() for x in items if x]))