import requests
import random
from typing import List, Optional
from datetime import datetime, timedelta
from data_classes import Vulnerability, Advisory
# from time import sleep

class GitHubAdvisoryCrawler:
    BASE_URL = "https://api.github.com/advisories"

    def __init__(self, token: str):
        self.headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2022-11-28",
        }

    def get_stars(self, url: str) -> int:
        # Parse the owner and repo name from the URL
        try:
            # Example URL: https://github.com/tensorflow/tensorflow
            parts = url.strip().split('/')
            owner = parts[-2]
            repo = parts[-1]
        except IndexError:
            print(f"Invalid GitHub URL format {url}")
            return 0

        # Construct API URL
        api_url = f"https://api.github.com/repos/{owner}/{repo}"

        attempt = 0
        max_attempts = 2

        while attempt < max_attempts:
            try:
                # Send request to GitHub API
                response = requests.get(api_url, headers={"Accept": "application/vnd.github.v3+json"})
                response.raise_for_status()  # Raise an exception for HTTP errors

                # Parse the JSON response and extract the stargazers count
                data = response.json()
                return data.get("stargazers_count", 0)
            except requests.exceptions.RequestException as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                attempt += 1

        # Return 0 if all attempts fail
        return 0

    def fetch_advisories(
        self,
        last: Optional[int] = None,
        start_date: Optional[str] = None,  # Added start_date parameter
        end_date: Optional[str] = None,    # Added end_date parameter
        severity: Optional[str] = 'critical',
        random_from_last_days: Optional[int] = None
    ) -> Optional[List[Advisory]]:
        """
        Fetch advisories from the GitHub API with optional filters and convert them to Advisory objects.

        :param last: Fetch only the latest n advisories
        :param start_date: Fetch advisories published on or after this date (format YYYY-MM-DD)
        :param end_date: Fetch advisories published on or before this date (format YYYY-MM-DD)
        :param severity: Filter advisories by severity level (critical, high, medium)
        :param random_from_last_days: Fetch a random advisory from the last specified number of days

        :return: List of Advisory objects, or a single random Advisory if random_from_last_days is specified.
        """

        # Determine the date range for the query
        if start_date or end_date:
            if not start_date:
                # If start_date is not provided, default to a very early date
                start_date = datetime.now().strftime('%Y-%m-%d')
            if not end_date:
                # If end_date is not provided, default to today's date
                end_date = datetime.now().strftime('%Y-%m-%d')
            published = f"{start_date}..{end_date}"
        else:
            published = None

        # Construct query params
        params = {"per_page": 100}
        if published:
            params['published'] = published
        if severity:
            params['severity'] = severity

        # Make request with query parameters
        response = requests.get(self.BASE_URL, headers=self.headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch advisories: {response.status_code}")

        advisories = response.json()

        # Filter by severity
        if severity:
            advisories = [adv for adv in advisories if adv.get("severity") == severity]

        # Fetch only the latest n advisories
        if last:
            advisories = advisories[:last]

        # Convert advisories to Advisory objects
        advisory_objects = []
        for adv in advisories:
            vulnerabilities = [
                Vulnerability(
                    package_name=vul["package"]["name"],
                    ecosystem=vul["package"]["ecosystem"],
                    first_patched_version=vul.get("first_patched_version"),
                    vulnerable_version_range=vul["vulnerable_version_range"],
                )
                for vul in adv.get("vulnerabilities", [])
            ]
            advisory = Advisory(
                ghsa_id=adv["ghsa_id"],
                cve_id=adv.get("cve_id"),
                url=adv["url"],
                html_url=adv["html_url"],
                summary=adv["summary"],
                description=adv["description"],
                severity=adv["severity"],
                published_at=adv["published_at"],
                updated_at=adv["updated_at"],
                vulnerabilities=vulnerabilities,
                references=adv.get("references", []),
                assigner_name='',
                source_code=adv.get('source_code_location', None),
                stars=self.get_stars(adv.get('source_code_location', None)),
                cvss_scrore=adv.get('cvss', {}).get('score') or 0
            )
            advisory_objects.append(advisory)

        # Return a random advisory if specified
        if random_from_last_days:
            if not advisory_objects:
                return None
            return [random.choice(advisory_objects)]

        return advisory_objects
# Example usage:
# crawler = GitHubAdvisoryCrawler(token="your_github_token")
# random_advisory_7_days = crawler.fetch_advisories(random_from_last_days=7)
# if random_advisory_7_days:
#     print(f"Random Advisory ID: {random_advisory_7_days[0].ghsa_id}")