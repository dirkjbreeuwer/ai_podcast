"""
Utility functions for working with LLMs
"""

import json

# pylint: disable=import-error
import tiktoken


def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.encoding_for_model(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


def count_tokens_in_summaries(filename: str) -> int:
    """
    Count the total number of tokens across all summaries in the provided JSON file.

    Args:
    - filename (str): Path to the JSON file containing the articles' summaries.

    Returns:
    - int: Total number of tokens across all summaries.
    """

    total_tokens = 0

    # Load the JSON file
    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)
        for article in data:
            summary = article.get("summary", "")
            num_tokens = num_tokens_from_string(summary, "gpt-4-0613")
            total_tokens += num_tokens
    return total_tokens
