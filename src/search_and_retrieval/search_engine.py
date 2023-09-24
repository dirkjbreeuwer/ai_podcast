"""
Search and Retrieval Module.

Provides an abstract base class (SearchEngine) for search engines.
"""

from abc import ABC, abstractmethod
from typing import List, Tuple


class SearchEngine(ABC):
    """Abstract base class for search engines."""

    @abstractmethod
    def convert_query_to_vector(self, query: str) -> List[float]:
        """Convert a text query to its vector representation."""

    @abstractmethod
    def execute_similarity_search(
        self, query_vector: List[float]
    ) -> List[Tuple[int, float]]:
        """Execute a similarity search using a query vector."""

    @abstractmethod
    def execute_advanced_search(
        self, query_vector: List[float], metadata: dict
    ) -> List[Tuple[int, float]]:
        """Execute an advanced search using a query vector and metadata."""
