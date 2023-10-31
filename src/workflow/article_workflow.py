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

# pylint: disable=import-error
from profilehooks import profile


from src.crawlers.data_structures.article import ArticleType
from src.crawlers.apify_crawler import ApifyArticleCrawler
from src.crawlers.transformers.apify_article_transformer import (
    ApifyArticleCrawlerOutputTransformer,
)
from src.storage.databases.article_sqlite_manager import ArticleSQLiteManager
from src.search_and_retrieval.chroma_vector_store import ChromaVectorStore
from src.search_and_retrieval.preprocessing_services.chunk_service import (
    LangChainChunkingService,
)
from src.script_generation.script_generator import generate_script
from src.utils.logging_config import get_logger


class ArticleWorkflow:
    """
    Manages the end-to-end workflow for articles, from crawling to searching.

    - `initialize_database`: Set up the SQLite database.
    - `crawl_and_store_articles`: Fetch and store articles.
    - `process_and_index_articles`: Process and index articles for search.
    - `search_articles`: Search for articles based on a query.
    """

    # pylint: disable=too-many-instance-attributes
    def __init__(self, relational_db_path):
        """
        Initialize the workflow with necessary configurations.

        Args:
            db_path (str): Path to the SQLite database.
        """
        self.logger = get_logger("my_logger")
        self.db_manager = ArticleSQLiteManager(db_path=relational_db_path)
        self.crawler = ApifyArticleCrawler("ApifyArticleCrawler", {})
        self.chunk_service = LangChainChunkingService(chunk_size=500, chunk_overlap=100)
        # Initialize the Chroma store with ephemeral storage
        self.vector_store = ChromaVectorStore(client_type="ephemeral")
        # Create and use a collection in Chroma for articles
        collection_names = [
            collection.name for collection in self.vector_store.list_collections()
        ]
        if "article_collection" not in collection_names:
            self.vector_store.create_collection(
                name="article_collection", metadata={"hnsw:space": "cosine"}
            )
        self.vector_store.use_collection(name="article_collection")

        # Create and use a collection in Chroma for article titles
        if "title_collection" not in collection_names:
            self.vector_store.create_collection(
                name="title_collection", metadata={"hnsw:space": "cosine"}
            )
        self.vector_store.use_collection(name="title_collection")
        # Initialize the database
        self.initialize_database()

    def initialize_database(self):
        """
        Initialize the SQLite database schema.
        Create necessary tables if they don't exist.
        """
        self.logger.info("Initializing the SQLite database schema.")
        self.db_manager.initialize_schema()

    @profile(filename="./profile_results.prof", immediate=True)
    def crawl_and_store_articles(self, urls):
        """
        Fetch articles from online sources, standardize them, and store them in the SQLite database.

        Args:
            urls (List[str]): A list of URLs to crawl.

        Returns:
            int: The number of articles successfully crawled and stored.
        """
        # Step 1: Crawl articles using the ApifyArticleCrawler
        self.logger.info(
            "Starting the crawl_and_store_articles method with URLs: %s", urls
        )
        crawled_data = self.crawler.batch_fetch(urls)
        self.logger.info(
            "Number of articles successfully crawled: %d", len(crawled_data)
        )

        # Step 2: Transform crawled data into standardized Article format
        self.logger.info("Transforming crawled data into standardized Article format")
        articles = []
        for data in crawled_data:
            self.logger.info("Transforming data: %s", data)
            transformer = ApifyArticleCrawlerOutputTransformer(data)
            article = transformer.transform(data)
            self.logger.info("Transformed article: %s", article)
            articles.append(article)
        self.logger.info(
            "Number of articles successfully transformed: %d", len(articles)
        )

        # Step 3: Store the standardized articles in the SQLite database
        self.logger.info("Storing the standardized articles in the SQLite database")
        for article in articles:
            article.get_type()
            self.logger.info("Storing article: %s", article)
            self.db_manager.save(article)

        self.logger.info(
            "Number of articles successfully crawled and stored: %d", len(articles)
        )
        return len(articles)

    # pylint: disable=fixme
    # TODO: Load existing index, and only process articles that have not been indexed
    def process_and_index_articles(self, max_articles: Optional[int] = None):
        """
        Load articles from the SQLite database, chunk their text
        and index the chunks for efficient similarity search.
        """
        self.logger.info(
            "Starting the process_and_index_articles method with max_articles: %s",
            max_articles,
        )
        # Step 1: Load articles from the SQLite database
        articles = self.db_manager.find_all(
            limit=max_articles
        )  # Modify the find_all method to accept a limit

        # Step 2: Chunk articles into smaller textual chunks
        all_chunks = []
        metadata_list = []  # List to store metadata for each chunk
        total_word_count = 0  # Initialize total word count

        for article in articles:
            # Split each article into chunks
            chunks = self.chunk_service.split_into_chunks(article)
            all_chunks.extend(chunks)

            # Calculate total word count for all chunks
            for chunk in chunks:
                total_word_count += len(chunk.split())

            # Generate metadata for each chunk
            for chunk in chunks:
                metadata = {
                    "title": article.title,
                    "url": article.url,
                    "date": article.date,
                    "id": article.article_id,
                }
                metadata_list.append(metadata)

        # Calculate average chunk length in words
        average_chunk_length = total_word_count / len(all_chunks) if all_chunks else 0

        # Print or return the debugging information
        self.logger.info("Average chunk length: %.2f words", average_chunk_length)

        # Step 3: Add chunks to the Chroma store
        self.vector_store.use_collection(name="article_collection")
        self.vector_store.add_documents(texts=all_chunks, metadata_list=metadata_list)

        # Add titles to the Chroma store
        titles = [article.title for article in articles]
        title_metadata_list = [
            {
                "title": article.title,
                "url": article.url,
                "date": article.date,
                "id": article.article_id,
                "text": article.text,
            }
            for article in articles
        ]

        self.vector_store.use_collection(name="title_collection")
        self.vector_store.add_documents(texts=titles, metadata_list=title_metadata_list)

    def search_articles(self, query):
        """
        Search for articles based on a query.

        Args:
            query (str): The search query.

        Returns:
            List[Article]: A list of relevant articles.
        """
        self.logger.info("Starting the search_articles method with query: %s", query)
        # First, search the title collection
        self.vector_store.use_collection(name="title_collection")
        title_results = self.vector_store.query_collection(query)
        return title_results

    @profile(filename="./profile_results.prof", immediate=True)
    def summarize_articles(self, article_type_not_other=True, progress_callback=None):
        # pylint: disable=line-too-long
        """
        Summarize articles in the database.
        If only_not_other is True, only summarizes articles where
        article_type is not ArticleType.OTHER
        Saves summary as a text file in the same directory as the article
        (appends each new summary to the file)

        Args:
            article_type_not_other (bool): If True, only summarize articles where article_type is not ArticleType.OTHER.
            progress_callback (Optional[Callable[[int, int], None]]): A callback function to update progress.
        """
        self.logger.info("Starting the summarize_articles method")
        # Step 1: Load articles from the SQLite database
        articles = self.db_manager.find_all(sort_by=[("article_type", "ASC")])
        # Only summarize articles that have not yet been summarized
        articles = [article for article in articles if article.summary is None]

        # Count the number of articles to be summarized
        num_articles_to_summarize = len(articles)
        if article_type_not_other:
            num_articles_to_summarize = len(
                [
                    article
                    for article in articles
                    if article.article_type != ArticleType.OTHER
                ]
            )

        # Step 2: Summarize articles
        for i, article in enumerate(articles):
            if article_type_not_other and article.article_type == ArticleType.OTHER:
                continue
            article.get_summary()
            self.db_manager.update(article)

            if progress_callback is not None:
                progress_callback(
                    i + 1, num_articles_to_summarize
                )  # Call the progress callback function

    def get_summarized_articles(self):
        """
        Get summarized articles from the database
        """
        self.logger.info("Starting the get_summarized_articles method")
        # Step 1: Load articles from the SQLite database
        articles = self.db_manager.find_articles_by_type_relevance(
            excluded_type=ArticleType.OTHER
        )
        # Only load articles that have not yet been summarized
        articles = [article for article in articles if article.summary is not None]
        return articles

    def write_podcast_script(self):
        """
        Read summaries from database and write podcast script
        """
        self.logger.info("Starting the write_podcast_script method")
        # Step 1: Load articles from the SQLite database
        articles = self.db_manager.find_articles_by_type_relevance(
            excluded_type=ArticleType.OTHER
        )
        # Only load articles that have not yet been summarized
        articles = [article for article in articles if article.summary is not None]
        # Prepare summaries for script generation
        # For every article get the title, type.value and summary, separated by a new line
        # pylint: disable=line-too-long
        summaries = [
            f"Title: {article.title}\nType: {article.article_type.name}\nSummary:\n{article.summary}\n\n"
            for article in articles
        ]
        # Step 2: Write podcast script
        script = generate_script(summaries)
        # Save script to text file
        with open("./data/script.txt", "w", encoding="utf-8") as script_file:
            script_file.writelines(script)
