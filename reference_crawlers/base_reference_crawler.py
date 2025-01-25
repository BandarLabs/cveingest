from abc import ABC, abstractmethod

class BaseReferenceCrawler(ABC):
    @abstractmethod
    def fetch_reference(self, url: str, cve_id: str) -> dict:
        """
        Fetches and processes a reference URL.
        Must be implemented by subclasses.
        """
        pass
