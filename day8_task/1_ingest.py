from pathlib import Path
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from lc_config import get_store

def main():
    documents = []

    for file in sorted(Path("data").glob("*.md")):
        text = file.read_text(encoding="utf-8")
        documents.append(Document(
            page_content=text,
            metadata={"source": file.name}
        ))

    if not documents:
        print("No Markdown files found in data folder.")
        return

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=100
    )
    chunks = splitter.split_documents(documents)

    # Start with a clean collection so rerunning this file does not duplicate data.
    store = get_store()
    store.delete_collection()
    store = get_store()
    store.add_documents(chunks)

    print("Documents loaded:", len(documents))
    print("Chunks loaded:", len(chunks))
    print("Files:", ", ".join(doc.metadata["source"] for doc in documents))

if __name__ == "__main__":
    main()
