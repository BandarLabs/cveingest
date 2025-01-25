import requests
from bs4 import BeautifulSoup
from reference_crawlers.base_reference_crawler import BaseReferenceCrawler

class TalosReferenceCrawler(BaseReferenceCrawler):
    def fetch_reference(self, url: str, cve_id: str) -> dict:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            html = response.content
            details, timeline = self.extract_details_timeline(html)

            return {
                "url": url,
                "type": "Talos",
                "status_code": response.status_code,
                "info": f"details: {details}, timeline: {timeline}"
            }
        except requests.exceptions.RequestException as e:
            return {"url": url, "type": "Talos", "error": str(e)}

    def extract_details_timeline(self, html: bytes) -> tuple:
        soup = BeautifulSoup(html, 'html.parser')
        details_text = ""
        timeline_text = ""

        # Extract Details
        details_header = soup.find('h5', id='details')
        if details_header:
            details_elem = details_header.find_next_siblings(['p', 'pre'])
            for elem in details_elem:
                details_text += elem.get_text(separator=' ', strip=True) + " "
            details_text = details_text.strip()

        # Extract Timeline
        timeline_header = soup.find('h5', id='timeline')
        if timeline_header:
            timeline_elem = timeline_header.find_next_sibling('p')
            if timeline_elem:
                timeline_text = timeline_elem.get_text(separator='\n', strip=True)
            timeline_text = timeline_text.replace('<br>', '\n')
            timeline_text = timeline_text.strip()

            timeline_items = []
            for p_tag in timeline_header.find_next_siblings('p'):
                for line in p_tag.get_text(separator='\n', strip=True).split('\n'):
                    timeline_items.append(line.strip())
            timeline_text = '\n'.join(timeline_items)

        return details_text, timeline_text