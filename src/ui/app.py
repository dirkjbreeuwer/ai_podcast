"""
This module defines the Streamlit UI for the AI Podcast Workflow application.
It uses the Streamlit library to create a web-based user interface that allows users to
input URLs for crawling and storing articles, summarize articles, and display summarized articles.
The module also includes performance profiling using cProfile and pstats.
"""

import cProfile
import pstats

# pylint: disable=import-error
import streamlit as st
from dotenv import load_dotenv
from src.workflow.article_workflow import ArticleWorkflow

# Load environment variables
load_dotenv()


class StreamlitUI:
    """
    This class handles the Streamlit UI components and interactions.
    """

    def __init__(self, workflow):
        """
        Initializes the StreamlitUI class.

        Args:
            workflow (ArticleWorkflow): The workflow object to handle article processing.
        """
        self.workflow = workflow

    def run(self):
        """
        Runs the Streamlit UI.
        """
        st.title("AI Podcast Workflow")
        self.crawl_and_store_articles_ui()
        self.summarize_articles_ui()
        self.show_summarized_articles_ui()

    def crawl_and_store_articles_ui(self):
        """
        UI components for crawling and storing articles.
        """
        st.subheader("Crawl and Store Articles")
        urls = st.text_area("Enter URLs to crawl, separated by commas:")
        if st.button("Crawl and Store"):
            if urls:
                url_list = urls.split(",")
                num_articles = self.workflow.crawl_and_store_articles(url_list)
                st.success(f"Successfully crawled and stored {num_articles} articles.")
            else:
                st.error("Please enter at least one URL.")

    def summarize_articles_ui(self):
        """
        UI components for summarizing articles.
        """
        st.subheader("Summarize Articles")
        if st.button("Summarize"):
            self.workflow.summarize_articles()
            st.success("Successfully summarized articles.")

    def show_summarized_articles_ui(self):
        """
        UI components for showing summarized articles.
        """
        st.subheader("Show Summarized Articles")
        if st.button("Show Summarized Articles"):
            articles = self.workflow.get_summarized_articles()
            for article in articles:
                st.write(f"Title: {article.title}")
                st.write(f"Summary: {article.summary}")
                st.write(f"Relevance: {article.article_relevance}")
                st.write(f"Article Type: {article.article_type.name}")
                st.write(f"Date: {article.date}")
                st.write(f"URL: {article.url}")
                st.write("-----")


def main():
    """
    Main function to run the Streamlit UI.
    """
    profiler = cProfile.Profile()
    profiler.enable()

    # Initialize the ArticleWorkflow class
    workflow = ArticleWorkflow(relational_db_path="./data/articles_test.sqlite")

    # Initialize and run the Streamlit UI
    user_interface = StreamlitUI(workflow)
    user_interface.run()

    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats("cumulative")  # Sort by cumulative time
    stats.dump_stats("profile_results.prof")  # Save results to a file


if __name__ == "__main__":
    main()
