"""
Web Crawlers Module

This module provides the foundational structure for creating and managing web crawlers
to scrape articles from various online platforms.

The primary component of this module is the `Crawler` base class, which outlines
the core functionalities expected of any web crawler, ensuring consistency in scraping,
transforming, and managing articles.

Classes:
    Crawler: The base class for web crawlers, ensuring consistent scraping
    across various web sources.
"""
from typing import List, Dict, Union


class Crawler:
    """
    Base class for web crawlers to ensure consistency in scraping articles.

    Attributes:
        name (str): The name of the crawler.
        config (Dict[str, Union[str, int, bool]]): Configuration settings specific to the crawler.
    """

    def __init__(self, name: str, config: Dict[str, Union[str, int, bool]]) -> None:
        """
        Initializes the Crawler with a name and specific configurations.

        Args:
            name (str): The name of the crawler.
            config (Dict[str, Union[str, int, bool]]): Configuration settings specific to
            the crawler.
        """
        self.name = name
        self.config = config

    def fetch(self, url: str) -> Dict:
        """
        Fetch a single article from a given URL.

        Args:
            url (str): The URL to fetch the article from.

        Returns:
            Dict: The scraped article data.

        Note:
            This method should be overridden by child classes.
        """
        raise NotImplementedError(
            "The fetch method should be implemented in child classes."
        )

    def batch_fetch(self, urls: List[str]) -> List[Dict]:
        """
        Fetch multiple articles from a list of URLs.

        Args:
            urls (List[str]): A list of URLs to fetch articles from.

        Returns:
            List[Dict]: A list of scraped article data.

        Note:
            This method can leverage the fetch method for individual URL fetching.
            Alternatively, child classes can provide a more efficient batch processing method.
        """
        return [self.fetch(url) for url in urls]

    def get_status(self) -> str:
        """
        Get the current status of the crawler.

        Returns:
            str: The status of the crawler.

        Note:
            This method should be overridden by child classes if specific status
            reporting is needed.
        """
        return f"Crawler {self.name} is operational."
