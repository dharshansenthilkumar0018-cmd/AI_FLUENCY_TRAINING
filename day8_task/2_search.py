from lc_config import get_store, MAX_DISTANCE

def main():
    store = get_store()
    questions = [
        "What CGPA do I need to be eligible for placements?",
        "What is the capital of France?"
    ]

    for question in questions:
        print("\nQuestion:", question)
        results = store.similarity_search_with_score(question, k=3)

        for doc, score in results:
            print("Source:", doc.metadata.get("source"), "| Score:", round(score, 4))

        print("MAX_DISTANCE:", MAX_DISTANCE)

if __name__ == "__main__":
    main()
