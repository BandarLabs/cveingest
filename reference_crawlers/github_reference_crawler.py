from bs4 import BeautifulSoup
import requests
from reference_crawlers.base_reference_crawler import BaseReferenceCrawler

class GitHubReferenceCrawler(BaseReferenceCrawler):
    def fetch_reference(self, url: str, cve_id: str) -> dict:
        # Define actions based on URL patterns
        url_handlers = {
            "/advisories": self.handle_advisory_url,
            "/commit": self.handle_commit_url,
        }

        # Determine which action to take
        for pattern, handler in url_handlers.items():
            if pattern in url:
                return handler(url)

        # Default action if no specific pattern matches
        return self.handle_default_url(url)

    def handle_advisory_url(self, url: str) -> dict:
        # Ignore advisory URLs by returning a specific message or an empty dict
        return {"url": url, "type": "GitHub", "info": ""}

    def handle_commit_url(self, url: str) -> dict:
        modified_url = url + ".diff"
        return self.make_request(modified_url)

    def handle_default_url(self, url: str) -> dict:
        return {"url": url, "type": "GitHub", "info": ""}
        # return self.make_request(url, parse_html=True)

    def make_request(self, url: str, parse_html: bool = False) -> dict:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            content = response.text

            if parse_html:
                # Parse HTML and extract text
                soup = BeautifulSoup(content, 'html.parser')
                content = soup.get_text(separator='\n', strip=True)

            return {
                "url": url,
                "type": "GitHub",
                "status_code": response.status_code,
                "info": f"Url {url} content: \n\n {content[:5000]}",
            }
        except requests.exceptions.RequestException as e:
            return {"url": url, "type": "GitHub", "error": str(e)}