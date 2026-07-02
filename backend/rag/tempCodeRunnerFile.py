
        print("Found file:", file)

        content = file.read_text(encoding="utf-8")
        print("Content:")
        print(content)
        print("-" * 50)

load_documents()