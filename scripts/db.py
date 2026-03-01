"""
Database Connection Module.

Provides a centralized function to establish a PostgreSQL
connection using environment variables.

This abstraction ensures secure, reusable, and consistent
database connectivity across the ETL pipeline and API layer.
"""

import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

def get_connection():
    """
    Create and return a new PostgreSQL database connection.

    The connection parameters are loaded from environment
    variables to ensure credentials are not hardcoded.

    Returns:
        psycopg2.extensions.connection: Active database connection.
    """
        
    return psycopg2.connect(
        dbname=os.getenv("PG_DB"),
        user=os.getenv("PG_USER"),
        password=os.getenv("PG_PASSWORD"),
        host=os.getenv("PG_HOST"),
        port=os.getenv("PG_PORT"),
        sslmode="require"
    )