"""
This module defines the data structure for representing an article scraped from the web.
"""
from typing import List, Dict, Optional
import uuid


# pylint: disable=R0902
class Article:
    """
    Represents an article scraped from the web.

    Attributes:
        url (Optional[str]): The URL of the article.
        loaded_domain (Optional[str]): The domain from which the article was loaded.
        title (str): The title of the article.
        date (str): The publication date of the article.
        author (Optional[List[str]]): The authors of the article.
        description (Optional[str]): A brief description or summary of the article.
        keywords (Optional[str]): Keywords associated with the article.
        lang (Optional[str]): The language of the article.
        tags (Optional[List[str]]): Tags associated with the article.
        image (Optional[str]): The main image URL of the article.
        text (str): The main text content of the article.
        id (str): A unique identifier for the article.
        is_vectorized (bool): Indicates if the article has been vectorized.
    """

    # Disabling the too many arguments warning because we want Article
    # to be a comprehensive data model
    # pylint: disable=R0913
    def __init__(
        self,
        title: str,
        text: str,
        date: str,
        _id: Optional[str] = None,
        url: Optional[str] = None,
        loaded_domain: Optional[str] = None,
        author: Optional[List[str]] = None,
        description: Optional[str] = None,
        keywords: Optional[str] = None,
        lang: Optional[str] = None,
        tags: Optional[List[str]] = None,
        image: Optional[str] = None,
        videos: Optional[List[Dict[str, str]]] = None,
        is_vectorized: bool = False,  # Add this line
    ):
        """Initializes an Article instance with provided attributes."""
        self.url = url
        self.loaded_domain = loaded_domain
        self.title = title
        self.date = date
        self.author = author
        self.description = description
        self.keywords = keywords
        self.lang = lang
        self.tags = tags
        self.image = image
        self.videos = videos
        self.text = text
        self._id = _id or str(uuid.uuid4())
        self.is_vectorized = is_vectorized  # And this line

    def __repr__(self):
        """Returns a string representation of the Article instance."""
        return f"<Article(title={self.title}, url={self.url}, date={self.date})>"

    def get_summary(self) -> str:
        """Returns a summary of the article (this is just a placeholder
        and should be implemented properly)"""
        return self.text[:100] + "..."

    @property
    def article_id(self):
        """Property to get the article's ID."""
        return self._id

    @article_id.setter
    def article_id(self, value):
        """Setter for the article's ID."""
        self._id = value
