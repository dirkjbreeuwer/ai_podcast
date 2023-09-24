"""
Embedding services for generating embeddings for textual content.
"""

from abc import ABC, abstractmethod
from typing import List
import os

# pylint: disable=import-error
from dotenv import load_dotenv

from langchain.embeddings import FakeEmbeddings
from langchain.embeddings import HuggingFaceBgeEmbeddings
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.schema.embeddings import Embeddings


# pylint: disable=too-few-public-methods
class EmbeddingService(ABC):
    """
    Abstract base class for embedding services.

    Provides an interface for services that generate embeddings for textual content.
    """

    @abstractmethod
    def generate_embedding(self, text_chunk: str) -> List[float]:
        """
        Generate embeddings for a given text chunk.

        Parameters:
            text_chunk (str): The text for which the embedding should be generated.

        Returns:
            List[float]: The generated embedding.
        """


class OpenAIEmbeddingService(EmbeddingService):
    """
    Embedding service using OpenAI's embeddings.
    """

    def __init__(self, openai_api_key: str = None):
        # If no API key is provided, try to load it from .env
        if openai_api_key is None:
            load_dotenv()
            openai_api_key = os.getenv("OPENAI_API_KEY")
            print(f"OpenAI API Key after os.getenv: {openai_api_key}")
            if not openai_api_key:
                # pylint: disable=line-too-long
                print(f"OpenAI API Key: {openai_api_key}")
                raise ValueError(
                    "No OpenAI API key provided and none found in environment variables."
                )
        self.embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

    def generate_embedding(self, text_chunk: str) -> List[float]:
        return self.embeddings.embed_query(text_chunk)


class FakeEmbeddingService(EmbeddingService):
    """
    Fake embedding service for testing purposes.
    """

    def __init__(self, size: int = 1481):
        self.embeddings = FakeEmbeddings(size=size)

    def generate_embedding(self, text_chunk: str) -> List[float]:
        return self.embeddings.embed_query(text_chunk)


class HuggingFaceBGEEmbeddingService(EmbeddingService):
    """
    Embedding service using HuggingFace's BGE embeddings.
    """

    def __init__(
        self,
        model_name: str = "BAAI/bge-small-en",
        model_kwargs: dict = None,
        encode_kwargs: dict = None,
    ):
        self.embeddings = HuggingFaceBgeEmbeddings(
            model_name=model_name,
            model_kwargs=model_kwargs or {"device": "cpu"},
            encode_kwargs=encode_kwargs or {"normalize_embeddings": False},
        )

    def generate_embedding(self, text_chunk: str) -> List[float]:
        return self.embeddings.embed_query(text_chunk)


class HuggingFaceToLangchainEmbeddingAdapter(Embeddings):
    """
    Adapter to make HuggingFaceBGEEmbeddingService compatible with LangChain's Embeddings interface.

    Attributes:
        huggingface_service (HuggingFaceBGEEmbeddingService): The HuggingFace embedding service.
    """

    def __init__(self, huggingface_service: HuggingFaceBGEEmbeddingService):
        """Initialize the adapter with a HuggingFace embedding service."""
        self.huggingface_service = huggingface_service

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Embed multiple documents.

        Args:
            texts (List[str]): List of documents to embed.

        Returns:
            List[List[float]]: List of embeddings for each document.
        """
        return [self.huggingface_service.generate_embedding(text) for text in texts]

    def embed_query(self, text: str) -> List[float]:
        """
        Embed a single query.

        Args:
            text (str): Query text to embed.

        Returns:
            List[float]: Embedding of the query.
        """
        return self.huggingface_service.generate_embedding(text)
