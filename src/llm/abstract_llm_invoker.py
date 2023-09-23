"""
LLM Invokers Module
-------------------

Provides tools to interact with various Language Learning Models (LLMs) such as
Huggingface and OpenAI platforms.

Handles the invocation of LLMs for tasks like summarization and script generation.

Classes:
    - AbstractLLMInvoker: Base class for LLM interactions.
    - HuggingfaceInvoker: Specific interactions for Huggingface LLMs.
    - OpenAIInvoker: Specific interactions for OpenAI LLMs.
"""

from abc import ABC, abstractmethod


# pylint: disable=too-few-public-methods
class AbstractLLMInvoker(ABC):
    """
    Abstract base class for LLM interactions.

    Provides a consistent interface for interacting with various LLMs.
    """

    @abstractmethod
    def invoke(self, prompt: str) -> str:
        """
        Generalized method to interact with any LLM.

        Parameters:
            prompt (str): The prompt to be passed to the LLM.

        Returns:
            str: The response from the LLM.
        """
