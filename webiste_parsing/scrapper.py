import requests
import json


def parse_website(target_url):
    url = "https://rag-prod.studio.lyzr.ai/v3/parse/website/"

    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "urls": [target_url],
        "source": "website",
        "max_crawl_pages": 1,
        "max_crawl_depth": 0,
        "dynamic_content_wait_secs": 5,
        "actor": "apify/website-content-crawler",
        "crawler_type": "cheerio"
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.status_code, "message": response.text}