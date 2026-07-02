from pathlib import Path


def get_dataset_path() -> Path:
    return Path(r"T:\msme-ai-copilot\dataset")


def main() -> None:
    dataset_path = get_dataset_path()

    print("Dataset path:")
    print(dataset_path)

    print("\nDoes dataset exist?")
    print(dataset_path.exists())

    print("\nDataset content loading is disabled.")


if __name__ == "__main__":
    main()