"""
Module: Prompt Builder

Provides tools to craft prompts for interaction with Language Learning Models (LLMs).
Handles creation of prompts for tasks like summarization and script generation.

Classes:
    - PromptBuilder: Manages the creation of prompts to invoke LLMs.
"""


class PromptBuilder:
    """
    Manages the creation of prompts for Language Learning Models (LLMs).

    Provides methods to craft prompts for tasks such as summarization and script generation.
    """

    @staticmethod
    def build_summary_prompt(article_content: str) -> str:
        """
        Create a prompt suitable for summarization.

        Args:
            article_content (str): The content of the article to be summarized.

        Returns:
            str: A crafted prompt for summarization.
        """
        return f"Summarize the following article: {article_content}"

    @staticmethod
    def build_script_prompt(article_content: str) -> str:
        """
        Craft a prompt for script generation.

        Args:
            article_content (str): The content of the article to be turned into a script.

        Returns:
            str: A crafted prompt for script generation.
        """
        return f"Convert the following article into a script: {article_content}"
