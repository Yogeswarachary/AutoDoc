**API Documentation for AutoDoc Pro**

**Overview**

AutoDoc Pro is a web-based AI documentation generator that uses the Groq API to generate high-quality documentation for GitHub repositories. The application is built using Streamlit and utilizes the GitPython library for cloning repositories.

**Key Modules and Classes**

### `LLMService`

The `LLMService` class is responsible for interacting with the Groq API to generate documentation.

*   **`__init__`**: Initializes the LLMService instance with the Groq API key.
*   **`generate_documentation`**: Generates documentation using the Groq API. Takes in the code context, model, and documentation type as input.

### `repo_handler`

The `repo_handler` module contains functions for processing GitHub repositories.

*   **`process_repository`**: Orchestrates the retrieval of repository content. Prioritizes Git clone (ephemeral) if available, otherwise falls back to ZIP download (in-memory).
*   **`_process_zip_in_memory`**: Downloads and processes a GitHub repository ZIP entirely in memory.
*   **`_get_file_contents_from_disk`**: Walks through a local directory and returns a dictionary of filename: content.
*   **`_should_ignore_dir`**: Determines if a directory should be ignored based on its name.
*   **`_should_ignore`**: Determines if a file should be ignored based on its extension or name.

### `app.py`

The `app.py` file contains the main application code.

*   **`st.set_page_config`**: Configures the Streamlit page settings.
*   **`apply_theme`**: Applies the theme to the application based on the user's selection.
*   **`clear_input`**: Clears the input fields and widgets.
*   **`generate_btn`**: Generates documentation when the "Generate Docs" button is clicked.
*   **`download_ui`**: Displays the generated documentation and provides a download button.

**API Endpoints**

The application exposes the following API endpoints:

*   **`/generate`**: Generates documentation for the specified repository.
*   **`/download`**: Downloads the generated documentation.

**Request and Response Formats**

The application uses JSON as the request and response format.

**Error Handling**

The application handles errors using try-except blocks. If an error occurs, an error message is displayed to the user.

**Security Considerations**

The application uses environment variables to store sensitive information, such as the Groq API key. The application also uses secure protocols (HTTPS) to communicate with the Groq API.

**API Documentation**

The following API documentation is available:

*   **`GET /generate`**: Generates documentation for the specified repository.
    *   **`repo_url`**: The URL of the GitHub repository.
    *   **`model`**: The LLM model to use.
    *   **`doc_type`**: The type of documentation to generate.
    *   **`Response`**: The generated documentation.
*   **`GET /download`**: Downloads the generated documentation.
    *   **`doc_type`**: The type of documentation to download.
    *   **`Response`**: The downloaded documentation.

**Example Use Cases**

1.  **Generating Documentation**:

    *   Send a `GET` request to `/generate` with the following parameters:
        *   `repo_url`: The URL of the GitHub repository.
        *   `model`: The LLM model to use.
        *   `doc_type`: The type of documentation to generate.
    *   The application will generate the documentation and return it in the response.
2.  **Downloading Documentation**:

    *   Send a `GET` request to `/download` with the following parameter:
        *   `doc_type`: The type of documentation to download.
    *   The application will download the documentation and return it in the response.