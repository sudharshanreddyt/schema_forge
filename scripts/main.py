from load_cases import load_cases
from load_dockets import load_dockets
from load_documents import load_documents
from load_secondary import load_secondary

def main():
    record_map = load_cases()
    load_dockets(record_map)
    load_documents(record_map)
    load_secondary(record_map)

if __name__ == "__main__":
    main()