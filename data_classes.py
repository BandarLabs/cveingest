from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Vulnerability:
    package_name: str
    ecosystem: str
    first_patched_version: Optional[str]
    vulnerable_version_range: str

    def to_dict(self):
        return {
            "package_name": self.package_name,
            "ecosystem": self.ecosystem,
            "first_patched_version": self.first_patched_version,
            "vulnerable_version_range": self.vulnerable_version_range,
        }


@dataclass
class Advisory:
    ghsa_id: str
    cve_id: Optional[str]
    url: str
    html_url: str
    summary: str
    description: str
    severity: str
    published_at: str
    updated_at: str
    assigner_name: str
    source_code: Optional[str]
    stars: Optional[int]
    cvss_scrore: float
    vulnerabilities: List[Vulnerability] = field(default_factory=list)
    references: List[str] = field(default_factory=list)

    def to_dict(self):
        return {
            "ghsa_id": self.ghsa_id,
            "cve_id": self.cve_id,
            "url": self.url,
            "html_url": self.html_url,
            "summary": self.summary,
            "description": self.description,
            "severity": self.severity,
            "published_at": self.published_at,
            "updated_at": self.updated_at,
            "source_code": self.source_code,
            "cvss_score": self.cvss_scrore,
            "vulnerabilities": [vul.to_dict() for vul in self.vulnerabilities],
            "references": self.references,
            "assigner_name": self.assigner_name
        }
