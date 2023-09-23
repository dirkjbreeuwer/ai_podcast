"""
Unit tests for the ApifyCrawlerOutputTransformer class.

This module contains tests that validate the functionality of the
ApifyCrawlerOutputTransformer class, ensuring that it correctly transforms
the raw output from Apify's scrape into the standardized Article data structure.

Classes:
    TestApifyCrawlerOutputTransformer: Contains tests for the ApifyCrawlerOutputTransformer class.

Usage:
    pytest path_to_this_module
"""

import unittest
from src.crawlers.transformers.apify_transformer import ApifyCrawlerOutputTransformer
from src.crawlers.data_structures.article import Article


class TestApifyCrawlerOutputTransformer(unittest.TestCase):
    """Tests for the ApifyCrawlerOutputTransformer class."""

    def setUp(self):
        """Initialize the transformer and sample data for testing."""
        self.sample_data = {
            "url": "https://www.wired.com/story/ai-civil-rights-narratives-robots/",
            "title": "Do Not Fear the Robot Uprising. Join It",
            "date": "2023-09-07T13:00:00.000Z",
            "text": "This is a long string ot text about robots.",
        }
        self.transformer = ApifyCrawlerOutputTransformer(self.sample_data)

    def test_transform(self):
        """Test the transformation of sample data to the Article format."""
        article = self.transformer.transform(self.sample_data)
        self.assertIsInstance(article, Article)
        self.assertEqual(article.title, "Do Not Fear the Robot Uprising. Join It")
        self.assertEqual(article.text, "This is a long string ot text about robots.")
        self.assertEqual(article.date, "2023-09-07T13:00:00.000Z")
        self.assertEqual(
            article.url,
            "https://www.wired.com/story/ai-civil-rights-narratives-robots/",
        )


if __name__ == "__main__":
    unittest.main()
