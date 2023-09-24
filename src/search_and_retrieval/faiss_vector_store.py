"""
FAISS Store Module

Provides an implementation of the VectorStore using the FAISS library via the LangChain wrapper.
Supports indexing of article chunks with metadata, efficient similarity searches, and persistence
of the FAISS index.

Classes:
    - FAISSStore: Implementation using FAISS via LangChain.

Dependencies:
    - Requires `faiss-cpu` package and `langchain.vectorstores.faiss`.

Note:
    Relies on the `vector_store.py` for the VectorStore abstract base class.
"""

import asyncio
from typing import List, Tuple, Dict, Optional

# pylint: disable=import-error
from langchain.vectorstores.faiss import FAISS
from langchain.schema.embeddings import Embeddings
from .vector_store import VectorStore
from .search_engine import SearchEngine


class FAISSStore(VectorStore, SearchEngine):
    """FAISS implementation of the VectorStore using langchain wrapper."""

    def __init__(self, embeddings: Embeddings):
        self.embeddings = embeddings
        self.index = None  # This will hold our FAISS index instance

    def index_documents(
        self,
        texts: List[str],
        embeddings: List[List[float]],
        metadata_list: List[Dict[str, str]],
    ) -> None:
        text_embeddings = list(zip(texts, embeddings))
        self.index = FAISS.from_embeddings(
            text_embeddings, self.embeddings, metadatas=metadata_list
        )

    def similarity_search(
        self, query_vector: List[float], k: Optional[int] = 10
    ) -> List[Tuple[int, float, Dict[str, str]]]:
        # Perform similarity search using the query vector
        # The method returns both the document IDs and their similarity scores
        # Run the coroutine synchronously

        # Using the updated method to get both doc_ids and scores
        # pylint: disable=line-too-long
        results_with_scores = asyncio.run(
            self.index.asimilarity_search_with_relevance_scores(query_vector, k)
        )

        # Extract doc_ids, scores, and metadata directly from results_with_scores
        doc_ids = [doc.metadata["id"] for doc, _ in results_with_scores]
        scores = [score[1] for score in results_with_scores]
        metadata_list = [doc.metadata for doc, _ in results_with_scores]

        # Combine doc_ids, scores, and metadata into a single list of results
        results = list(zip(doc_ids, scores, metadata_list))

        return results

    def save_index(self, file_path: str) -> None:
        # Save the FAISS index to the specified file path
        self.index.save_local(file_path)

    def load_index(self, file_path: str) -> None:
        # Load the FAISS index from the specified file path
        self.index = FAISS.load_local(file_path)

    def convert_query_to_vector(self, query: str) -> List[float]:
        return self.embeddings.embed_query(query)

    def execute_similarity_search(
        self, query_vector: List[float]
    ) -> List[Tuple[int, float]]:
        return self.similarity_search(query_vector)

    def execute_advanced_search(
        self, query_vector: List[float], metadata: dict
    ) -> List[Tuple[int, float]]:
        # Implement advanced search combining vector similarity with metadata filtering
        pass
