"""
Module to generate script based on summaries of articles
"""

import os

# pylint: disable=import-error
from dotenv import load_dotenv
from magentic import prompt

# Load environment variables from .env file
load_dotenv()

# Set the environment variable
os.environ["MAGENTIC_OPENAI_MODEL"] = "gpt-4"


# pylint: disable=line-too-long
@prompt(
    """Generate a podcast script based on the following article summarries: {article_summaries}
        ---
        The podcast should be informative, factual and insightful.
        The podcast script should be in the style of Ben Thomson from Statcherry or Mark Andreessen from the a16z podcast.
        The podcast should use straightforward language and avoid jargon.
        The podcast should include an introduction section, a body section, and a conclusion section.
        The body section should have 2 chapters: Product releases and AI founding rounds.
        Each section should go in depth on the topic and try to include all points in the article summaries.
        After each section be sure to reflect on key themes and takeaways.
        Our audience is entrepreneurs who are AI savvy.
        Your name, the podcast narrator, is Sophia.
        """
)
# pylint: disable=unused-argument
def generate_script(article_summaries: str) -> str:
    """
    Generates a podcast script based on the summaries of articles.

    Args:
        article_summaries (str): The summaries of the articles.

    Returns:
        str: A podcast script.
    """
