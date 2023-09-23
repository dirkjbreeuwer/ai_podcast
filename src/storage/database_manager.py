"""
DatabaseManager Module: Provides an abstract interface for foundational database interactions
related to articles, including CRUD operations, vectorization status checks, and batch saving.

Attributes:
    Article: A placeholder class representing the structure of an article.

Classes:
    DatabaseManager: Abstract Base Class for foundational database interactions.
"""

from abc import ABC, abstractmethod

from src.crawlers.data_structures.article import Article


class DatabaseManager(ABC):
    """
    Abstract Base Class for foundational database interactions.

    This class provides an interface for CRUD operations on articles and additional
    functionalities like checking vectorization status and batch saving.
    """

    @abstractmethod
    def save(self, article: Article) -> None:
        """
        Persist a new article.

        Parameters:
            article (Article): The article to be saved.

        Returns:
            None
        """

    @abstractmethod
    def update(self, article: Article) -> None:
        """
        Modify an existing article.

        Parameters:
            article (Article): The article to be updated.

        Returns:
            None
        """

    @abstractmethod
    def delete(self, article_id: int) -> None:
        """
        Remove an article by its ID.

        Parameters:
            article_id (int): The ID of the article to be deleted.

        Returns:
            None
        """

    @abstractmethod
    def find_by_id(self, article_id: int) -> Article:
        """
        Retrieve a specific article by its ID.

        Parameters:
            article_id (int): The ID of the article to be retrieved.

        Returns:
            Article: The retrieved article.
        """

    @abstractmethod
    def find_all(self) -> list[Article]:
        """
        Retrieve all articles.

        Returns:
            list[Article]: A list of all articles.
        """

    @abstractmethod
    def find_by_criteria(self, criteria: dict) -> list[Article]:
        """
        Retrieve articles based on certain criteria.

        Parameters:
            criteria (dict): A dictionary of criteria to filter articles.

        Returns:
            list[Article]: A list of articles that match the criteria.
        """

    @abstractmethod
    def mark_as_vectorized(self, article_id: int) -> None:
        """
        Set the vectorization flag for an article.

        Parameters:
            article_id (int): The ID of the article to be marked.

        Returns:
            None
        """

    @abstractmethod
    def is_vectorized(self, article_id: int) -> bool:
        """
        Check the vectorization status for an article.

        Parameters:
            article_id (int): The ID of the article to check.

        Returns:
            bool: True if the article is vectorized, False otherwise.
        """

    @abstractmethod
    def batch_save(self, articles: list[Article]) -> None:
        """
        Persist multiple articles at once.

        Parameters:
            articles (list[Article]): A list of articles to be saved.

        Returns:
            None
        """
