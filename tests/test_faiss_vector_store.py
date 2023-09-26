"""
Test Module for FAISSStore.

This module contains unit tests for the FAISSStore class, ensuring its proper
integration with the HuggingFaceBGEEmbeddingService and the adapter pattern.

Dependencies:
    - Requires `pytest`, `pytest-asyncio`, and `numpy`.

Classes:
    - TestFAISSStore: Contains unit tests for the FAISSStore class.
"""
import unittest

# pylint: disable=import-error
import pytest
import numpy as np

from src.search_and_retrieval.faiss_vector_store import FAISSStore

# pylint disable=line-too-long

from src.search_and_retrieval.preprocessing_services.embedding_service import (
    HuggingFaceBGEEmbeddingService,
    GenericEmbeddingAdapter,
    OpenAIEmbeddingService,
)


class TestFAISSStore(unittest.TestCase):
    """
    Test class for the FAISSStore.

    This class contains unit tests that ensure the functionality and behavior
    of the FAISSStore class, especially its integration with the embedding service
    and the adapter pattern.
    """

    def setUp(self):
        """
        Set up the test environment.

        Initializes the HuggingFaceBGEEmbeddingService, the adapter, and the FAISSStore.
        """
        # Initialize the HuggingFaceBGEEmbeddingService
        # huggingface_service = HuggingFaceBGEEmbeddingService()
        openai_service = OpenAIEmbeddingService()

        # Use the adapter to adapt the HuggingFaceBGEEmbeddingService
        # to the expected Embeddings interface
        adapter = GenericEmbeddingAdapter(openai_service)

        # Initialize the FAISSStore with the adapter
        self.faiss_store = FAISSStore(adapter)

    def test_initialization(self):
        """Test the initialization of the FAISSStore."""
        self.assertIsNone(self.faiss_store.index)

    def test_embedding_structure(self):
        """Test the structure of generated embeddings."""
        embeddings = [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]
        # Assert that the first embedding is a list or array
        assert isinstance(
            embeddings[0], (list, np.ndarray)
        ), "Embedding should be a list or array"
        # Assert that the length of the first embedding is 3
        assert len(embeddings[0]) == 3, "Embedding length should be 3"

    def generate_sample_texts_and_embeddings(self, num_samples: int = 2):
        """
        Generate sample texts and their embeddings.

        Args:
            num_samples (int): Number of sample texts to generate.

        Returns:
            tuple: A tuple containing lists of sample texts and their embeddings.
        """
        # Generate sample texts
        texts = [f"Sample text {i}" for i in range(num_samples)]

        # Use the adapter to generate embeddings for the sample texts
        embeddings = [self.faiss_store.embeddings.embed_query(text) for text in texts]

        return texts, embeddings

    def test_index_documents(self):
        """Test the indexing of documents in the FAISSStore."""
        texts, embeddings = self.generate_sample_texts_and_embeddings()
        metadata_list = [{"article_id": str(i + 1)} for i in range(len(texts))]
        self.faiss_store.index_documents(texts, embeddings, metadata_list)
        self.assertIsNotNone(self.faiss_store.index)

    async def test_similarity_search(self):
        """Test the asynchronous similarity search functionality of the FAISSStore."""
        texts, embeddings = self.generate_sample_texts_and_embeddings()
        metadata_list = [{"article_id": str(i + 1)} for i in range(len(texts))]
        self.faiss_store.index_documents(texts, embeddings, metadata_list)
        results = await self.faiss_store.similarity_search(embeddings[0], k=1)
        self.assertEqual(len(results), 1)
        self.assertIn("article_id", results[0][2])

    def test_similarity_search_with_sample_data(self):
        """Test the similarity search functionality with sample data."""
        # Sample data
        query = "I like to eat apples"
        texts = [
            "I like to eat oranges",
            "I like to eat burgers",
            "I like to shower",
            "My car broke down",
            "France is a country in Europe",
        ]

        # Generate embeddings for the texts
        embeddings = [self.faiss_store.embeddings.embed_query(text) for text in texts]

        # Metadata for the texts
        metadata_list = [{"id": i, "title": f"Document {i}"} for i in range(len(texts))]

        # Index the documents
        self.faiss_store.index_documents(texts, embeddings, metadata_list)

        # Perform similarity search
        results = self.faiss_store.similarity_search(query, k=6)

        # Print the results
        print("Query:", query)
        print("Results (in order of similarity):")
        for idx, (doc_id, score, metadata, chunk_text) in enumerate(results):
            print(
                f"{idx + 1}. {doc_id} {metadata['title']} (Score: {score}): {chunk_text}"
            )

        # Check the results
        self.assertEqual(len(results), 5)
        for result in results:
            self.assertIn(result[2]["title"], [f"Document {i}" for i in range(5)])

        # Check if "France is a country in Europe" is ranked the lowest
        france_doc_rank = [result[2]["title"] for result in results].index("Document 4")
        self.assertEqual(france_doc_rank, len(results) - 1)

    @pytest.mark.asyncio
    async def test_save_and_load_index(self):
        """Test the save and load functionality of the FAISSStore's index."""
        texts, embeddings = self.generate_sample_texts_and_embeddings()
        metadata_list = [{"article_id": str(i + 1)} for i in range(len(texts))]
        self.faiss_store.index_documents(texts, embeddings, metadata_list)
        self.faiss_store.save_index("temp_index")

        # Create a new adapter and FAISSStore instance
        huggingface_service = HuggingFaceBGEEmbeddingService()
        adapter = GenericEmbeddingAdapter(huggingface_service)
        new_store = FAISSStore(adapter)

        new_store.load_index("temp_index")
        results_original = await self.faiss_store.similarity_search(embeddings[0], k=1)
        results_new = await new_store.similarity_search(embeddings[0], k=1)
        self.assertEqual(results_original, results_new)

    def test_search_without_indexing(self):
        """Test searching without indexing to ensure it raises an exception."""
        with self.assertRaises(Exception):
            self.faiss_store.similarity_search([0.1, 0.2, 0.3], k=1)

    def test_invalid_save_path(self):
        """Test saving the index from an invalid path to ensure it raises an exception."""

        with self.assertRaises(Exception):
            self.faiss_store.save_index("/invalid/path")

    def test_invalid_load_path(self):
        """Test loading the index from an invalid path to ensure it raises an exception."""
        with self.assertRaises(Exception):
            self.faiss_store.load_index("/invalid/path")


if __name__ == "__main__":
    unittest.main()
