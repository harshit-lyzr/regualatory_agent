from data_collection import fetch_ecfr_versions
from datetime import datetime
from rag_service.rag import get_rag_docs, delete_rag_docs, train_rag_agent
from webiste_parsing.scrapper import parse_website
import json
from supabase import create_client, Client
from dotenv import load_dotenv
import os

load_dotenv()

# Supabase Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")        # Replace with your Supabase API URL
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

RAG_ID = os.getenv("RAG_ID")
title = "12"
chapter = "3"
today = datetime.today()
formatted_date = today.strftime('%Y-%m-%d')


def get_subchapter(part):
    part_num = int(part)
    if 302 <= part_num <= 313:
        return "A"
    elif 323 <= part_num <= 390:
        return "B"
    else:
        return "Unknown"


result = fetch_ecfr_versions(title, formatted_date, chapter)

extracted_data = []
for item in result.get('content_versions', []):
    extracted_data.append({
        'amendment_date': item['amendment_date'],
        'issue_date': item['issue_date'],
        'name': item['name'],
        'part': item['part'],
        'flag': "yes"
    })

# Handle the case when there is no data
if not extracted_data:
    extracted_data.append({
        "name": "No Updates",
        "amendment_date": "",
        "issue_date": "",
        "part": "",
        "flag": "no"
    })

# Insert into Supabase
response = supabase.table("regulatory_agent").insert(extracted_data).execute()

print("Data Inserted:", response)

parts = sorted(set(entry["part"] for entry in result["content_versions"]))

urls = [
    f"https://www.ecfr.gov/current/title-12/chapter-III/subchapter-{get_subchapter(part)}/part-{part}"
    for part in parts
]

all_docs = get_rag_docs(RAG_ID)
print(all_docs)

matching_urls = [url for url in all_docs if url in urls]

updated_list = []
for match in matching_urls:
    updated_list.append(match)

print(updated_list)
delete_rag_docs(RAG_ID, updated_list)
print(f"deleted {updated_list}")
for rule in updated_list:
    scrapped_content = parse_website(rule)
    print(f"scrap content for {rule}")
    json_data = json.loads(json.dumps(scrapped_content, indent=4))
    train_rag_agent(RAG_ID, json_data["documents"][0])
    print(f"Training done for {rule}")
