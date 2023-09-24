"""
Tests for the ArticleWorkflow class.

This module contains unit tests for the ArticleWorkflow class, ensuring the correct
workflow of crawling, storing, processing, and indexing articles. The tests use a SQLite
database for isolation, and some tests that make actual API calls are skipped by default.

Run this module directly to execute all tests: `pytest tests/test_article_workflow.py`
"""
import unittest
import os
from src.workflow.article_workflow import ArticleWorkflow


class TestArticleWorkflow(unittest.TestCase):
    """
    Unit test for testing the ArticleWorkflow class.
    """

    def setUp(self):
        """
        Set up the test environment. This method is called before every test function.
        """
        # Initialize the ArticleWorkflow with a dummy dataset_id and SQLite database stored on disk
        self.db_path = "test_db.sqlite3"
        self.workflow = ArticleWorkflow(
            dataset_id="dummy_dataset", db_path=self.db_path
        )

        # Only crawl and store articles if the database does not exist
        if not os.path.exists(self.db_path):
            sample_urls = [
                "https://techcrunch.com/category/artificial-intelligence/",
                "https://www.wired.com/tag/artificial-intelligence/",
            ]
            self.workflow.crawl_and_store_articles(sample_urls)

    def tearDown(self):
        """
        Clean up after tests. This method is called after every test function.
        """
        # Do not remove the SQLite database file after the test
        # If you want to clean up occasionally, you can do it manually
        os.remove(self.db_path)
        # pass

    @unittest.skip("This test makes an actual API call. Remove if you want to run it.")
    def test_crawl_and_store_articles(self):
        """
        Test the crawl_and_store_articles method of the ArticleWorkflow class.
        """
        # Define a list of sample URLs for testing
        sample_urls = [
            "https://techcrunch.com/category/artificial-intelligence/",
            "https://www.wired.com/tag/artificial-intelligence/",
        ]

        # Call the crawl_and_store_articles method with the sample URLs
        num_articles_stored = self.workflow.crawl_and_store_articles(sample_urls)

        # Check if the number of articles stored matches the number of URLs provided
        self.assertGreaterEqual(num_articles_stored, len(sample_urls))

        # Further checks can be added to validate the content of the stored articles,
        # such as checking if the title, text, and other attributes are correctly stored.

    def test_process_and_index_articles(self):
        """
        Test the process_and_index_articles method of the ArticleWorkflow class.
        """
        # Process and index a limited number of stored articles (e.g., 5 articles)
        self.workflow.process_and_index_articles(max_articles=5)

        # Validate that the articles have been correctly processed and indexed
        # For this, you can use a sample query vector and perform a similarity search
        sample_query = "GPT4"

        # query_vector = self.workflow.faiss_store.convert_query_to_vector(sample_query)
        search_results = self.workflow.faiss_store.similarity_search(sample_query, k=1)

        # Check if we get at least one result, indicating that the articles have been indexed
        self.assertGreaterEqual(len(search_results), 1)

        # Further checks can be added to validate the content of the indexed articles,
        # such as checking the metadata or the similarity scores of the results.


if __name__ == "__main__":
    unittest.main()
