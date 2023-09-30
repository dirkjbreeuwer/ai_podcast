"""
Vector Store Module

Defines the `VectorStore` abstract base class for consistent vector operations.
Designed for extensibility with various vector storage technologies.

Key Features:
    - Core vector operations as abstract methods.
    - Initialization with API key, environment, and config.

Classes:
    - VectorStore: Base class for vector operations.

Note:
    Abstract base class; requires subclassing and method implementations.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional, TypedDict


class QueryResult(TypedDict):
    """
    Represents the result of a query in the vector store.

    Attributes:
        ids (List[str]): List of document IDs.
        embeddings (Optional[List[List[float]]]): List of embeddings for the documents.
        documents (Optional[List[str]]): List of document texts.
        metadatas (Optional[List[Dict[str, str]]]): List of metadata associated with the documents.
        distances (Optional[List[float]]): List of distances or similarity scores for the documents.
    """

    ids: List[str]
    embeddings: Optional[List[List[float]]]
    documents: Optional[List[str]]
    metadatas: Optional[List[Dict[str, str]]]
    distances: Optional[List[float]]


class VectorStore(ABC):
    """
    Abstract base class for vector store operations.

    This class provides a consistent interface for vector operations
    regardless of the underlying technology.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        environment: Optional[str] = None,
        config: Optional[Dict[str, str]] = None,
    ):
        """
        Initializes the VectorStore with optional parameters.

        Args:
            api_key (str, optional): API key or authentication token.
            environment (str, optional): Environment or endpoint URL.
            config (Dict[str, str], optional): Additional configuration settings.
        """
        self.api_key = api_key
        self.environment = environment
        self.config = config if config else {}

    @abstractmethod
    def create_collection(self, name: str) -> None:
        """
        Creates a new collection to store embeddings and associated metadata.

        Args:
            name (str): Name of the collection.

        Returns:
            None
        """

    @abstractmethod
    def query_collection(self, query_texts: List[str], n_results: int) -> QueryResult:
        """
        Queries the collection and returns the most similar documents.

        Args:
            query_texts (List[str]): List of query texts.
            n_results (int): Number of results to return.

        Returns:
            List[Tuple[int, float]]: List of (index, similarity_score) tuples.
        """

    @abstractmethod
    def add_documents(
        self,
        texts: List[str],
        embeddings: Optional[List[List[float]]] = None,
        metadata_list: Optional[List[Dict[str, str]]] = None,
        ids: Optional[List[str]] = None,
    ) -> None:
        """
        Adds documents and their associated embeddings and metadata to the collection.

        Args:
            texts (List[str]): List of documents to be added.
            embeddings (List[List[float]], optional): List of embeddings.
            If not provided, embeddings will be generated.
            metadata_list (List[Dict], optional): Metadata associated with each document.
            ids (List[str], optional): IDs for each document.

        Returns:
            None
        """

    @abstractmethod
    def remove_documents(self, ids: List[str]) -> None:
        """
        Removes documents from the collection based on their IDs.

        Args:
            ids (List[str]): IDs of the documents to be removed.

        Returns:
            None
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
