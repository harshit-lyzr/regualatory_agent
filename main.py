from data_collection import fetch_ecfr_versions
from datetime import datetime
from rag_service.rag import get_rag_docs, delete_rag_docs, train_rag_agent
from webiste_parsing.scrapper import parse_website
import json

RAG_ID = "679b2ab71439666773122b9d"
TITLE = "12"
CHAPTER = "3"
TODAY = datetime.today()
FORMATTED_DATE = TODAY.strftime('%Y-%m-%d')


def get_subchapter(part):
    part_num = int(part)
    if 302 <= part_num <= 313:
        return "A"
    elif 323 <= part_num <= 390:
        return "B"
    return "Unknown"


def fetch_and_filter_versions():
    """Fetch ECFR versions and filter parts."""
    result = fetch_ecfr_versions(TITLE, FORMATTED_DATE, CHAPTER)
    parts = sorted(set(entry["part"] for entry in result["content_versions"]))
    return parts


def generate_urls(parts):
    """Generate list of URLs for the corresponding parts."""
    return [
        f"https://www.ecfr.gov/current/title-{TITLE}/chapter-III/subchapter-{get_subchapter(part)}/part-{part}"
        for part in parts
    ]


def get_matching_urls(all_docs, urls):
    """Get matching URLs between RAG documents and ECFR URLs."""
    return [url for url in all_docs if url in urls]


def scrap_and_train(matching_urls):
    """Scrape content and train the RAG agent with the new data."""
    for rule in matching_urls:
        scrapped_content = parse_website(rule)
        print(f"Scraped content for {rule}")

        # Safely handle potential missing documents or invalid structure
        documents = scrapped_content.get("documents", [])
        if documents:
            json_data = json.loads(json.dumps(scrapped_content, indent=4))
            train_rag_agent(RAG_ID, json_data["documents"][0])
            print(f"Training done for {rule}")
        else:
            print(f"No documents found for {rule}, skipping training.")


def main():
    parts = fetch_and_filter_versions()
    urls = generate_urls(parts)

    # Get RAG documents and find matching URLs
    all_docs = get_rag_docs(RAG_ID)
    print(all_docs)

    matching_urls = get_matching_urls(all_docs, urls)

    if matching_urls:
        # Delete matching URLs from RAG
        delete_rag_docs(RAG_ID, matching_urls)
        print(f"Deleted {matching_urls}")

        # Scrap and train RAG agent for each URL
        scrap_and_train(matching_urls)
    else:
        print("No matching URLs found in RAG.")


if __name__ == "__main__":
    main()
