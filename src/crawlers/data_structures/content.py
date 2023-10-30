"""
This module defines the abstract base class for representing different content types.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
import uuid
import logging


# pylint: disable=R0902
class Content(ABC):
    """
    Represents the abstract base class for content types.
    """

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
    ):
        """Initializes a Content instance with provided attributes."""
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
        self.text = text
        self._id = _id or str(uuid.uuid4())

        logging.info("Content instance created for title: %s", self.title)

    def __repr__(self):
        """Returns a string representation of the Content instance."""
        return f"<Content(title={self.title}, url={self.url}, date={self.date})>"

    @abstractmethod
    def get_summary(self) -> str:
        """Abstract method for getting a summary of the content."""

    @abstractmethod
    def get_type(self):
        """Abstract method for getting the type of the content."""

    @abstractmethod
    def get_relevance(self):
        """Abstract method for getting the relevance of the content."""

    @property
    def content_id(self):
        """Property to get the content's ID."""
        return self._id

    @content_id.setter
    def content_id(self, value):
        """Setter for the content's ID."""
        self._id = value
