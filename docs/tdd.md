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

## 3.1 Web Crawlers Module

### 3.1.1 Design and Purpose

#### Purpose:
To fetch, extract, and standardize articles from the web, making them suitable for downstream processing.

#### Scope:
Scraping from diverse online platforms, transforming the results into a uniform structure, and ensuring reliability and efficiency in data collection.

#### Primary Objective:
Seamless and consistent scraping of articles across various web sources.

#### Secondary Objectives:
- Standardization of the scraped data.
- Ensuring compatibility with downstream modules.

### 3.1.2 Key Components

#### Data Structures:

- **Article**:
  - **Description**: Holds attributes like URL, title, text, and associated metadata of each scraped article.
  - **Relationships**: Serves as the primary data type for the downstream storage and processing modules.

#### Classes/Interfaces:

- **Crawler**:
  - **Role**: Foundation for web crawlers ensuring consistency.
  - **Attributes**:
    - **Name**: Specific configurations for scraping. Type: `dict`.
  - **Methods**:
    - `fetch()`: Single article retrieval.
    - `batch_fetch()`: Multiple article retrieval.
    - `get_status()`: Current status of the crawler.

- **ApifyArticleCrawler**:
  - **Role**: Crawler tailored for the Apify platform.
  - **Methods**:
    - `set_options()`: Configuration setter for Apify.

- **CrawlerOutputTransformer**:
  - **Role**: Converts diverse crawler outputs into `Article` data type.
  - **Methods**:
    - `transform()`: Raw data transformation into `Article`.

- **ApifyCrawlerOutputTransformer**:
  - **Role**: Transformation for Apify-specific outputs.
  - **Methods**:
    - `transform()`: Apify data transformation into `Article`.

### 3.1.3 Implementation Details

#### Data Structures:

- **Article**:
  - **Pseudo-code**:
    ```python
    class Article:
        def __init__(self, url, title, text, ...):
            self.url = url
            self.title = title
            ...
    ```

#### Classes/Interfaces:

- **ApifyCrawlerOutputTransformer**:
  - **Attributes**:
    - **raw_data**: Type: `dict`. Contains the raw outputs from Apify's scrape.
  - **Methods**:
    - **transform**:
      - **Purpose**: Converts Apify's output to the `Article` structure.
      - **Parameters**: `raw_data` (Type: `dict`).
      - **Return Type**: `Article`.
      - **Pseudo-code**:
        ```python
        def transform(self, raw_data):
            article = Article(...)
            return article
        ```
      - **Complexity**: Time: O(1) (for the transformation, not considering possible IO operations).



---

## 3.2 Data Storage Module

### 3.2.1 Design and Purpose

#### Purpose:
To persist articles into appropriate storage mechanisms, facilitating efficient retrieval, update, and relationship management, and to ensure vectorized data is stored for similarity search.

#### Scope:
Incorporates both relational database storage for structured articles and vector database storage for vectorized article embeddings.

#### Primary Objective:
Reliable storage of articles and their associated embeddings in appropriate databases.

#### Secondary Objectives:
- Efficient retrieval and update operations.
- Seamless integration between structured and vectorized storage mechanisms.

### 3.2.2 Key Components

#### Data Structures:

- **Article (Refer to 3.1 for definition)**:
  - **Description**: A standardized representation for articles scraped from the web. Used here for persistence in the database.
  - **Relationships**: Associated with authors, sources, and tags.

#### Classes/Interfaces:

- **DatabaseManager**:
  - **Role**: Provides foundational database interactions.
  - **Methods**:
    - `save()`: Persist a new article.
    - `update()`: Modify an existing article.
    - `delete()`: Remove an article by ID.
    - `find_by_id()`: Retrieve a specific article.
    - `find_all()`: Retrieve all articles.
    - `find_by_criteria()`: Retrieve articles by certain criteria.
    - `mark_as_vectorized()`: Set the vectorization flag for an article.
    - `is_vectorized()`: Check vectorization status for an article.
    - `batch_save()`: Persist multiple articles.

- **PostgreSQLManager**:
  - **Role**: Specialized operations for PostgreSQL.

- **ChunkService**:
  - **Role**: Facilitate article chunking.
  - **Methods**:
    - `split_into_chunks()`: Divide an article into smaller parts.

- **EmbeddingService**:
  - **Role**: Generate embeddings from text.
  - **Methods**:
    - `generate_embedding()`: Produce embeddings using LLMs.

- **VectorDBManager**:
  - **Role**: Interface for vector database operations.

- **ChromaDBManager**:
  - **Role**: Operations specific to ChromaDB.

### 3.2.3 Implementation Details


#### Classes/Interfaces:

- **DatabaseManager**:
  - **Methods**:
    - **save**:
      - **Purpose**: Persist a new article.
      - **Parameters**: `article` (Type: `Article`).
      - **Return Type**: None.
    - (Continue with other methods similarly...)

- **ChunkService**:
  - **Methods**:
    - **split_into_chunks**:
      - **Purpose**: Split an article into smaller textual chunks.
      - **Parameters**: `article` (Type: `Article`).
      - **Return Type**: `List[str]`.

- **EmbeddingService**:
  - **Methods**:
    - **generate_embedding**:
      - **Purpose**: Generate embeddings for a text chunk.
      - **Parameters**: `text_chunk` (Type: `str`).
      - **Return Type**: `Embedding` (or appropriate data type).


## 3.3 Language Models

### 3.3.1 Design and Purpose

**Purpose**: Facilitate the interaction with various Language Learning Models (LLMs) to perform tasks such as summarization and script generation.

**Scope**: This module encompasses the creation of prompts, as well as interaction logic with different LLMs, namely Huggingface and OpenAI platforms.

**Primary Objective**: Enable seamless interaction with LLMs, ensuring consistency and accuracy in tasks.

**Secondary Objectives**:
- Standardize the invocation of various LLMs through a unified interface.
- Provide tailored interactions for specific LLM platforms.

### 3.3.2 Key Components

#### Classes/Interfaces:

- **PromptBuilder**:
  - **Role**: Manage the creation of prompts to invoke LLMs.
  - **Methods**:
    - `build_summary_prompt`: Craft a prompt for summarization tasks.
    - `build_script_prompt`: Design a prompt for script generation.

- **AbstractLLMInvoker**:
  - **Role**: Serve as the foundational structure for all LLM interactions, ensuring consistency in method calls.
  - **Methods**:
    - `invoke`: A generalized method to interact with any LLM.

- **HuggingfaceInvoker (inherits from AbstractLLMInvoker)**:
  - **Role**: Define specific interactions for Huggingface LLMs.
  - **Attributes**:
    - **Technologies**: Utilize Huggingface Transformers Library.
  - **Methods**:
    - `invoke`: Implement the interaction tailored for Huggingface.

- **OpenAIInvoker (inherits from AbstractLLMInvoker)**:
  - **Role**: Define specific interactions for OpenAI LLMs.
  - **Attributes**:
    - **Technologies**: Leverage OpenAI API.
  - **Methods**:
    - `invoke`: Tailor the method for OpenAI's requirements.

### 3.3.3 Implementation Details

#### Classes/Interfaces:

- **PromptBuilder**:
  - **Methods**:
    - `build_summary_prompt(article_content: str) -> str`: Create a prompt suitable for summarization.
    - `build_script_prompt(article_content: str) -> str`: Craft a prompt for script generation.

- **AbstractLLMInvoker**:
  - **Methods**:
    - `invoke(prompt: str) -> str`: A method to be implemented by each specific LLM invoker for model interaction.

- **HuggingfaceInvoker**:
  - **Methods**:
    - `invoke`: Specific to Huggingface platform, it accesses and invokes models using the Transformers Library.

- **OpenAIInvoker**:
  - **Methods**:
    - `invoke`: Specifically optimized for OpenAI's model invocation requirements.

### 3.3.4 Rationale

- **PromptBuilder**: Centralize prompt management for consistency and modifiability.
- **AbstractLLMInvoker**: Offers a flexible structure for future LLM platform extensions, ensuring integration without major system alterations.
- **Dedicated Invokers**: Recognizes and accommodates the nuances and unique structures of each LLM provider, enhancing clarity and maintainability.

# 3.4 Search and Retrieval Service

## 3.4.1 Design and Purpose

**Purpose**: Empower users to efficiently and comprehensively query and fetch articles based on a query.

**Scope**: This module encompasses the functionalities of executing search queries on stored articles and fetching various components (full articles, chunks, summaries) of the retrieved articles.

**Primary Objective**: Deliver relevant search results using vector embeddings and provide options for content retrieval.

**Secondary Objectives**:
- Allow users to refine search based on content and metadata.
- Offer quick and efficient access to different segments of the content.

## 3.4.2 Evaluation of Options

**Option A**: Use a Vector Database (e.g., Chroma DB) for the Entire Process.

**Option B**: Use Existing Modules for Chunking, Embedding + FAISS for Indexing/Search + SQLite for Retrieval.

After evaluating the pros and cons of each option, we have decided to proceed with **Option B** for the following reasons:

- **Modularity**: Ensures easier updates, optimizations, or replacements of individual modules.
- **Customization**: Allows for tailored optimizations or adjustments based on specific needs.
- **Leveraging Existing Work**: Ensures that previous development efforts are not wasted and provides a foundation to build upon.

### 3.4.3 Key Components

#### Classes/Interfaces:

- **SearchEngine**:
  - **Role**: Primary interface for executing vector-based search queries on stored articles.
  - **Methods**:
    - `similarity_search`: Conduct a basic similarity search on articles.
    - `advanced_search`: Perform an enhanced search based on content and metadata.

- **ArticleRetrieval**:
  - **Role**: Fetch various components of articles (full, chunks, summaries) based on search results.
  - **Methods**:
    - `retrieve_full_articles`: Fetch complete articles using given IDs.
    - `retrieve_article_chunks`: Extract specific segments from articles.
    - `retrieve_summaries`: Get pre-generated article summaries.

### 3.4.4 Implementation Details

#### Classes/Interfaces:

- **SearchEngine**:
  - **Attributes**:
    - **Technologies**: Leverage vector search engines (e.g., Faiss, Annoy) and pre-trained language models for embeddings.
  - **Methods**:
    - `similarity_search(query: str) -> List[Article]`: Convert query to vector embedding, search for nearest article embeddings.
    - `advanced_search(query: str, metadata: dict) -> List[Article]`: Combine similarity search with metadata filters to narrow results.

- **ArticleRetrieval**:
  - **Attributes**:
    - **Database Queries**: Efficiently fetch full articles or specific sections based on returned article IDs from the search engine.
  - **Methods**:
    - `retrieve_full_articles(article_ids: List[int]) -> List[Article]`: Fetch directly from the database using primary keys.
    - `retrieve_article_chunks(article_ids: List[int]) -> List[str]`: Use text processing to extract required sections.
    - `retrieve_summaries(article_ids: List[int]) -> List[str]`: Access pre-generated article summaries from the database.

### 3.4.5 Rationale

- **Vector-based Search**: Vector search identifies similar articles even without exact keyword matches. It understands context and semantic similarities by translating queries and articles into shared vector spaces.

- **Advanced Search Capabilities**: Alongside content similarity, users can filter results using metadata (e.g., date, author), enhancing the search experience.

- **Multiple Retrieval Options**: Users might need complete articles, specific sections, or summaries. Providing these options ensures a comprehensive user experience.



## 3.5 Podcast Script Generation Module

### 3.5.1 Design and Purpose

**Purpose**: To convert summarized content into coherent, user-tailored podcast scripts that can be vocalized effortlessly while adhering to set guidelines and styles.

**Scope**: The module encompasses functionalities to craft podcast scripts based on user preferences, integrating Large Language Models for script generation, and adjusting outputs to desired specifications.

**Primary Objective**: Produce podcast scripts from sets of summaries in a coherent manner while staying aligned with user requirements.

**Secondary Objectives**:
- Ensure that scripts can be fine-tuned for desired durations.
- Integrate transitional phrases for seamless content flow.
- Attribute content to the original sources.
- Make the system adaptable to user-specified guidelines, styles, and directives.
- Implement a review mechanism to iterate and improve script outputs.

### 3.5.2 Key Components

#### Classes/Interfaces:

- **ScriptGenerator**:
  - **Role**: Main class to handle the transformation of summaries into podcast scripts based on given configurations.
  - **Attributes**:
    - `llm_invoker`: Mechanism to call the LLM for script generation.
  - **Methods**:
    - `generate_script`: Converts summaries into podcast scripts.
    - `_estimate_word_count`: Calculates expected word count for given duration.
    - `_adjust_script_length`: Modifies script length to match target word count.

- **PromptBuilder for ScriptGeneration**:
  - **Role**: Constructs LLM prompts for script generation ensuring desired styles and guidelines are respected.
  - **Methods**:
    - `build_podcast_script_prompt`: Creates a suitable prompt to guide LLM in generating the podcast script.

### 3.5.3 Implementation Details

#### Classes/Interfaces:

- **ScriptGenerator**:
  - **Attributes**:
    - `llm_invoker`: Interface for LLM invocation, can be implementations such as HuggingfaceInvoker or OpenAIInvoker.
  - **Methods**:
    - `generate_script(summaries: List[str], style: str = "conversational", duration: int = 5, include_intro_conclusion: bool = True, source_attribution: bool = True) -> str`: Generates a podcast script from summaries based on style, duration, and other preferences. Integrates with the LLM to get the raw script and then adjusts its length and structure as per user specifications.
    - `_estimate_word_count(duration: int) -> int`: Approximates the word count based on desired script duration.
    - `_adjust_script_length(script: str, target_word_count: int) -> str`: Adapts the script to fit the desired word count.

- **PromptBuilder**:
  - **Methods**:
    - `build_podcast_script_prompt(summaries: List[str], style: str, include_intro_conclusion: bool, source_attribution: bool) -> str`: Combines the given summaries into a unified text and crafts an LLM prompt for script generation considering the provided style, introduction, conclusion, and source attribution preferences.

# 4. Complete Workflow

## 4.1 Overview

The system is designed to provide an end-to-end solution for web-based article crawling, processing, storage, search, retrieval, and podcast script generation. The workflow encompasses the following steps:

1. **Article Crawling**: The Crawler class fetches articles from various online sources. The Transformer class then standardizes the crawl output into the `Article` data structure.
2. **Storage**: The SQLite Manager class handles CRUD operations, storing the articles in a structured manner for efficient retrieval.
3. **Chunking**: The Chunking service divides articles into smaller textual chunks, facilitating vector search.
4. **Embedding**: The Embedding service uses LLMs to convert text chunks into vector space, generating embeddings that represent the content.
5. **Indexing and Search**: Using FAISS, articles are indexed based on their embeddings. When a search query is made, it's also embedded into the same vector space, and a similarity search is executed to find the most relevant articles or chunks.
6. **Retrieval**: Based on the search results, articles or specific chunks are retrieved from the SQLite database.
7. **Podcast Script Generation**: Summarized content is transformed into coherent podcast scripts using the Script Generator module. These scripts can then be vocalized or used for other purposes.

## 4.2 Rationale

The workflow is designed to be modular and scalable. Each step is handled by a dedicated module, ensuring that the system can efficiently process large volumes of data and deliver accurate results. The choice of tools and technologies at each step is based on their suitability for the task, ensuring optimal performance and maintainability.

