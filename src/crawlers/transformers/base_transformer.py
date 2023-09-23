"""
Provides a base class for transforming crawler outputs into the standardized Article format.

The `CrawlerOutputTransformer` class is an abstract base class designed to ensure
consistent transformation of diverse crawler outputs into the Article data structure.

Classes:
    - CrawlerOutputTransformer: Abstract base class for output transformation.

Usage:
    class MyTransformer(CrawlerOutputTransformer):
        def transform(self, raw_data: dict) -> Article:
            # Specific implementation
            ...

    transformer = MyTransformer()
    raw_data = {
        "url": "https://example.com",
        "title": "Sample Article",
        "text": "Sample content.",
        "date": "2021-01-01"
    }
    article = transformer.transform(raw_data)
"""

from abc import ABC, abstractmethod
from ..data_structures.article import Article


# This is a base class so its OK to have too few public methods
# pylint: disable=too-few-public-methods
class CrawlerOutputTransformer(ABC):
    """
    Abstract base class for transforming crawler outputs into the Article data type.
    """

    @abstractmethod
    def transform(self, raw_data: dict) -> Article:
        """
        Transforms raw data into an Article instance.

        Args:
            raw_data (dict): The raw data to be transformed.

        Returns:
            Article: The transformed Article instance.
        """
