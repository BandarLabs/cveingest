import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime, timedelta

BASE_URL = "https://github.com/advisories"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; ProjectCrawler/1.0)"}

def fetch_advisories():
    """
    Fetch this week's advisories from GitHub.
    """
    response = requests.get(BASE_URL, headers=HEADERS)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch advisories: {response.status_code}")
    return response.text

def parse_advisories(html):
    """
    Parse the advisories page and extract links to critical CVEs.
    """
    soup = BeautifulSoup(html, "html.parser")
    advisories = []
    for advisory in soup.select("div.AdvisoryItem"):  # Adjust selector as needed
        severity = advisory.select_one(".severity-critical")
        if severity:
            title = advisory.select_one(".AdvisoryItem-title").text.strip()
            link = advisory.select_one("a")["href"]
            advisories.append({"title": title, "link": link})
    return advisories

def fetch_advisory_details(link):
    """
    Fetch detailed information from an advisory link.
    """
    response = requests.get(link, headers=HEADERS)
    if response.status_code != 200:
        print(f"Failed to fetch details for {link}")
        return None
    return response.text

def process_advisories(advisories):
    """
    Process each advisory, follow links, and extract additional data.
    """
    details = []
    for advisory in advisories:
        detail_html = fetch_advisory_details(advisory["link"])
        if detail_html:
            soup = BeautifulSoup(detail_html, "html.parser")
            # Extract further details or follow more links
            description = soup.select_one(".description").text.strip() if soup.select_one(".description") else ""
            advisory["description"] = description
            details.append(advisory)
    return details

def save_to_file(data, filename="advisories.json"):
    """
    Save the extracted data to a JSON file.
    """
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    html = fetch_advisories()
    advisories = parse_advisories(html)
    detailed_advisories = process_advisories(advisories)
    save_to_file(detailed_advisories)
    print("Crawl complete. Results saved to advisories.json.")
