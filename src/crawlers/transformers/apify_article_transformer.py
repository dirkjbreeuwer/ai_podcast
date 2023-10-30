"""
Module for transforming Apify's web scrape output into the standardized Article data structure.

Classes:
    - ApifyArticleCrawlerOutputTransformer: Transforms Apify's output to the `Article` format.
"""

from src.crawlers.transformers.base_transformer import CrawlerOutputTransformer

from src.crawlers.data_structures.article import Article


# pylint: disable=too-few-public-methods
class ApifyArticleCrawlerOutputTransformer(CrawlerOutputTransformer):
    """
    Transforms the output from Apify's web scrape into the Article data structure.
    """

    def __init__(self, raw_data: dict):
        self.raw_data = raw_data

    def transform(self, raw_data: dict = None) -> Article:
        """
        Converts Apify's output to the `Article` structure.

        Args:
            raw_data (dict): The raw outputs from Apify's scrape.
            If not provided, uses the instance's raw_data.

        Returns:
            Article: The transformed Article instance.
        """
        if not raw_data:
            raw_data = self.raw_data

        title = raw_data.get("title", "")
        text = raw_data.get("text", "")
        _id = raw_data.get("id", "")
        date = raw_data.get("date", "")
        url = raw_data.get("url", "")
        loaded_domain = raw_data.get("loadedDomain", "")
        author = raw_data.get("author", [])
        description = raw_data.get("description", "")
        keywords = raw_data.get("keywords", "")
        lang = raw_data.get("lang", "")
        tags = raw_data.get("tags", [])
        image = raw_data.get("image", "")
        videos = raw_data.get("videos", [])

        return Article(
            title=title,
            text=text,
            _id=_id,
            date=date,
            url=url,
            loaded_domain=loaded_domain,
            author=author,
            description=description,
            keywords=keywords,
            lang=lang,
            tags=tags,
            image=image,
            videos=videos,
        )
