import requests


def fetch_ecfr_versions(title, issue_date, chapter):
    url = f"https://www.ecfr.gov/api/versioner/v1/versions/title-{title}.json"

    params = {
        "issue_date[on]": issue_date,
        "chapter": chapter
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to fetch data. Status code: {response.status_code}"}