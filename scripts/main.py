"""
ETL Orchestration Script.

Coordinates the full migration process by executing
case, docket, document, and secondary source loaders
in proper dependency order.

Ensures foreign key integrity across the dataset.
"""

from load_cases import load_cases
from load_dockets import load_dockets
from load_documents import load_documents
from load_secondary import load_secondary

def main():
    """
    Execute full data migration workflow.

    Steps:
    1. Load cases
    2. Load dockets
    3. Load documents
    4. Load secondary sources
    """
    
    record_map = load_cases()
    load_dockets(record_map)
    load_documents(record_map)
    load_secondary(record_map)

if __name__ == "__main__":
    main()