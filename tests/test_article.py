"""
This module contains the unit tests for the Article class
"""

import unittest

# pylint: disable=import-error
from dotenv import load_dotenv
from src.crawlers.data_structures.article import Article, ArticleType

# Load environment variables
load_dotenv()


class TestArticle(unittest.TestCase):
    """
    This class contains the unit tests for the Article class.
    """

    def setUp(self):
        """
        Set up the test environment by creating an instance of the Article class.
        """
        self.article = Article(
            title="OpenAI Launches GPT-5",
            text="OpenAI has released its latest foundation model, GPT-5.",
            date="2023-10-21",
        )

    def test_article_initialization(self):
        """
        Test the initialization of the Article class.
        """
        self.assertEqual(self.article.title, "OpenAI Launches GPT-5")
        # pylint: disable=line-too-long
        self.assertEqual(
            self.article.text, "OpenAI has released its latest foundation model, GPT-5."
        )
        self.assertEqual(self.article.date, "2023-10-21")

    def test_article_type(self):
        """
        Test the article_type attribute of the Article class.
        """
        self.assertEqual(self.article.article_type, ArticleType.FOUNDATION_MODEL)

    def test_get_summary(self):
        """
        Test the get_summary method of the Article class.
        """
        summary = self.article.get_summary()
        self.assertIsInstance(summary, str)
        self.assertTrue(len(summary.split("\n")) <= 5)

    def test_get_relevance(self):
        """
        Test the get_relevance method of the Article class.
        """
        relevance = self.article.get_relevance()
        self.assertIsInstance(relevance, int)
        self.assertTrue(0 <= relevance <= 100)


if __name__ == "__main__":
    unittest.main()
