"""
PostgreSQLManager Module.

This module provides specialized database operations tailored for PostgreSQL.
It extends the foundational database interactions outlined in the DatabaseManager class,
utilizing the psycopg2 library for PostgreSQL-specific operations.

Classes:
    - PostgreSQLManager: Handles CRUD operations and other database interactions for PostgreSQL.

Note: VSCode pylint might flag the psycopg2 import, but it should work fine in the terminal.
"""

# VSCode pylint is having trouble with the psycopg2 import, but it works fine in the terminal.
# pylint: disable=import-error
import psycopg2
from psycopg2 import sql

from src.crawlers.data_structures.article import Article
from .database_manager import DatabaseManager


class PostgreSQLManager(DatabaseManager):
    """
    PostgreSQLManager: Specialized operations for PostgreSQL.

    This class provides concrete implementations for the foundational database interactions
    outlined in the DatabaseManager class, tailored for PostgreSQL using the psycopg2 library.
    """

    def __init__(self, connection_params):
        self.conn = psycopg2.connect(**connection_params)
        self.cursor = self.conn.cursor()

    def save(self, article: Article) -> None:
        query = sql.SQL("INSERT INTO articles (url, title, text) VALUES (%s, %s, %s)")
        self.cursor.execute(query, (article.url, article.title, article.text))
        self.conn.commit()

    def update(self, article: Article) -> None:
        query = sql.SQL("UPDATE articles SET url=%s, title=%s, text=%s WHERE id=%s")
        self.cursor.execute(
            query, (article.url, article.title, article.text, article.id)
        )
        self.conn.commit()

    def delete(self, article_id: int) -> None:
        query = sql.SQL("DELETE FROM articles WHERE id=%s")
        self.cursor.execute(query, (article_id,))
        self.conn.commit()

    def find_by_id(self, article_id: int) -> Article:
        # pylint: disable=line-too-long
        query = sql.SQL(
            "SELECT title, text, id, date, url, loaded_domain, author, description, keywords, lang, tags, image FROM articles WHERE id=%s"
        )
        self.cursor.execute(query, (article_id,))
        result = self.cursor.fetchone()
        return Article(
            title=result[0],
            text=result[1],
            _id=result[2],
            date=result[3],
            url=result[4],
            loaded_domain=result[5],
            author=result[6],
            description=result[7],
            keywords=result[8],
            lang=result[9],
            tags=result[10],
            image=result[11],
        )

    def find_all(self) -> list[Article]:
        # pylint: disable=line-too-long
        query = sql.SQL(
            "SELECT title, text, id, date, url, loaded_domain, author, description, keywords, lang, tags, image FROM articles"
        )
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        return [
            Article(
                title=row[0],
                text=row[1],
                _id=row[2],
                date=row[3],
                url=row[4],
                loaded_domain=row[5],
                author=row[6],
                description=row[7],
                keywords=row[8],
                lang=row[9],
                tags=row[10],
                image=row[11],
            )
            for row in results
        ]

    def find_by_criteria(self, criteria: dict) -> list[Article]:
        # This method would require more complex SQL generation based on the criteria.
        # For simplicity, I'm skipping the implementation here.
        pass

    def mark_as_vectorized(self, article_id: int) -> None:
        query = sql.SQL("UPDATE articles SET is_vectorized=True WHERE id=%s")
        self.cursor.execute(query, (article_id,))
        self.conn.commit()

    def is_vectorized(self, article_id: int) -> bool:
        query = sql.SQL("SELECT is_vectorized FROM articles WHERE id=%s")
        self.cursor.execute(query, (article_id,))
        result = self.cursor.fetchone()
        return result[0]

    def batch_save(self, articles: list[Article]) -> None:
        query = sql.SQL("INSERT INTO articles (url, title, text) VALUES %s")
        values = [(article.url, article.title, article.text) for article in articles]
        psycopg2.extras.execute_values(self.cursor, query, values)
        self.conn.commit()
