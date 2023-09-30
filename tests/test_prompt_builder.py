"""
Test Module for PromptBuilder
-----------------------------

Contains unit tests for the PromptBuilder class to ensure prompt creation for LLMs is accurate.

Classes:
    - TestPromptBuilder: Test suite for the PromptBuilder class.
"""

import unittest
from src.llm.prompt_builder import PromptBuilder


class TestPromptBuilder(unittest.TestCase):
    """
    Test suite for the PromptBuilder class.

    Contains methods to test the prompt creation functionality for
    tasks like summarization and script generation.
    """

    def test_build_summary_prompt(self):
        """
        Test the build_summary_prompt method.

        Ensure the method crafts the correct prompt for summarization tasks.
        """
        content = "This is a sample article about AI."
        expected_prompt = (
            "Summarize the following article: This is a sample article about AI."
        )
        result = PromptBuilder.build_summary_prompt(content)
        self.assertEqual(result, expected_prompt)

    def test_build_script_prompt(self):
        """
        Test the build_script_prompt method.

        Ensure the method crafts the correct prompt for script generation tasks.
        """
        content = "This is a sample article about AI."
        # pylint: disable=line-too-long
        expected_prompt = "Convert the following article into a script: This is a sample article about AI."
        result = PromptBuilder.build_script_prompt(content)
        self.assertEqual(result, expected_prompt)


if __name__ == "__main__":
    unittest.main()
