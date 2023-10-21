"""
SQLiteManager Module.

This module provides specialized database operations tailored for SQLite.
It extends the foundational database interactions outlined in the DatabaseManager class.

Classes:
    - SQLiteManager: Handles CRUD operations and other database interactions for SQLite.
"""

from typing import Optional
import sqlite3
from src.crawlers.data_structures.article import Article, ArticleType
from .database_manager import DatabaseManager


class SQLiteManager(DatabaseManager):
    """
    SQLiteManager: Specialized operations for SQLite.

    This class provides concrete implementations for the foundational database interactions
    outlined in the DatabaseManager class, tailored for SQLite.
    """

    def __init__(self, db_path="articles.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def save(self, article: Article) -> None:
        # pylint: disable=line-too-long
        query = "INSERT INTO articles (url, title, text, date, loaded_domain, author, description, keywords, lang, tags, image, is_vectorized, article_type, article_relevance, summary) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        self.cursor.execute(
            query,
            (
                article.url,
                article.title,
                article.text,
                article.date,
                article.loaded_domain,
                ",".join(article.author) if article.author else None,
                article.description,
                article.keywords,
                article.lang,
                ",".join(article.tags) if article.tags else None,
                article.image,
                article.is_vectorized,
                article.article_type.value,
                article.article_relevance,
                article.summary,
            ),
        )
        self.conn.commit()

    def update(self, article: Article) -> None:
        # pylint: disable=line-too-long
        query = "UPDATE articles SET url=?, title=?, text=?, date=?, loaded_domain=?, author=?, description=?, keywords=?, lang=?, tags=?, image=?, is_vectorized=? , article_type=?, article_relevance=?, summary=? WHERE id=?"
        self.cursor.execute(
            query,
            (
                article.url,
                article.title,
                article.text,
                article.date,
                article.loaded_domain,
                ",".join(article.author) if article.author else None,
                article.description,
                article.keywords,
                article.lang,
                ",".join(article.tags) if article.tags else None,
                article.image,
                article.is_vectorized,
                article.article_type.value,
                article.article_relevance,
                article.summary,
                article.article_id,
            ),
        )
        self.conn.commit()

    def delete(self, article_id: int) -> None:
        query = "DELETE FROM articles WHERE id=?"
        self.cursor.execute(query, (article_id,))
        self.conn.commit()

    def find_by_id(self, article_id: int) -> Article:
        # pylint: disable=line-too-long
        query = "SELECT title, text, id, date, url, loaded_domain, author, description, keywords, lang, tags, image, is_vectorized, article_type, article_relevance, summary FROM articles WHERE id=?"
        self.cursor.execute(query, (article_id,))
        result = self.cursor.fetchone()
        if result:
            return Article(
                title=result[0],
                text=result[1],
                _id=result[2],
                date=result[3],
                url=result[4] if result[4] else None,
                loaded_domain=result[5] if result[5] else None,
                author=result[6].split(",") if result[6] else None,
                description=result[7] if result[7] else None,
                keywords=result[8] if result[8] else None,
                lang=result[9] if result[9] else None,
                tags=result[10].split(",") if result[10] else None,
                image=result[11] if result[11] else None,
                is_vectorized=result[12],
                article_type=ArticleType(result[13]),
                article_relevance=result[14],
                summary=result[15],
            )
        return None

    # pylint: disable=line-too-long
    def find_all(
        self,
        limit: Optional[int] = None,
        sort_by: Optional[list[tuple[str, str]]] = None,
    ) -> list[Article]:
        # Base query
        # pylint: disable=line-too-long
        query = "SELECT title, text, id, date, url, loaded_domain, author, description, keywords, lang, tags, image, is_vectorized, article_type, article_relevance, summary  FROM articles"

        # If sort_by is provided, append the ORDER BY clause to the query
        if sort_by:
            order_by_clause = ", ".join(
                [f"{field} {order}" for field, order in sort_by]
            )
            query += f" ORDER BY {order_by_clause}"

        # If a limit is provided, append the LIMIT clause to the query
        if limit is not None:
            query += f" LIMIT {limit}"

        self.cursor.execute(query)
        results = self.cursor.fetchall()
        return [
            Article(
                title=row[0],
                text=row[1],
                _id=row[2],
                date=row[3],
                url=row[4] if row[4] else None,
                loaded_domain=row[5] if row[5] else None,
                author=row[6].split(",") if row[6] else None,
                description=row[7] if row[7] else None,
                keywords=row[8] if row[8] else None,
                lang=row[9] if row[9] else None,
                tags=row[10].split(",") if row[10] else None,
                image=row[11] if row[11] else None,
                is_vectorized=row[12],
                article_type=ArticleType(row[13]),
                article_relevance=row[14],
                summary=row[15],
            )
            for row in results
        ]

    def find_by_criteria(self, criteria: dict) -> list[Article]:
        # This method would require more complex SQL generation based on the criteria.
        # For simplicity, I'm skipping the implementation here.
        pass

    def mark_as_vectorized(self, article_id: int) -> None:
        """
        Set the vectorization flag for an article.

        Parameters:
            article_id (int): The ID of the article to be marked.

        Returns:
            None
        """
        query = "UPDATE articles SET is_vectorized=1 WHERE id=?"
        self.cursor.execute(query, (article_id,))
        self.conn.commit()

    def is_vectorized(self, article_id: int) -> bool:
        """
        Check the vectorization status for an article.

        Parameters:
            article_id (int): The ID of the article to check.

        Returns:
            bool: True if the article is vectorized, False otherwise.
        """
        query = "SELECT is_vectorized FROM articles WHERE id=?"
        self.cursor.execute(query, (article_id,))
        result = self.cursor.fetchone()
        return result[0] == 1

    def batch_save(self, articles: list[Article]) -> None:
        # pylint: disable=line-too-long
        query = "INSERT INTO articles (url, title, text, date, loaded_domain, author, description, keywords, lang, tags, image, is_vectorized, article_type, article_relevance, summary) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        values = [
            (
                article.url,
                article.title,
                article.text,
                article.date,
                article.loaded_domain,
                ",".join(article.author) if article.author else None,
                article.description,
                article.keywords,
                article.lang,
                ",".join(article.tags) if article.tags else None,
                article.image,
                article.is_vectorized,
                article.article_type.value,
                article.article_relevance,
                article.summary,
            )
            for article in articles
        ]
        self.cursor.executemany(query, values)
        self.conn.commit()

    def initialize_schema(self):
        """
        Initialize the SQLite database schema.
        Create the articles table if it doesn't exist.
        """
        # Check if the articles table exists
        self.cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='articles'"
        )
        if not self.cursor.fetchone():
            # If the articles table doesn't exist, create it
            self.cursor.execute(
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
                    is_vectorized INTEGER DEFAULT 0,
                    article_type INTEGER,
                    article_relevance INTEGER,
                    summary TEXT
                )
                """
            )
            self.conn.commit()

    def close(self):
        """
        Closes the connection to the database.
        """
        self.conn.close()
