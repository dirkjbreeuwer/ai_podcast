"""
Handles the workflow of crawling, storing, processing, and searching articles.
Includes components for crawling, database management, chunking, embedding, and indexing.

Available methods:
- initialize_database: Set up the SQLite database schema.
- crawl_and_store_articles: Fetch and store articles from online sources.
- process_and_index_articles: Chunk articles, generate embeddings, and index them.
- search_articles: Search for relevant articles based on a query.
"""
from typing import Optional

from src.crawlers.apify_crawler import ApifyArticleCrawler
from src.crawlers.transformers.apify_transformer import ApifyCrawlerOutputTransformer
from src.storage.databases.sqlite_manager import SQLiteManager
from src.search_and_retrieval.preprocessing_services.chunk_service import (
    LangChainChunkingService,
)
from src.search_and_retrieval.preprocessing_services.embedding_service import (
    HuggingFaceBGEEmbeddingService,
    HuggingFaceToLangchainEmbeddingAdapter,
)
from src.search_and_retrieval.faiss_vector_store import FAISSStore


class ArticleWorkflow:
    """
    Manages the end-to-end workflow for articles, from crawling to searching.

    - `initialize_database`: Set up the SQLite database.
    - `crawl_and_store_articles`: Fetch and store articles.
    - `process_and_index_articles`: Process and index articles for search.
    - `search_articles`: Search for articles based on a query.
    """

    # pylint: disable=too-many-instance-attributes
    def __init__(self, dataset_id, db_path):
        """
        Initialize the workflow with necessary configurations.

        Args:
            dataset_id (str): The dataset ID for the ApifyCrawler.
            db_path (str): Path to the SQLite database.
        """
        self.dataset_id = dataset_id
        self.db_path = db_path
        self.crawler = ApifyArticleCrawler("ApifyArticleCrawler", {})
        self.db_manager = SQLiteManager(db_path=self.db_path)
        self.chunk_service = LangChainChunkingService(chunk_size=300, chunk_overlap=20)
        self.huggingface_service = HuggingFaceBGEEmbeddingService()
        self.adapter = HuggingFaceToLangchainEmbeddingAdapter(self.huggingface_service)
        self.faiss_store = FAISSStore(self.adapter)

        # Initialize the database
        self.initialize_database()

    def initialize_database(self):
        """
        Initialize the SQLite database schema.
        Create necessary tables if they don't exist.
        """
        self.db_manager.initialize_schema()

    def crawl_and_store_articles(self, urls):
        """
        Fetch articles from online sources, standardize them, and store them in the SQLite database.

        Args:
            urls (List[str]): A list of URLs to crawl.

        Returns:
            int: The number of articles successfully crawled and stored.
        """
        # Step 1: Crawl articles using the ApifyArticleCrawler
        crawled_data = self.crawler.batch_fetch(urls)

        # Step 2: Transform crawled data into standardized Article format
        articles = []
        for data in crawled_data:
            transformer = ApifyCrawlerOutputTransformer(data)
            article = transformer.transform(data)
            articles.append(article)

        # Step 3: Store the standardized articles in the SQLite database
        for article in articles:
            self.db_manager.save(article)

        return len(articles)

    def process_and_index_articles(self, max_articles: Optional[int] = None):
        """
        Load articles from the SQLite database, chunk their text, generate embeddings,
        and index the embeddings for efficient similarity search.
        """
        # Step 1: Load articles from the SQLite database
        articles = self.db_manager.find_all(
            limit=max_articles
        )  # Modify the find_all method to accept a limit

        # Step 2: Chunk articles into smaller textual chunks
        all_chunks = []
        metadata_list = []  # List to store metadata for each chunk
        for article in articles:
            # Split each article into chunks
            chunks = self.chunk_service.split_into_chunks(article)
            all_chunks.extend(chunks)

            # Generate metadata for each chunk
            for chunk in chunks:
                metadata = {
                    "title": article.title,
                    "url": article.url,
                    "date": article.date,
                    "id": article.article_id,
                }
                metadata_list.append(metadata)

        # Step 3: Generate embeddings for the chunks
        embeddings = [
            self.faiss_store.embeddings.embed_query(chunk) for chunk in all_chunks
        ]

        # Step 4: Index the embeddings into the FAISSStore
        self.faiss_store.index_documents(all_chunks, embeddings, metadata_list)

    def search_articles(self, query):
        """
        Search for articles based on a query.

        Args:
            query (str): The search query.

        Returns:
            List[Article]: A list of relevant articles.
        """
