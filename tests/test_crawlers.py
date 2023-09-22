"""
Unit test for testing the ApifyArticleCrawler class.
"""
import unittest

# pylint: disable=fixme
### TODO: Mock the ApifyArticleCrawler class to avoid making actual API calls

# Assuming the Crawler and ApifyArticleCrawler classes are in a module named 'crawlers'
from src.crawlers.apify_crawler import ApifyArticleCrawler


class TestApifyArticleCrawler(unittest.TestCase):
    """
    Unit test for testing the ApifyArticleCrawler class.
    """

    def setUp(self):
        """
        Set up the test environment. This method is called before every test function.
        """
        # Initialize the ApifyArticleCrawler with a dummy name, config, and API key
        self.crawler = ApifyArticleCrawler("ApifyArticleCrawler", {})

    def test_fetch(self):
        """
        Test the fetch method of the ApifyArticleCrawler class.
        """
        # Test the fetch method with a sample URL
        url = "https://techcrunch.com/category/artificial-intelligence/"
        result = self.crawler.fetch(url)
        # Check if the result is a dictionary and contains expected keys
        self.assertIsInstance(result, dict)
        self.assertIn("title", result)
        self.assertIn("text", result)

    def test_batch_fetch(self):
        """
        Test the batch_fetch method of the ApifyArticleCrawler class.
        """
        # Test the batch_fetch method with a list of sample URLs
        urls = [
            "https://techcrunch.com/category/artificial-intelligence/",
            "https://www.wired.com/tag/artificial-intelligence/",
        ]
        results = self.crawler.batch_fetch(urls)
        # Check if the results is a list and each item is a dictionary with expected keys
        self.assertIsInstance(results, list)
        for result in results:
            self.assertIsInstance(result, dict)
            self.assertIn("title", result)
            self.assertIn("text", result)

    def test_get_status(self):
        """
        Test the get_status method of the ApifyArticleCrawler class.
        """
        # Test the get_status method
        status = self.crawler.get_status()
        # Check if the status is a string and contains the crawler's name
        self.assertIsInstance(status, str)
        self.assertIn("ApifyArticleCrawler", status)

    def test_set_options(self):
        """
        Test the set_options method of the ApifyArticleCrawler class.
        """
        # Test the set_options method
        options = {"option1": "value1", "option2": "value2"}
        self.crawler.set_options(options)
        # Check if the options were updated in the crawler's config
        self.assertEqual(self.crawler.config["option1"], "value1")
        self.assertEqual(self.crawler.config["option2"], "value2")


if __name__ == "__main__":
    unittest.main()
