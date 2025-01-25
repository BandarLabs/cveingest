import requests
from typing import List
from data_classes import Vulnerability, Advisory  # Ensure these are defined appropriately
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CVECrawler:
    NVD_BASE_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0/"
    CIRCL_BASE_URL = "https://cve.circl.lu/api/cve/"

    def __init__(self):
        self.headers = {
            "Accept": "application/json"
        }

    def fetch_cve_ids(self, start_date: str, end_date: str, cvss_version: str) -> List[str]:
        url = (
            f"{self.NVD_BASE_URL}?resultsPerPage=2000&startIndex=0"
            f"&pubStartDate={start_date}T00:00:00.000&pubEndDate={end_date}T23:59:59.999"
            f"&cvssV{cvss_version}Severity=CRITICAL"
        )

        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch CVE IDs: {response.status_code}")

        data = response.json()
        vulnerabilities = data.get("vulnerabilities", [])
        return [vuln.get("cve", {}).get("id") for vuln in vulnerabilities if vuln.get("cve")]

    def fetch_cve_details_from_circl(self, cve_id: str) -> dict:
        """
        Fetch detailed CVE information from the CIRCL API for a given CVE ID.
        """
        response = requests.get(f"{self.CIRCL_BASE_URL}{cve_id}", headers=self.headers)
        if response.status_code != 200:
            print(f"Failed to fetch details for {cve_id} from CIRCL: {response.status_code}")
            return {}
        return response.json()

    def fetch_advisories(self, start_date: str, end_date: str) -> List[Advisory]:
        cve_ids_v3 = self.fetch_cve_ids(start_date, end_date, '3')
        cve_ids_v4 = self.fetch_cve_ids(start_date, end_date, '4')

        all_cve_ids = set(cve_ids_v3 + cve_ids_v4)
        advisory_objects = []

        for cve_id in all_cve_ids:
            cve_details = self.fetch_cve_details_from_circl(cve_id)
            if not cve_details:
                continue

            containers = cve_details.get("containers", {}).get("cna", {})
            cve_metadata = cve_details.get("cveMetadata", {})

            description = (
                containers.get("descriptions", [{}])[0].get("value", "")
            )
            published_at = cve_metadata.get("datePublished", "")
            date_updated = cve_metadata.get("dateUpdated", "")
            references = containers.get("references", [])
            # Retrieve severity, checking CVSS v4 first, then v3 if v4 is not available
            metrics = containers.get("metrics", [{}])[0]  # Getting the first metric container
            cvss_v4 = metrics.get("cvssV4_0", {})
            cvss_v3 = metrics.get("cvssV3_0", {})

            severity = cvss_v4.get("baseSeverity", cvss_v3.get("baseSeverity", "CRITICAL"))

            # Retrieve CVSS score, checking CVSS v4 first, then v3 if v4 is not available
            cvss_score = cvss_v4.get("baseScore", cvss_v3.get("baseScore", 0))

            # Log missing fields
            missing_fields = []
            if not description:
                missing_fields.append("description")
            if not published_at:
                missing_fields.append("published_at")
            if not date_updated:
                missing_fields.append("date_updated")
            if not references:
                missing_fields.append("references")

            if missing_fields:
                logger.info(f"Advisory {cve_id} missing fields: {', '.join(missing_fields)}")

            vulnerabilities = [
                Vulnerability(
                    package_name=cve_id,
                    ecosystem="UNKNOWN",  # Adjust to your specific context
                    first_patched_version=None,
                    vulnerable_version_range=None,
                )
            ]

            advisory = Advisory(
                ghsa_id=None,
                cve_id=cve_id,
                url=references[0]["url"] if references else "",
                html_url=references[0]["url"] if references else "",
                summary=description,
                description=description,
                severity=severity,
                published_at=published_at,
                updated_at=date_updated,
                vulnerabilities=vulnerabilities,
                references=[r["url"] for r in references],
                assigner_name=cve_metadata.get("assignerShortName", ""),
                cvss_scrore=cvss_score
            )
            advisory_objects.append(advisory)

        return advisory_objects
# Usage example
# crawler = CVECrawler()
# advisories = crawler.fetch_advisories("2025-01-14", "2025-01-20")
# for advisory in advisories:
#     print(advisory)