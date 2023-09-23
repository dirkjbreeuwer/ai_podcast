"""
Unit tests for the SQLiteManager class.

This module contains unit tests that validate the functionality of the SQLiteManager class,
ensuring that CRUD operations and other database interactions work as expected.

Usage:
    python -m unittest path_to_this_module

"""

import unittest
from src.crawlers.data_structures.article import Article
from src.storage.sqlite_manager import SQLiteManager


class TestSQLiteManager(unittest.TestCase):
    """
    Unit Test Suite for SQLiteManager.

    This class contains tests that validate the CRUD operations and other database interactions
    implemented in the SQLiteManager class.
    """

    def setUp(self):
        """
        Set up the testing environment.

        This method initializes a new SQLite database in memory and creates the articles table
        for testing purposes before each test case.
        """
        self.db_manager = SQLiteManager(":memory:")
        # Create the articles table for testing
        self.db_manager.cursor.execute(
            """
            CREATE TABLE articles (
                id INTEGER PRIMARY KEY,
                url TEXT,
                title TEXT NOT NULL,
                text TEXT NOT NULL,
                date DATE NOT NULL,
                loaded_domain TEXT,
                author TEXT,
                description TEXT,
                keywords TEXT,
                lang TEXT,
                tags TEXT,
                image TEXT,
                is_vectorized INTEGER DEFAULT 0
            )
        """
        )
        self.db_manager.conn.commit()

    def tearDown(self):
        """
        Tear down the testing environment.

        This method closes the database connection after each test case.
        """
        self.db_manager.close()

    def test_save_and_find_by_id(self):
        """
        Test the save and find_by_id methods.

        This test validates that an article can be saved to the database and then retrieved
        by its ID. It also checks the default value of the is_vectorized attribute.
        """
        article = Article(title="Test Title", text="Test Text", date="2023-09-23")
        self.db_manager.save(article)
        retrieved_article = self.db_manager.find_by_id(1)
        self.assertEqual(retrieved_article.title, "Test Title")
        self.assertEqual(retrieved_article.text, "Test Text")
        self.assertEqual(retrieved_article.is_vectorized, 0)  # Check the default value

    def test_update(self):
        """
        Test the update method.

        This test validates that an article's attributes can be updated in the database.
        It also checks the updated value of the is_vectorized attribute.
        """
        article = Article(title="Test Title", text="Test Text", date="2023-09-23")
        self.db_manager.save(article)
        article.title = "Updated Title"
        article.article_id = "1"  # Ensure this is the correct way to set the article ID
        article.is_vectorized = 1  # Set the is_vectorized attribute
        self.db_manager.update(article)
        retrieved_article = self.db_manager.find_by_id(1)
        self.assertEqual(retrieved_article.title, "Updated Title")
        self.assertEqual(retrieved_article.is_vectorized, 1)  # Check the updated value

    def test_delete(self):
        """
        Test the delete method.

        This test validates that an article can be deleted from the database using its ID.
        """
        article = Article(title="Test Title", text="Test Text", date="2023-09-23")
        self.db_manager.save(article)
        self.db_manager.delete(1)
        retrieved_article = self.db_manager.find_by_id(1)
        self.assertIsNone(retrieved_article)

    def test_find_all(self):
        """
        Test the find_all method.

        This test validates that multiple articles can be saved and then retrieved using
        the find_all method. It also checks the default value of the is_vectorized attribute
        for each saved article.
        """
        article1 = Article(title="Test Title 1", text="Test Text 1", date="2023-09-23")
        article2 = Article(title="Test Title 2", text="Test Text 2", date="2023-09-24")
        self.db_manager.save(article1)
        self.db_manager.save(article2)
        articles = self.db_manager.find_all()
        self.assertEqual(len(articles), 2)
        self.assertEqual(articles[0].title, "Test Title 1")
        self.assertEqual(articles[1].title, "Test Title 2")
        self.assertEqual(articles[0].is_vectorized, 0)  # First article
        self.assertEqual(articles[1].is_vectorized, 0)  # Second article


if __name__ == "__main__":
    unittest.main()
