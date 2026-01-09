# AutoDoc Pro
================

AutoDoc Pro is a Streamlit application that generates AI-powered documentation for GitHub repositories. It uses the Groq API to summarize code and generate documentation in Markdown format.

## Key Features

*   **GitHub Repository Support**: AutoDoc Pro supports GitHub repositories and can clone them using Git or download ZIP files.
*   **AI-Powered Documentation**: The application uses the Groq API to generate documentation based on the code in the repository.
*   **Customizable**: Users can select the LLM model and theme to suit their needs.
*   **Easy to Use**: The application provides a simple and intuitive interface for users to input the repository URL and generate documentation.

## Installation Instructions

To install AutoDoc Pro, follow these steps:

1.  Clone the repository using Git or download the ZIP file.
2.  Install the required dependencies by running `pip install -r requirements.txt`.
3.  Create a `.env` file and set the `GROQ_API_KEY` environment variable with your Groq API key.
4.  Run the application using `streamlit run app.py`.

## Usage Examples

### Example 1: Generating Documentation for a GitHub Repository

```python
import streamlit as st
from src.repo_handler import process_repository

repo_url = "https://github.com/user/repository"
file_contents = process_repository(repo_url)

if file_contents:
    # Process the file contents and generate documentation
    pass
```

### Example 2: Using the Groq API to Generate Documentation

```python
import streamlit as st
from src.llm_service import LLMService

llm = LLMService()
context = "Your code or context here"
model = "llama-3.3-70b-versatile"
doc_type = "readme"

documentation = llm.generate_documentation(context, model, doc_type)

if documentation:
    # Display the generated documentation
    st.markdown(documentation)
```

## Project Structure

The project is structured as follows:

*   `app.py`: The main application file that runs the Streamlit app.
*   `diagnose.py`: A diagnostic script that checks the environment and dependencies.
*   `requirements.txt`: A file containing the required dependencies.
*   `src/`: A directory containing the source code for the application.
    *   `__init__.py`: An empty file indicating that the directory is a package.
    *   `llm_service.py`: A file containing the LLMService class that interacts with the Groq API.
    *   `repo_handler.py`: A file containing the RepoHandler class that processes GitHub repositories.

## Project Dependencies

The project depends on the following libraries:

*   `streamlit`: A library for building web applications.
*   `groq`: A library for interacting with the Groq API.
*   `gitpython`: A library for interacting with Git repositories.
*   `python-dotenv`: A library for loading environment variables from a `.env` file.
*   `pandas`: A library for data manipulation and analysis.
*   `requests`: A library for making HTTP requests.

Note: The project uses the `groq` library to interact with the Groq API, which requires a valid API key.