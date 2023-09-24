"""
Vector Store Module

This module provides an abstract base class for vector store operations,
ensuring a consistent interface for indexing, searching, saving, and loading
vector embeddings regardless of the underlying technology.

The primary purpose of this module is to empower users to efficiently and
comprehensively query and fetch articles based on a query, delivering relevant
search results using vector embeddings.

Classes:
    - VectorStore: Abstract base class for vector store operations.

Future implementations can derive from the VectorStore class to provide
specific implementations using technologies like FAISS, Annoy, etc.
"""
from abc import ABC, abstractmethod
from typing import List, Tuple, Dict


class VectorStore(ABC):
    """
    Abstract base class for vector store operations.

    This class provides a consistent interface for vector operations
    regardless of the underlying technology.
    """

    @abstractmethod
    def index_documents(
        self,
        texts: List[str],
        embeddings: List[List[float]],
        metadata_list: List[Dict[str, str]],
    ) -> None:
        """
        Indexes the provided embeddings along with their associated metadata.

        Args:
            embeddings (List[List[float]]): List of embeddings to be indexed.
            metadata_list (List[Dict]): List of metadata associated with each embedding.

        Returns:
            None
        """

    @abstractmethod
    def similarity_search(self, query_vector: List[float]) -> List[Tuple[int, float]]:
        """
        Performs a similarity search using the provided query vector.

        Args:
            query_vector (List[float]): Query vector for similarity search.

        Returns:
            List[Tuple[int, float]]: List of (index, similarity_score) tuples.
        """

    @abstractmethod
    def save_index(self, file_path: str) -> None:
        """
        Saves the current index to the specified file path.

        Args:
            file_path (str): Path to save the index.

        Returns:
            None
        """

    @abstractmethod
    def load_index(self, file_path: str) -> None:
        """
        Loads the index from the specified file path.

        Args:
            file_path (str): Path to load the index from.

        Returns:
            None
        """
