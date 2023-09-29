"""
ApifyArticleCrawler Module
--------------------------

This module provides the `ApifyArticleCrawler` class, a specialized web crawler tailored for the
Apify platform  using the Smart Article Extractor. It extends the base `Crawler` class
and offers methods to fetch articles from given URLs using Apify's Smart Article Extractor.

The module also integrates with the `decouple` library to securely load the Apify API key
from environment variables or configuration files.

Classes:
    - ApifyArticleCrawler: A web crawler tailored for the Apify platform.

Note:
    This module requires the `requests` and `decouple` libraries to be installed.
"""

from typing import List, Dict, Union

# pylint: disable=E0401
import requests

# pylint: disable=E0401
from decouple import config
from .base_crawler import Crawler


class ApifyArticleCrawler(Crawler):
    """
    Crawler tailored for the Apify platform using the Smart Article Extractor.

    Attributes:
        api_key (str): The API key for accessing Apify services.
    """

    def __init__(
        self,
        name: str,
        crawler_config: Dict[str, Union[str, int, bool]],
        api_key: str = None,  # Optional API key parameter
    ) -> None:
        super().__init__(name, crawler_config)
        if api_key:
            self.api_key = api_key
        else:
            self.api_key = self._load_api_key()

    def _load_api_key(self) -> str:
        # Load the API key using decouple's config function
        api_key = config("APIFY_API_KEY", default="")

        # Check if the API key is empty or None
        if not api_key:
            # pylint: disable=line-too-long
            raise ValueError(
                "No API key loaded from environment or provided. Please ensure you have the APIFY_API_KEY set in your environment or configuration."
            )
        print(api_key)
        return api_key

    def set_options(self, options: Dict) -> None:
        """
        Configuration setter for Apify.

        Args:
            options (Dict): Configuration settings specific to Apify.
        """
        self.config.update(options)

    # pylint: disable=R1710
    def fetch(self, url: str) -> Dict:
        """
        Fetch a single article from a given URL using the Apify Smart Article Extractor.

        Args:
            url (str): The URL to fetch the article from.

        Returns:
            Dict: The scraped article data.
        """
        # pylint: disable=C0301
        endpoint = f"https://api.apify.com/v2/acts/lukaskrivka~article-extractor-smart/run-sync-get-dataset-items?token={self.api_key}"
        payload = {"startUrls": [{"url": url}]}
        print(endpoint)
        timeout_seconds = 60 * 4  # 4 minutes

        response = requests.post(endpoint, json=payload, timeout=timeout_seconds)
        if response.status_code in [200, 201]:
            data = response.json()
            if isinstance(data, list) and data:
                return data[0]  # Return only the first article
            raise ValueError(
                f"Failed to fetch article from {url}. Status code: {response.status_code}"
            )

    def batch_fetch(self, urls: List[str]) -> List[Dict]:
        """
        Fetch multiple articles from a list of URLs using the Apify Smart Article Extractor.

        Args:
            urls (List[str]): A list of URLs to fetch articles from.

        Returns:
            List[Dict]: A list of scraped article data.
        """
        results = []
        for url in urls:
            # Since fetch returns only the first article, we need to handle multiple articles here
            data = self._fetch_all_articles(url)
            results.extend(data)
        return results

    def _fetch_all_articles(self, url: str) -> List[Dict]:
        """
        Fetch all articles from a given URL using the Apify Smart Article Extractor.

        Args:
            url (str): The URL to fetch the articles from.

        Returns:
            List[Dict]: A list of scraped article data.
        """
        # pylint: disable=C0301
        endpoint = f"https://api.apify.com/v2/acts/lukaskrivka~article-extractor-smart/run-sync-get-dataset-items?token={self.api_key}"
        payload = {"startUrls": [{"url": url}]}
        timeout_seconds = 60 * 4  # 4 minutes

        response = requests.post(endpoint, json=payload, timeout=timeout_seconds)
        if response.status_code in [200, 201]:
            data = response.json()
            if isinstance(data, list):
                return data
            raise ValueError(f"Unexpected data format from {url}.")
        raise ConnectionError(
            f"Failed to fetch articles from {url}. Status code: {response.status_code}"
        )

    def get_status(self) -> str:
        """
        Get the current status of the ApifyArticleCrawler.

        Returns:
            str: The status of the crawler.
        """
        # This can be enhanced to get the real-time status from Apify if they provide such an API.
        return f"ApifyArticleCrawler {self.name} is operational."
