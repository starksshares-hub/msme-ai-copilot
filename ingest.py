from backend.rag.config import DEFAULT_CONFIG
from backend.rag.vectordb import rebuild_index


def ingest() -> int:
    return rebuild_index(DEFAULT_CONFIG)


def main() -> None:
    count = ingest()
    print(f"Ingested {count} chunks into {DEFAULT_CONFIG.collection_name}")


if __name__ == "__main__":
    main()
