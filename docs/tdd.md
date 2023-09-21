# Technical Design Document for Web-Based Article Crawler and Processor

## 1. Introduction
### 1.1 Purpose:

This document delineates the technical architecture for a web-based system designed to crawl, process, store, search, retrieve, and generate summarizations of articles. The ultimate goal is to convert these summaries into podcast scripts.

### 1.2 Scope:

The solution aims to target news sites, blogs, academic journals, and GitHub repositories. By integrating Language Learning Models (LLMs), the system will deliver optimized content processing, summarization, and scripting functionalities. The design encompasses both backend processing components and considerations for future frontend user interfaces, ensuring scalability and efficient data handling.

### 1.3 Definitions & Acronyms:

* Web Crawlers: Automated scripts programmed to fetch content from the web.
* LLMs (Language Learning Models): Advanced machine learning models primed for natural language processing tasks.
* Vector Embeddings: Mathematical constructs that represent data in a vector space, facilitating similarity-based searches.

## 2. System Overview
### 2.1 System Architecture:

The system is architected as a set of distinct, loosely coupled modules, ensuring modularization, scalability, and maintainability. These modules intercommunicate through defined interfaces, promoting flexibility in the data flow and interactions. Key components include:

* Web Crawlers: Fetch content from designated online sources.
* Data Storage: Store raw and processed data, including embeddings, in a structured manner.
* Language Models (LLMs): Responsible for content processing, summarization, and scripting tasks.
* Search & Retrieval Service: Handle the querying and extraction of stored articles and summaries.
* Podcast Script Generator: Transform summarized content into scripts suitable for podcasts.

### 2.2 Component Summary:

* Web Crawlers: Initially, we'll employ Apify, a scalable web scraping tool. As our needs evolve, we may transition to Scrapy for a more scalable and cost-effective solution. The collected data is directed to the storage system for subsequent processing.

* Data Storage: The storage system will be cloud-based, using solutions such as Amazon S3 for raw data and Amazon RDS or equivalent relational databases for structured, processed data. This setup ensures durability, availability, and efficient data retrieval.

* Language Models (LLMs): These models, sourced from providers like Hugging Face or OpenAI, perform tasks of content processing. They extract data from storage, process it, and then relay the processed content back to the storage module.

* Search & Retrieval Service: A dedicated module to query the stored data. It heavily collaborates with the vector embeddings to derive articles similar to user queries.

* Podcast Script Generator: This module retrieves the summarized content and adapts it into a format that's coherent and optimized for podcast narratives.

## 3.1 Web Crawlers

### 3.1.1 Design:

**Objective**: To fetch articles from the web, extract relevant data, and standardize the outputs into a uniform structure suitable for downstream processing.

#### Data Structures:

- **Article**: 
  A structured representation for holding attributes like URL, title, content, and associated metadata of each scraped article.

#### Classes and Their Roles:

- **Crawler**: 
  The foundational class for all web crawlers to ensure consistency and standardization.
  
- **ApifyArticleCrawler**: 
  Designed for the Apify platform, inheriting from the Crawler class.
  
- **CrawlerOutputTransformer**: 
  Ensures the outputs from diverse crawlers are transformed and standardized into the `Article` data structure.
  
- **ApifyCrawlerOutputTransformer**: 
  Manages unique outputs from Apify, ensuring they are also transformed to fit the `Article` data structure.

### 3.1.2 Implementation:

#### Crawler:

- **Methods**:
  - `fetch()`: Single article fetch based on given criteria.
  - `batch_fetch()`: Collect multiple articles based on a broader set of criteria or a list of URLs.
  - `get_status()`: Get the current status of the crawler, e.g., running, idle, error.

#### ApifyArticleCrawler (inherits from Crawler):

- **Methods**:
  - `set_options()`: Specialized for Apify, to provide additional configurations unique to this platform.

#### CrawlerOutputTransformer:

- **Objective**: 
  Convert various crawler outputs into the standardized `Article` data type.
  
- **Methods**:
  - `transform(raw_data: dict) -> Article`: Converts the raw output of a crawl into the `Article` data type.

#### ApifyCrawlerOutputTransformer (inherits from CrawlerOutputTransformer):

- **Methods**:
  - `transform(raw_data: dict) -> Article`: Specific transformation logic for Apify's outputs to the `Article` data type.

**Transformation Logic for ApifyCrawlerOutputTransformer**:

```python
def transform(self, raw_data: dict) -> Article:
    """
    Convert Apify's raw JSON output to the Article data type.
    """
    article = Article(
        article_id=None,  # This could be auto-incremented or generated during database insertion.
        md5_id=hashlib.md5(raw_data["url"].encode()).hexdigest(),
        url=raw_data["url"],
        title=raw_data["title"],
        content=raw_data["text"],
        domain=raw_data["loadedDomain"],
        date=raw_data["date"],
        author=raw_data["author"],
        description=raw_data["description"],
        keywords=raw_data["keywords"],
        lang=raw_data["lang"],
        tags=raw_data["tags"],
        summary=""  # This will be generated separately
    )
    return article
```

---

## 3.2 Data Storage

### 3.2.1 Relational Database Storage

#### 3.2.1.1 Design

**Objective**: To persist the articles of the `Article` data type transformed by the crawler into a relational database, ensuring their efficient retrieval, update, and relationship management.

- **Article and Metadata Storage**:
  - **Relational Database**: The choice of PostgreSQL is influenced by its robustness in handling structured data and complex relationships, making it an excellent choice for articles, authors, sources, and tags storage.
  - **Flagging Mechanism**: The need for an `is_vectorized` column in the Articles schema stems from the requirement to track which articles have already been processed and stored in ChromaDB.
  - **Schemas**: These are designed to represent the structure and relationships of our primary entities:
    - Articles: Capturing the essence of each article and its processing status.
    - Authors: Representing individual or group authors.
    - Sources: Denoting where the article originated.
    - Tags: Categories or themes associated with an article.
    - Article_Tag and Article_Author: Bridging tables to manage many-to-many relationships.

#### 3.2.1.2 Implementation

- **DatabaseManager Class**: This class provides foundational operations to interact with the relational database, ensuring encapsulation and separation of concerns.

  - `save(article: Article)`: Persists a new article into the database, initializing the `is_vectorized` status as `False`.
  
  - `update(article: Article)`: Updates an existing article's attributes in the database.
  
  - `delete(article_id: int)`: Removes an article based on its ID.
  
  - `find_by_id(article_id: int) -> Article`: Retrieves a specific article based on its ID.
  
  - `find_all() -> List[Article]`: Retrieves all articles from the database.
  
  - `find_by_criteria(criteria: dict) -> List[Article]`: Retrieves articles based on specified criteria (e.g., articles from a specific source or date range).
  
  - `mark_as_vectorized(article_id: int)`: Updates the `is_vectorized` flag to `True` for a given article.
  
  - `is_vectorized(article_id: int) -> bool`: Checks if a given article has been vectorized.
  
  - `batch_save(articles: List[Article])`: Persists multiple articles in a single operation, useful for bulk insertions.

- **PostgreSQLManager Class** (inherits from DatabaseManager): Tailored for PostgreSQL-specific operations, this class ensures that the generic CRUD operations defined in `DatabaseManager` are implemented in a way that's optimized for PostgreSQL.

### 3.2.2 Article Chunking and Embedding

#### 3.2.2.1 Design

To facilitate efficient storage and retrieval from the vector database, articles that have the `is_vectorized` flag set to `False` will be chunked and then embedded.

- **ChunkService Class**:
  - `split_into_chunks(article: Article)`: Splits an article into smaller textual chunks.
- **EmbeddingService Class**:
  - `generate_embedding(text_chunk: str)`: Produces embeddings from textual chunks using LLMs.

#### 3.2.2.2 Implementation

Embeddings are generated for each chunk of articles flagged with `is_vectorized = False` and prepared for storage in the vector database.

### 3.2.3 Vector Database Storage (ChromaDB)

#### 3.2.3.1 Design

Once embeddings are generated, they are stored in a vector database to facilitate efficient similarity search operations.

- **VectorDBManager Class**: Abstraction over the specific vector database operations.
- **ChromaDBManager** (inherits from VectorDBManager): Methods tailored for ChromaDB-specific operations.

#### 3.2.3.2 Implementation

The generated embeddings are stored in ChromaDB, allowing for efficient retrieval based on similarity search.


---
## 3.3 Language Models

### 3.3.1 Design

**Objective**: To enable seamless and consistent interaction with various Language Learning Models (LLMs) for tasks such as summarizing articles or generating scripts.

#### PromptBuilder

- **Purpose**:
  - To create and manage the prompts that are used to invoke the LLMs.
  - Ensuring that prompts are appropriately structured is crucial for obtaining accurate and relevant results from the models.

#### AbstractLLMInvoker

- **Purpose**:
  - Acts as a blueprint for all LLM interactions.
  - It ensures a standardized method set, which allows for flexibility in using different LLMs while maintaining consistency in method calls.

#### HuggingfaceInvoker

- **Purpose**:
  - Specific interaction logic for Huggingface LLMs.
  - Ensures that any unique requirements or behaviors of the Huggingface platform are addressed.

#### OpenAIInvoker

- **Purpose**:
  - Specific interaction logic for OpenAI LLMs.
  - Tailors interactions to meet the requirements and best practices of the OpenAI platform.

### 3.3.2 Implementation

#### PromptBuilder

- **Methods**:
  - `build_summary_prompt(article_content: str) -> str`: Creates a prompt suitable for summarization tasks.
  - `build_script_prompt(article_content: str) -> str`: Crafts a prompt for generating scripts.

#### AbstractLLMInvoker

- **Methods**:
  - `invoke(prompt: str) -> str`: An abstract method to invoke any LLM. Specific LLMs will provide their own implementation of this method.

#### HuggingfaceInvoker (inherits from `AbstractLLMInvoker`):

- **Technologies**:
  - Utilizes the Huggingface Transformers Library for accessing and invoking models.
  - Implement the `invoke` method tailored for the Huggingface platform.

#### OpenAIInvoker (inherits from `AbstractLLMInvoker`):

- **Technologies**:
  - Leverages the OpenAI API for model invocation.
  - Provides a specific `invoke` method optimized for OpenAI's requirements.

### 3.3.3 Rationale

- **PromptBuilder**: Provides a centralized place to manage the prompt logic. This ensures consistency and ease of modifications.
- **AbstractLLMInvoker**: Ensures flexibility. If a new LLM platform is added in the future, we can extend this abstract class, ensuring seamless integration without major changes to the existing system.
- **Separate Invokers**: Each LLM provider might have different API structures, nuances, and error handling. Keeping them in separate classes ensures clarity and maintainability.

## 3.4 Search and Retrieval Service

### 3.4.1 Design

#### Objective
Enable users to query and retrieve articles and summaries based on content and metadata, leveraging vector search engines to ensure that the results are relevant and comprehensive.

#### **SearchEngine**

- **Purpose**:
  - Acts as the primary interface for executing search queries against stored articles.
  - Uses vector embeddings to index and retrieve articles, ensuring content similarity and relevance.

- **Structure**:
  - Methods:
    - `similarity_search(query: str) -> List[Article]`: Basic implementation to find articles most similar to the given query.
    - `advanced_search(query: str, metadata: dict) -> List[Article]`: Enhanced search capability to include additional filters and conditions based on article metadata.

#### **ArticleRetrieval**

- **Purpose**:
  - Fetches the full articles, article chunks, or summaries based on the search results.

- **Structure**:
  - Methods:
    - `retrieve_full_articles(article_ids: List[int]) -> List[Article]`: Returns full articles based on provided article IDs.
    - `retrieve_article_chunks(article_ids: List[int]) -> List[str]`: Extracts and returns specific sections or chunks of articles.
    - `retrieve_summaries(article_ids: List[int]) -> List[str]`: Provides the summaries of the given articles.

### 3.4.2 Implementation

#### **SearchEngine**

- **Technologies**:
  - Vector search engines such as Faiss or Annoy to facilitate efficient similarity search.
  - Vector embeddings generated from articles using pre-trained language models to ensure effective indexing.

- **Methods**:
  - `similarity_search(query: str) -> List[Article]`: Transforms the query into a vector embedding and searches for the nearest article embeddings in the index.
  - `advanced_search(query: str, metadata: dict) -> List[Article]`: Combines the similarity search with filters based on provided metadata to refine the search results.

#### **ArticleRetrieval**

- **Database Queries**:
  - Retrieve full articles or specific sections based on the returned article IDs from the search engine.
  - Utilize efficient querying mechanisms to ensure fast retrieval of large volumes of text data.

- **Methods**:
  - `retrieve_full_articles(article_ids: List[int]) -> List[Article]`: Direct database fetch based on primary keys.
  - `retrieve_article_chunks(article_ids: List[int]) -> List[str]`: Uses text processing to extract and return specific sections of the articles.
  - `retrieve_summaries(article_ids: List[int]) -> List[str]`: Fetches the pre-generated summaries of articles from the database.

### 3.4.3 Rationale

- **Vector-based Search**:
  The core advantage of vector-based search lies in its ability to identify similar articles even if the exact keywords or phrases aren't present. By translating both the query and the articles into a shared vector space, the system can identify content that is contextually and semantically related.

- **Advanced Search Capabilities**:
  While content similarity is crucial, there are scenarios where users may want to filter or prioritize results based on metadata (e.g., publication date, author, or source). The system's design provides this flexibility.

- **Multiple Retrieval Options**:
  Depending on the user's needs, they might want the full article, a concise summary, or specific sections of the content. Offering these options enhances user experience and utility.


## 3.4 Podcast Script Generation Module

### 3.4.1 Design

#### **ScriptGenerator**

- **Role**: To convert sets of summaries into coherent podcast scripts tailored to user preferences and guidelines.
  - **Why**: To produce content that can be easily vocalized, maintaining coherence and ensuring it aligns with user requirements.

#### **PromptBuilder for ScriptGeneration**

- **Role**: To construct appropriate prompts that guide the LLM in script generation, ensuring the final output adheres to the set guidelines and desired style.
  - **Why**: The effectiveness of the LLM is largely dependent on the clarity and specificity of the prompts it receives. A structured and well-defined prompt will guide the model to produce the desired output.

#### **Considerations for Expansion**:

1. **Duration**: Podcast scripts should be customizable to a certain duration, typically aiming for less than 5 minutes.
2. **Transitional Phrases**: These interlink the different sections of the podcast. Leveraging the LLM's strength here is vital.
3. **Source Attribution**: An essential part of any content, ensuring that the original sources of the summaries are appropriately credited.
4. **User Input**: The system should be adaptable, allowing users to define guidelines, styles, and other directives for the script.
5. **Review and Iteration**: The system should be flexible enough to allow for improvements, especially in areas where user feedback can guide development.

### 3.4.2 Implementation

#### **ScriptGenerator Class**:

Handles the actual process of taking summaries and desired configurations, and producing the podcast script.

```python
class ScriptGenerator:

    def __init__(self, llm_invoker):
        self.llm_invoker = llm_invoker
    
    def generate_script(self, summaries: List[str], style: str = "conversational", duration: int = 5, include_intro_conclusion: bool = True, source_attribution: bool = True) -> str:
        
        # Estimate the word count based on the desired duration
        target_word_count = self._estimate_word_count(duration)
        
        # Use PromptBuilder to create an appropriate prompt
        prompt = PromptBuilder.build_podcast_script_prompt(summaries, style, include_intro_conclusion, source_attribution)
        
        # Use the LLM to generate the script
        raw_script = self.llm_invoker.invoke(prompt)
        
        # Trim or adjust the script based on the target word count
        adjusted_script = self._adjust_script_length(raw_script, target_word_count)
        
        return adjusted_script

    def _estimate_word_count(self, duration: int) -> int:
        # Assuming an average reading speed of 150 words per minute
        return duration * 150

    def _adjust_script_length(self, script: str, target_word_count: int) -> str:
        # Simplistic approach: Split the script and keep only the required number of words.
        # Future implementations can be smarter about this.
        words = script.split()
        return ' '.join(words[:target_word_count])


class PromptBuilder:

    @staticmethod
    def build_podcast_script_prompt(summaries: List[str], style: str, include_intro_conclusion: bool, source_attribution: bool) -> str:
        # Combines the summaries into a single text
        combined_summaries = ' '.join(summaries)

        # Constructs the prompt
        prompt = f"Generate a {style} podcast script from the following summaries: {combined_summaries}"
        
        if include_intro_conclusion:
            prompt += " Include an introduction and conclusion."
        
        if source_attribution:
            prompt += " Remember to cite the sources."

        return prompt

```

#### Integration with LLM:
The actual generation of the podcast script requires integration with Large Language Models. The generated prompt is passed to a specific LLM invoker, such as HuggingfaceInvoker or OpenAIInvoker, which then returns the raw script. This raw script undergoes further processing to adjust its length and structure to match user specifications.