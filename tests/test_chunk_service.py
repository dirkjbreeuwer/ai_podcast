"""
Test suite for the ChunkService implementations.

This module contains unit tests that validate the functionality of the chunking services.
These tests ensure that the services correctly split articles into chunks, handle edge cases,
respect chunk sizes and overlaps, and interact correctly with the Article class.

Usage:
    Run this test suite using pytest:
    $ pytest path_to_this_module.py
"""

import unittest
from src.crawlers.data_structures.article import Article
from src.search_and_retrieval.preprocessing_services.chunk_service import (
    ContentAwareChunkingService,
    LangChainChunkingService,
)


class TestChunkService(unittest.TestCase):
    """
    Test suite for the ChunkService implementations.
    """

    def setUp(self):
        """
        Set up the testing environment before each test case.

        This method initializes instances of the chunking services to be used in the test cases.
        """
        self.content_aware_service = ContentAwareChunkingService()
        self.lang_chain_service = LangChainChunkingService(
            chunk_size=100, chunk_overlap=20
        )

    def test_basic_functionality(self):
        """
        Test the basic functionality of the chunking services.

        This test ensures that both the ContentAwareChunkingService and the LangChainChunkingService
        correctly split articles into chunks and return lists of strings.
        """
        article = Article(
            title="Test",
            text="This is a sample article. It has multiple sentences.",
            date="2023-09-23",
        )
        # Test ContentAwareChunkingService
        chunks = self.content_aware_service.split_into_chunks(article)
        self.assertTrue(isinstance(chunks, list))
        self.assertTrue(all(isinstance(chunk, str) for chunk in chunks))

        # Test LangChainChunkingService
        chunks = self.lang_chain_service.split_into_chunks(article)
        self.assertTrue(isinstance(chunks, list))
        self.assertTrue(all(isinstance(chunk, str) for chunk in chunks))

    def test_edge_cases(self):
        """
        Test edge cases for the chunking services.

        This test covers scenarios such as empty article text, article text
        shorter than the specified chunk size, and article text with special
        characters or non-standard formatting.
        """
        # Empty article text
        article_empty = Article(title="Empty", text="", date="2023-09-23")
        self.assertEqual(
            self.content_aware_service.split_into_chunks(article_empty), []
        )
        self.assertEqual(self.lang_chain_service.split_into_chunks(article_empty), [])

        # Article text shorter than the specified chunk size
        short_text = "Short text."
        article_short = Article(title="Short", text=short_text, date="2023-09-23")
        self.assertEqual(
            self.lang_chain_service.split_into_chunks(article_short), [short_text]
        )

        # Article text with special characters or non-standard formatting
        special_text = "This is a text with special characters: @#$%^&*()_+{}|:<>?~"
        article_special = Article(title="Special", text=special_text, date="2023-09-23")
        self.assertIn(
            special_text, self.content_aware_service.split_into_chunks(article_special)
        )
        self.assertIn(
            special_text, self.lang_chain_service.split_into_chunks(article_special)
        )

    def test_chunk_size_and_overlap(self):
        """
        Test chunk sizes and overlaps for the LangChainChunkingService.

        This test ensures that the LangChainChunkingService respects the specified
        chunk size and overlap when splitting articles into chunks.
        """
        long_text = "A" * 150  # 150 characters
        article = Article(title="Long", text=long_text, date="2023-09-23")
        chunks = self.lang_chain_service.split_into_chunks(article)

        # Check chunk sizes and overlap
        self.assertEqual(len(chunks[0]), 100)
        self.assertEqual(len(chunks[1]), 70)
        self.assertEqual(chunks[0][-20:], chunks[1][:20])  # Check overlap

    def test_interaction_with_article_class(self):
        """
        Test the interaction of the chunking services with the Article class.

        This test ensures that the chunking services can handle real
        Article instances and not just mock data.
        """
        article = Article(
            title="Test",
            text="This is a sample article. It has multiple sentences.",
            date="2023-09-23",
        )
        self.assertTrue(
            isinstance(self.content_aware_service.split_into_chunks(article), list)
        )
        self.assertTrue(
            isinstance(self.lang_chain_service.split_into_chunks(article), list)
        )


if __name__ == "__main__":
    unittest.main()
