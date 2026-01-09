import streamlit as st
import os
import shutil
from src.repo_handler import process_repository
from src.llm_service import LLMService
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page Config
st.set_page_config(
    page_title="AutoDoc Pro",
    page_icon="📄",
    layout="wide"
)

# Initialize Session State
if "repo_url" not in st.session_state:
    st.session_state.repo_url = ""
if "readme_content" not in st.session_state:
    st.session_state.readme_content = ""
if "api_content" not in st.session_state:
    st.session_state.api_content = ""
if "history" not in st.session_state:
    st.session_state.history = []
if "theme" not in st.session_state:
    st.session_state.theme = "System"

# Theme Handler
def apply_theme():
    theme = st.session_state.theme
    if theme == "Dark":
        st.markdown("""
            <style>
                [data-testid="stAppViewContainer"] { background-color: #0E1117; color: white; }
                [data-testid="stSidebar"] { background-color: #262730; }
                [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 { color: white !important; }
                [data-testid="stHeader"] { background-color: #0E1117; }
                .main-header { color: white !important; font-size: 3rem; font-weight: 800; margin-bottom: 20px; }
            </style>
        """, unsafe_allow_html=True)
    elif theme == "Light":
        st.markdown("""
            <style>
                [data-testid="stAppViewContainer"] { background-color: #FFFFFF; color: black; }
                [data-testid="stSidebar"] { background-color: #F0F2F6; }
                [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 { color: black !important; }
                [data-testid="stHeader"] { background-color: #FFFFFF; }
                .main-header { color: #4B4B4B !important; font-size: 3rem; font-weight: 800; margin-bottom: 20px; }
            </style>
        """, unsafe_allow_html=True)

apply_theme()

st.markdown('<h1 class="main-header">📄 AutoDoc Pro - AI Documentation Generator</h1>', unsafe_allow_html=True)

# Callback to clear text
def clear_input():
    st.session_state.repo_url = ""
    st.session_state.readme_content = ""
    st.session_state.api_content = ""
    st.session_state.repo_input_widget = "" # Explicitly clear the widget state

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    
    # API Key
    try:
        if "GROQ_API_KEY" in st.secrets:
            api_key = st.secrets["GROQ_API_KEY"]
        else:
            api_key = st.text_input("Groq API Key", type="password", value=os.getenv("GROQ_API_KEY", ""))
            if not api_key:
                st.warning("Enter your Groq API Key to proceed")
    except Exception:
         api_key = st.text_input("Groq API Key", type="password", value=os.getenv("GROQ_API_KEY", ""))
         if not api_key:
            st.warning("Enter your Groq API Key.")

    # Model Selection
    model_option = st.selectbox(
        "Select Model",
        ("llama-3.3-70b-versatile", "llama-3.1-8b-instant")
    )
    # Restore the blue styled info box
    st.info("Supported Models: Llama 3.3, Llama 3.1 Instant")
    
    st.markdown("---")
    
    # History Section (moved up)
    st.subheader("📜 History")
    if st.session_state.history:
        # Inject CSS to style these specific buttons if possible, or just use primary type
        # Streamlit doesn't strictly allow reliable styling of specific buttons easily without ID hacks.
        # We will use type="primary" to match the orange Generate button as requested.
        for i, item in enumerate(reversed(st.session_state.history)):
            if i >= 5: break
            repo_name = item['url'].split('/')[-1]
            if st.button(f"📄 {repo_name}", key=f"hist_{i}", type="primary", use_container_width=True):
                st.session_state.repo_url = item['url']
                st.session_state.readme_content = item['readme']
                st.session_state.api_content = item['api']
                st.rerun()
    else:
        st.caption("No history yet.")
    
    st.markdown("---")
    
    # Theme Switcher (Icon based)
    st.subheader("🎨 Appearance")
    # Use columns for icons
    t_col1, t_col2, t_col3 = st.columns(3)
    with t_col1:
        if st.button("☀️", key="theme_light", help="Light Mode", use_container_width=True):
            st.session_state.theme = "Light"
            st.rerun()
    with t_col2:
        if st.button("🌙", key="theme_dark", help="Dark Mode", use_container_width=True):
            st.session_state.theme = "Dark"
            st.rerun()
    with t_col3:
        if st.button("🖥️", key="theme_system", help="System Default", use_container_width=True):
            st.session_state.theme = "System"
            st.rerun()
            
    # Show current theme status
    st.caption(f"Current: {st.session_state.theme}")

    st.markdown("---")
    st.caption("Created for Developer Productivity 🚀")

# Main Content
col_input, col_clear = st.columns([5, 1])
with col_input:
    # Key 'repo_input_widget' binds this to session state
    repo_url = st.text_input("🔗 Enter GitHub Repository URL", key="repo_input_widget")
    # Sync with manual input
    if repo_url != st.session_state.repo_url:
        st.session_state.repo_url = repo_url

with col_clear:
    st.write("")
    st.write("")
    st.button("Clear", on_click=clear_input)

generate_btn = st.button("Generate Docs", type="primary")

# Logic to Handle Generation
if generate_btn:
    if not api_key:
        st.error("Please provide a Groq API Key in the sidebar.")
    elif not st.session_state.repo_url:
        st.error("Please enter a GitHub repository URL.")
    else:
        try:
            with st.spinner("Processing repository..."):
                # Single step processing (In-Memory or Ephemeral)
                file_contents = process_repository(st.session_state.repo_url)
                
            if file_contents:
                with st.spinner("Analyzing codebase..."):
                    combined_content = ""
                    for file, content in file_contents.items():
                        combined_content += f"\nFile: {file}\n```\n{content}\n```\n"
                
                llm = LLMService(api_key=api_key)
                
                with st.spinner("Generating Documentation..."):
                    readme = llm.generate_documentation(combined_content, model_option, "readme")
                    api_doc = llm.generate_documentation(combined_content, model_option, "api_docs")
                    
                    st.session_state.readme_content = readme
                    st.session_state.api_content = api_doc
                    
                    # Update History
                    new_item = {'url': st.session_state.repo_url, 'readme': readme, 'api': api_doc}
                    st.session_state.history = [x for x in st.session_state.history if x['url'] != st.session_state.repo_url]
                    st.session_state.history.append(new_item)
            else:
                st.error("Failed to process repository. Please check the URL or try again.")
                
        except Exception as e:
            st.error(f"An error occurred: {e}")

# Display Results
if st.session_state.readme_content:
    tab1, tab2 = st.tabs(["📘 README.md", "📙 API Documentation"])
    
    def download_ui(content, base_filename, key_suffix):
        col1, col2 = st.columns([1, 1])
        with col1:
            format_choice = st.radio(f"Format", [".md", ".txt"], horizontal=True, label_visibility="collapsed", key=f"fmt_{key_suffix}")
        with col2:
            file_ext = format_choice
            mime_type = "text/markdown" if file_ext == ".md" else "text/plain"
            st.download_button(
                label=f"Download {base_filename}{file_ext}",
                data=content,
                file_name=f"{base_filename}{file_ext}",
                mime=mime_type,
                key=f"btn_{key_suffix}",
                use_container_width=True
            )

    with tab1:
        st.markdown(st.session_state.readme_content)
        st.divider()
        st.subheader("Download README")
        download_ui(st.session_state.readme_content, "README", "readme")
        
    with tab2:
        st.markdown(st.session_state.api_content)
        st.divider()
        st.subheader("Download API Docs")
        download_ui(st.session_state.api_content, "API_DOCS", "api")
