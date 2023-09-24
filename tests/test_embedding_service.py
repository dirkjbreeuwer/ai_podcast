"""
Module for testing the functionality of the EmbeddingService and its derived classes.

This module contains unit tests that validate the behavior of the embedding services,
ensuring they generate embeddings as expected and handle edge cases appropriately.
"""

import unittest
import os
from unittest.mock import patch
from src.search_and_retrieval.preprocessing_services.embedding_service import (
    OpenAIEmbeddingService,
    FakeEmbeddingService,
    HuggingFaceBGEEmbeddingService,
    EmbeddingService,
)


class TestEmbeddingService(unittest.TestCase):
    """
    Test suite for the EmbeddingService and its derived classes.
    """

    # Explicitly unset the OPENAI_API_KEY environment variable
    os.environ.pop("OPENAI_API_KEY", None)

    def test_abstract_class_instantiation(self):
        """
        Test that instantiating the abstract base class directly raises a TypeError.
        """
        with self.assertRaises(TypeError):
            # pylint: disable=abstract-class-instantiated
            _ = EmbeddingService()

    def test_openai_api_key_loading(self):
        """
        Test the OpenAIEmbeddingService's behavior when no API key is provided or found.
        """
        # Mock os.getenv to always return None, and also mock load_dotenv to do nothing
        with patch(
            "src.search_and_retrieval.preprocessing_services.embedding_service.os.getenv",
            return_value=None,
        ), patch(
            "src.search_and_retrieval.preprocessing_services.embedding_service.load_dotenv",
            return_value=None,
        ):
            # This should raise a ValueError since no API key is provided and none is
            # found in the environment
            with self.assertRaises(ValueError):
                _ = OpenAIEmbeddingService()

            # This should also raise a ValueError since an empty string is provided as the API key
            with self.assertRaises(ValueError):
                _ = OpenAIEmbeddingService(openai_api_key="")

    @unittest.skip("This test makes an actual API call. Remove if you want to run it.")
    def test_openai_embedding_generation(self):
        """
        Test the generation of embeddings using the OpenAIEmbeddingService.
        """
        service = OpenAIEmbeddingService()
        embedding = service.generate_embedding("sample text")
        self.assertTrue(isinstance(embedding, list))
        self.assertTrue(all(isinstance(val, float) for val in embedding))

    def test_fake_embedding_default_size(self):
        """
        Test the default size of embeddings generated by the FakeEmbeddingService.
        """
        service = FakeEmbeddingService()
        embedding = service.generate_embedding("sample text")
        self.assertEqual(len(embedding), 1481)

    def test_fake_embedding_generation(self):
        """
        Test the generation of embeddings of a specified size using the FakeEmbeddingService.
        """
        service = FakeEmbeddingService(size=10)
        embedding = service.generate_embedding("sample text")
        self.assertEqual(len(embedding), 10)

    def test_huggingface_default_model(self):
        """
        Test the default model used by the HuggingFaceBGEEmbeddingService.
        """
        service = HuggingFaceBGEEmbeddingService()
        # Check if the default model is set (you can add more checks if needed)
        self.assertEqual(service.embeddings.model_name, "BAAI/bge-small-en")

    def test_huggingface_embedding_generation(self):
        """
        Test the generation of embeddings using the HuggingFaceBGEEmbeddingService.
        """
        service = HuggingFaceBGEEmbeddingService()
        embedding = service.generate_embedding("sample text")
        self.assertTrue(isinstance(embedding, list))
        self.assertTrue(all(isinstance(val, float) for val in embedding))

    def test_huggingface_embedding_api_call(self):
        """
        Test the API call and embedding generation of the HuggingFaceBGEEmbeddingService.
        """
        # Initialize the HuggingFace BGE embedding service
        service = HuggingFaceBGEEmbeddingService()

        # Provide a sample text for embedding
        sample_text = "This is a sample text for embedding."

        # Generate the embedding
        embedding = service.generate_embedding(sample_text)

        # Assertions to check the structure
        self.assertTrue(isinstance(embedding, list))
        self.assertTrue(all(isinstance(val, float) for val in embedding))


if __name__ == "__main__":
    unittest.main()
