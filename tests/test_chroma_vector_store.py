"""
Unit tests for the ChromaVectorStore class.
"""

import unittest
import tempfile
import os
import shutil

from src.search_and_retrieval.chroma_vector_store import ChromaVectorStore


class TestChromaVectorStore(unittest.TestCase):
    """Test cases for the ChromaVectorStore class."""

    def test_ephemeral_client_initialization(self):
        """Test initialization with an ephemeral client."""
        store = ChromaVectorStore(client_type="ephemeral")
        heartbeat = store.client.heartbeat()
        self.assertIsNotNone(heartbeat, "Ephemeral client heartbeat failed.")

    def test_persistent_client_initialization(self):
        """Test initialization with a persistent client."""
        with tempfile.TemporaryDirectory() as temp_dir:
            store = ChromaVectorStore(client_type="persistent", path=temp_dir)
            heartbeat = store.client.heartbeat()
            self.assertIsNotNone(heartbeat, "Persistent client heartbeat failed.")
            self.assertTrue(
                os.listdir(temp_dir), "Persistent storage directory is empty."
            )

    def test_successful_collection_creation(self):
        """Test successful creation of a collection."""
        store = ChromaVectorStore(client_type="ephemeral")
        collection_name = "test_collection"
        store.create_collection(name=collection_name)
        store.use_collection(name=collection_name)
        self.assertEqual(
            store.current_collection.name, collection_name, "Collection name mismatch."
        )
        store.delete_collection(name=collection_name)

    def test_duplicate_collection_creation(self):
        """Test error handling for duplicate collection creation."""
        store = ChromaVectorStore(client_type="ephemeral")
        collection_name = "test_collection"
        store.create_collection(name=collection_name)
        with self.assertRaises(ValueError):
            store.create_collection(name=collection_name)
        store.delete_collection(name=collection_name)

    def test_collection_metadata_association(self):
        """Test metadata association with a collection."""
        store = ChromaVectorStore(client_type="ephemeral")
        collection_name = "test_collection"
        metadata = {"key": "value"}
        store.create_collection(name=collection_name, metadata=metadata)
        store.use_collection(name=collection_name)
        self.assertEqual(
            store.current_collection.metadata, metadata, "Collection metadata mismatch."
        )
        store.delete_collection(name=collection_name)

    def test_successful_document_addition(self):
        """Test successful addition of documents to a collection."""
        store = ChromaVectorStore(client_type="ephemeral")
        collection_name = "test_collection"
        store.create_collection(name=collection_name)
        store.use_collection(name=collection_name)
        texts = ["doc1", "doc2"]
        store.add_documents(texts=texts)
        self.assertEqual(store.current_collection.count(), 2)
        store.delete_collection(name=collection_name)

    def test_simple_query_collection(self):
        """Test a simple query against a collection."""
        store = ChromaVectorStore(client_type="ephemeral")
        collection_name = "simple_query_test"
        store.create_collection(name=collection_name)
        store.use_collection(name=collection_name)
        texts = ["Apple", "Samsung", "Nokia", "Sony", "LG"]
        store.add_documents(texts=texts)
        results = store.query_collection(
            query_texts=["phone manufacturers"], n_results=5
        )
        self.assertTrue(results["ids"], "Query did not return any results.")
        store.delete_collection(name=collection_name)

    def test_query_with_where_clause(self):
        """Test a query with a 'where' clause."""
        store = ChromaVectorStore(client_type="ephemeral")
        collection_name = "where_query_test"
        store.create_collection(name=collection_name)
        store.use_collection(name=collection_name)
        texts = ["Apple", "Samsung", "Nokia", "Sony", "LG"]
        metadatas = [{"GICS Sector": "Information Technology"} for _ in texts]
        store.add_documents(texts=texts, metadata_list=metadatas)
        results = store.query_collection(
            query_texts=["phone manufacturers"],
            n_results=5,
            where={"GICS Sector": "Information Technology"},
        )
        self.assertTrue(
            results["ids"], "Query with where clause did not return any results."
        )
        store.delete_collection(name=collection_name)

    def test_query_with_complex_where_clause(self):
        """Test a query with a complex 'where' clause."""
        store = ChromaVectorStore(client_type="ephemeral")
        collection_name = "complex_where_query_test"
        store.create_collection(name=collection_name)
        store.use_collection(name=collection_name)
        texts = ["Apple", "Samsung", "Nokia", "Sony", "LG"]
        metadatas = [
            {"GICS Sector": "Information Technology", "date_founded": 2000}
            for _ in texts
        ]
        store.add_documents(texts=texts, metadata_list=metadatas)
        where_clause = {
            "$and": [
                {"GICS Sector": {"$eq": "Information Technology"}},
                {"date_founded": {"$gte": 1990}},
            ]
        }
        results = store.query_collection(
            query_texts=["phone manufacturers"], n_results=5, where=where_clause
        )
        # pylint: disable=line-too-long
        self.assertTrue(
            results["ids"],
            "Query with complex where clause did not return any results.",
        )
        store.delete_collection(name=collection_name)

    def test_save_index(self):
        """Test saving the Chroma index to a file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            store = ChromaVectorStore(client_type="persistent", path=temp_dir)
            collection_name = "save_index_test"
            store.create_collection(name=collection_name)
            store.use_collection(name=collection_name)
            texts = ["doc1", "doc2"]
            store.add_documents(texts=texts)

            # Save the index
            store.save_index(file_path=temp_dir)

            # Check if the directory is not empty (indicating the index was saved)
            self.assertTrue(os.listdir(temp_dir), "Index was not saved correctly.")

            # Delete the index files from the disk after testing
            shutil.rmtree(temp_dir)

    def test_load_index(self):
        """Test loading the Chroma index from a file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # First, create and save an index
            store = ChromaVectorStore(client_type="persistent", path=temp_dir)
            collection_name = "load_index_test"
            store.create_collection(name=collection_name)
            store.use_collection(name=collection_name)
            texts = ["doc1", "doc2"]
            store.add_documents(texts=texts)
            store.save_index(file_path=temp_dir)

            # Now, create a new store and load the index
            new_store = ChromaVectorStore(client_type="persistent", path=temp_dir)
            new_store.load_index(file_path=temp_dir)

            # Set the current collection to the one you're working with
            new_store.use_collection(name=collection_name)

            # Query the loaded index to check if it was loaded correctly
            results = new_store.query_collection(query_texts=["doc1"], n_results=1)
            self.assertTrue(results["ids"], "Index was not loaded correctly.")

            # Delete the index files from the disk after testing
            shutil.rmtree(temp_dir)


if __name__ == "__main__":
    unittest.main()
