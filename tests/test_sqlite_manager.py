"""
Unit tests for the SQLiteManager class.

This module contains unit tests that validate the functionality of the SQLiteManager class,
ensuring that CRUD operations and other database interactions work as expected.

Usage:
    pytest path_to_this_module

"""

import unittest
import os
from src.crawlers.data_structures.article import Article
from src.storage.databases.sqlite_manager import SQLiteManager


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
        self.db_manager.initialize_schema()

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

    def test_load_database_from_disk(self):
        """
        Test the ability to load a database from disk after it has been closed.
        """
        # Step 1: Create a SQLite database on disk
        db_path = "test_db.sqlite3"
        db_manager = SQLiteManager(db_path)
        db_manager.initialize_schema()  # Initialize the database

        # Step 2: Add some data to it
        article = Article(
            title="Disk Test Title", text="Disk Test Text", date="2023-09-23"
        )
        db_manager.save(article)

        # Step 3: Close the database
        db_manager.close()
        del db_manager  # Ensure the original manager is no longer in use

        # Step 4: Reopen the database from the disk location
        reopened_db_manager = SQLiteManager(db_path)

        # Step 5: Verify that the data added in step 2 is still present
        retrieved_article = reopened_db_manager.find_by_id(1)
        self.assertEqual(retrieved_article.title, "Disk Test Title")
        self.assertEqual(retrieved_article.text, "Disk Test Text")

        # Cleanup: Remove the test database file
        os.remove(db_path)


if __name__ == "__main__":
    unittest.main()
