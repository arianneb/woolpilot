from abc import ABC, abstractmethod

class BaseParser(ABC):
    # return a list of product dictionaries parsed from a search results HTML page
    @abstractmethod
    def parse_search_results(self, html: str) -> List[Dict]:
        pass
