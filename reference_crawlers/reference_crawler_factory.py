from reference_crawlers.nist_reference_crawler import NISTReferenceCrawler
from reference_crawlers.base_reference_crawler import BaseReferenceCrawler
from reference_crawlers.github_reference_crawler import GitHubReferenceCrawler
from reference_crawlers.npmjs_reference_crawler import NPMJSReferenceCrawler
from reference_crawlers.talos_reference_crawler import TalosReferenceCrawler
from reference_crawlers.apple_reference_crawler import AppleReferenceCrawler

import requests
from bs4 import BeautifulSoup

class ReferenceCrawlerFactory:
    @staticmethod
    def get_crawler(url: str) -> BaseReferenceCrawler:
        if "github.com" in url:
            return GitHubReferenceCrawler()
        elif "nist.gov" in url:
            return NISTReferenceCrawler()
        elif "npmjs.com" in url:
            return NPMJSReferenceCrawler()
        elif "talosintelligence.com" in url:
            return TalosReferenceCrawler()
        elif "apple.com" in url:
            return AppleReferenceCrawler()
        else:
            return DefaultReferenceCrawler()


class DefaultReferenceCrawler(BaseReferenceCrawler):
    # Define a whitelist of allowed domains
    WHITELISTED_DOMAINS = [
        "twcert.org.tw",
        # Add additional domains as needed
    ]

    def fetch_reference(self, url: str, cve_id: str) -> dict:
        # Check if the URL is within the whitelisted domains
        if not any(domain in url for domain in self.WHITELISTED_DOMAINS):
            return {
                "url": url,
                "type": "Default",
                "info": "",  # Return empty or placeholder if not whitelisted
                "error": "Domain not whitelisted"
            }

        try:
            # If URL is whitelisted, proceed to fetch and parse the content
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            # Use BeautifulSoup to parse the HTML and extract text
            soup = BeautifulSoup(response.text, 'html.parser')
            text_content = soup.get_text()

            return {
                "url": url,
                "type": "Default",
                "status_code": response.status_code,
                "info": text_content[:5000],  # First 5000 characters of text
            }
        except requests.exceptions.RequestException as e:
            return {
                "url": url,
                "type": "Default",
                "error": str(e)
            }
