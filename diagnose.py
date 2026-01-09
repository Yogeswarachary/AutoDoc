import sys
import os

print("Checking environment...")

try:
    import streamlit
    print("Streamlit imported successfully.")
except ImportError as e:
    print(f"Error importing streamlit: {e}")

try:
    import git
    print(f"GitPython imported successfully. Version: {git.__version__}")
    try:
        git.Repo.init("test_repo_check")
        print("Git executable found and working.")
        import shutil
        shutil.rmtree("test_repo_check")
    except Exception as e:
        print(f"Error using Git (git executable might be missing): {e}")
except ImportError as e:
    print(f"Error importing git: {e}")

try:
    from src.repo_handler import clone_repo, get_file_contents
    print("src.repo_handler imported successfully.")
except Exception as e:
    print(f"Error importing src.repo_handler: {e}")

try:
    from src.llm_service import LLMService
    print("src.llm_service imported successfully.")
except Exception as e:
    print(f"Error importing src.llm_service: {e}")

print("Diagnostics complete.")
