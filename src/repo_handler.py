import os
import shutil
import requests
import zipfile
import io
import tempfile
from typing import Dict, Optional

try:
    import git
    GIT_AVAILABLE = True
except ImportError:
    GIT_AVAILABLE = False

def process_repository(repo_url: str) -> Dict[str, str]:
    """
    Orchestrates the retrieval of repository content.
    Prioritizes Git clone (ephemeral) if available, otherwise falls back to ZIP download (in-memory).
    
    Args:
        repo_url (str): The URL of the GitHub repository.
        
    Returns:
        Dict[str, str]: A dictionary where keys are relative file paths and values are file contents.
    """
    content = {}
    
    # 1. Try Git Clone (Ephemeral)
    if GIT_AVAILABLE:
        try:
            print(f"Attempting to clone {repo_url} using Git...")
            with tempfile.TemporaryDirectory() as temp_dir:
                git.Repo.clone_from(repo_url, temp_dir)
                print(f"Cloned to temporary directory: {temp_dir}")
                content = _get_file_contents_from_disk(temp_dir)
                print("Repo content read. Temporary directory will be auto-deleted.")
            return content
        except Exception as e:
            print(f"Git clone failed ({e}). Falling back to ZIP download.")
    else:
        print("Git is not available. Using ZIP download.")

    # 2. Fallback to ZIP download (In-Memory)
    try:
        content = _process_zip_in_memory(repo_url)
        if not content:
             print("Failed to process ZIP or empty repo.")
        return content
    except Exception as e:
         print(f"Error processing repository via ZIP: {e}")
         return {}

def _process_zip_in_memory(repo_url: str) -> Dict[str, str]:
    """
    Downloads and processes a GitHub repository ZIP entirely in memory.
    """
    file_contents = {}
    
    # Construct ZIP URL
    clean_url = repo_url[:-4] if repo_url.endswith(".git") else repo_url
    zip_url = f"{clean_url}/archive/refs/heads/main.zip"
    
    print(f"Downloading ZIP from {zip_url}...")
    try:
        response = requests.get(zip_url)
        if response.status_code == 404:
             zip_url = f"{clean_url}/archive/refs/heads/master.zip"
             print(f"main branch not found. Trying {zip_url}...")
             response = requests.get(zip_url)
        
        if response.status_code != 200:
            print(f"Failed to download ZIP. Status code: {response.status_code}")
            return {}
            
        print("ZIP downloaded. Extracting in memory...")
        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            for file_info in z.infolist():
                # Skip directories
                if file_info.is_dir():
                    continue
                
                # Get relative path (strip the root folder usually present in GitHub zips)
                # e.g., 'repo-main/src/main.py' -> 'src/main.py'
                parts = file_info.filename.split("/", 1)
                if len(parts) < 2: 
                    continue # Skip top level files if likely just metadata or weird structure
                
                relative_path = parts[1] # Use the path AFTER the root folder
                
                if _should_ignore(relative_path):
                    continue

                try:
                    with z.open(file_info) as f:
                        # Decode assuming utf-8, ignore errors for binaryish text
                        file_contents[relative_path] = f.read().decode('utf-8', errors='ignore')
                except Exception as e:
                     # print(f"Skipping file {relative_path}: {e}")
                     pass

        return file_contents

    except Exception as e:
        print(f"ZIP processing error: {e}")
        return {}

def _get_file_contents_from_disk(repo_path: str) -> Dict[str, str]:
    """
    Walks through a local directory and returns a dictionary of filename: content.
    Used for the Git clone strategy.
    """
    file_contents = {}
    for root, dirs, files in os.walk(repo_path):
        # Remove ignored directories in-place to prevent recursion
        dirs[:] = [d for d in dirs if not _should_ignore_dir(d)]
        
        for file in files:
            relative_path = os.path.relpath(os.path.join(root, file), repo_path)
            
            if _should_ignore(relative_path):
                continue
            
            file_path = os.path.join(root, file)
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    file_contents[relative_path] = f.read()
            except Exception as e:
                # print(f"Error reading file {file_path}: {e}")
                pass
                
    return file_contents

def _should_ignore_dir(dirname: str) -> bool:
    ignored_dirs = {
        'node_modules', '.git', '__pycache__', 'venv', 'env', '.idea', '.vscode', 
        'dist', 'build', 'target', 'bin', 'obj', 'lib'
    }
    return dirname in ignored_dirs

def _should_ignore(filepath: str) -> bool:
    """
    Determines if a file should be ignored based on extension or name.
    """
    filename = os.path.basename(filepath)
    ext = os.path.splitext(filename)[1].lower()
    
    ignored_files = {
        'package-lock.json', 'yarn.lock', '.gitignore', '.gitattributes', '.DS_Store'
    }
    
    ignored_extensions = {
        '.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico', 
        '.mp4', '.mov', '.avi', '.mp3', '.wav',
        '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
        '.zip', '.tar', '.gz', '.7z', '.rar',
        '.exe', '.dll', '.so', '.dylib', '.bin', '.pkl', '.pyc',
        '.jar', '.class', '.war'
    }
    
    if filename in ignored_files:
        return True
    if ext in ignored_extensions:
        return True
        
    return False
