import requests
import os
import time
from reference_crawlers.base_reference_crawler import BaseReferenceCrawler

class NISTReferenceCrawler(BaseReferenceCrawler):
    def fetch_reference(self, url: str, cve_id: str) -> dict:
        # Define the maximum number of retries and the backoff time (in seconds)
        max_retries = 3
        backoff_time = 5

        try:
            # Fetch the API key from the environment variable
            api_key = os.getenv('NIST_API_KEY')

            # Split the URL by '/' and get the last segment
            cve_id_parts = url.split('/')
            cve_id = cve_id_parts[-1]

            if not cve_id.startswith("CVE-"):
                return {"url": url, "type": "NIST", "error": "Invalid CVE ID format"}

            # Construct the API URL
            api_url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?cveId={cve_id}"

            # Prepare headers, optionally including the API key
            headers = {}
            if api_key:
                headers["apiKey"] = api_key

            attempt = 0
            while attempt <= max_retries:
                try:
                    response = requests.get(api_url, headers=headers, timeout=10)
                    response.raise_for_status()
                    data = response.json()  # Parse the response as JSON

                    vulnerabilities = data.get("vulnerabilities", [])
                    if not vulnerabilities:
                        return {"url": url, "type": "NIST", "status_code": response.status_code, "error": "No vulnerabilities found"}

                    # Extract information from the first vulnerability entry
                    vulnerability = vulnerabilities[0].get("cve", {})
                    descriptions = vulnerability.get("descriptions", [{"lang": "en", "value": "No description available"}])
                    english_description = next((desc['value'] for desc in descriptions if desc['lang'] == 'en'), "No description available")

                    return {
                        "url": url,
                        "type": "NIST",
                        "status_code": response.status_code,
                        "info": english_description[:5000],
                    }
                except requests.exceptions.RequestException as e:
                    if attempt == max_retries:
                        return {"url": url, "type": "NIST", "error": str(e)}
                    else:
                        time.sleep(backoff_time)
                        attempt += 1
        except Exception as e:
            return {"url": url, "type": "NIST", "error": str(e)}