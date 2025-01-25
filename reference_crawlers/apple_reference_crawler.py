import requests
from bs4 import BeautifulSoup
from reference_crawlers.base_reference_crawler import BaseReferenceCrawler

class AppleReferenceCrawler(BaseReferenceCrawler):
    def fetch_reference(self, url: str, cve_id: str) -> dict:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            html = response.content
            cve_details = self.extract_cve_details(html, cve_id)

            if cve_details:
                return {
                    "url": url,
                    "type": "Apple",
                    "status_code": response.status_code,
                    "info": cve_details["info"]
                }
            else:
                return {
                    "url": url,
                    "type": "Apple",
                    "error": f"CVE ID {cve_id} not found"
                }
        except requests.exceptions.RequestException as e:
            return {"url": url, "type": "Apple", "error": str(e)}

    def extract_cve_details(self, html: bytes, cve_id: str) -> dict:
        soup = BeautifulSoup(html, 'html.parser')
        sections_div = soup.find('div', id='sections')

        if not sections_div:
            return None

        cve_entry = sections_div.find(string=lambda text: cve_id in text)

        if not cve_entry:
            return None

        cve_entry_container = cve_entry.find_parent('p')

        if not cve_entry_container:
            return None

        # Extract surrounding details
        # details_text = cve_entry_container.get_text(separator=' ', strip=True)

        # Find the 'Impact' section before the CVE entry
        impact_info = ""
        for sibling in cve_entry_container.find_previous_siblings('p'):
            if 'Impact' in sibling.get_text():
                impact_info = sibling.get_text(separator=' ', strip=True)
                break  # Exit the loop once we find the first matching 'Impact' paragraph

        cve_details = {
            "cve_id": cve_id,
            "details": impact_info,
            "info": impact_info
        }

        return cve_details