# reference_crawlers/npmjs_reference_crawler.py

from reference_crawlers.base_reference_crawler import BaseReferenceCrawler
import requests
from bs4 import BeautifulSoup

class NPMJSReferenceCrawler(BaseReferenceCrawler):
    def fetch_reference(self, url: str, cve_id: str) -> dict:
        try:
            # response = requests.get(url, timeout=10)
            # response.raise_for_status()

            # # Use BeautifulSoup to parse the HTML and extract text
            # soup = BeautifulSoup(response.text, 'html.parser')
            # text_content = soup.get_text()

            return {
                "url": url,
                "type": "NPMJS",
                "status_code": 200,  # response.status_code,
                "info": "",  # Return the first 5000 characters of the extracted text
            }
        except requests.exceptions.RequestException as e:
            return {"url": url, "type": "NPMJS", "error": str(e)}