# AI Podcast


## Installation

Follow these steps to set up and install the necessary packages for the project:

### 1. Install Packages

Use Poetry to install the required packages for the project:
```
poetry install
```

### 2. Activate Virtual Environment (venv)

Once the packages are installed, activate the virtual environment:
```
poetry shell
```

### 3. Run Post-install Script

After activating the virtual environment, run the post-install script:
```
poetry run postinstall
```

#### Why is the Post-install Script Needed?

The post-install script is essential for ensuring the smooth operation of the Chroma library in our project. Due to a known SQLite version incompatibility issue with Chroma, we've implemented a workaround using `pysqlite3-binary`. The post-install script automates this workaround by making necessary modifications, allowing Chroma to function correctly without manual intervention. This ensures a seamless experience for users and developers alike.

## Setting Up API Keys

To integrate with APIFY and OPENAI, you'll need to set up the respective API keys. Follow these steps:

### 1. Copy the Example Environment File

Start by copying the `.env.example` file to a new file named `.env`:
```
cp .env.example .env
```

### 2. Add Your API Keys

Open the `.env` file in your preferred text editor. You'll find placeholders for the APIFY and OPENAI keys. Replace them with your actual keys.

**Note**: When adding your keys, ensure you don't wrap them in quotes. Enter them as plain text.

Example:
```
APIFY_API_KEY=YOUR_APIFY_KEY_HERE
OPENAI_API_KEY=YOUR_OPENAI_KEY_HERE
```

With these steps, your project is now configured to use the APIFY and OPENAI services.

Of course! Here's the note added to the "Running Tests" section:

## Running Tests

To ensure the functionality and reliability of the project, we have a suite of tests that you can run. Use the following command to execute the tests:

```
pytest ./tests/*
```

This will run all the tests located in the `tests` directory. Make sure to run them after making any changes to the codebase to ensure everything is working as expected.

> **Note**: Running these tests will invoke API calls to Apify and OpenAI. While the costs associated with these calls are minimal, please be aware that they might incur charges. Typically, the total cost should be less than $0.10. Always monitor your API usage to avoid unexpected charges.


## Usage

### Using Jupyter Notebook

The AI Podcast tool can be used via the Jupyter notebook `main.ipynb`. To generate your podcast, simply follow these steps:

1. Open the `main.ipynb` notebook in Jupyter.

2. Run all the cells in the notebook. The notebook is set up to guide you through the process of generating your podcast.

3. Your output files should be in the `./data` directory.

### Using Streamlit

Alternatively, you can use the AI Podcast tool with Streamlit. To do so, follow these steps:

1. Navigate to the project's root directory in your terminal or command prompt.

2. Run the following command:

```
streamlit run ./src/ui/app.py
```

3. A new tab should open in your web browser with the Streamlit UI. Follow the instructions in the UI to generate your podcast.


## Roadmap

Here is a list of features and enhancements we are currently working on or planning to add in the future:

- [ ] WIP: User interface for running workflows and visualizing output.
- [ ] Free alternatives to the crawler and summarizer (currently using OpenAI, which will always incur costs).
- [ ] Optimizations such as re-downloading and re-calculating only once a week or day.
- [ ] Improved content ranking system.
- [ ] Human in the loop: the ability for users to select the final set of articles/content that goes into the summary.
- Enhanced crawling capabilities:
- [ ] Arxiv
- [ ] Github
- [ ] Youtube




