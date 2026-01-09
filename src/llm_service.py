import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class LLMService:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("Groq API Key is missing. Please set it in .env or pass it to the constructor.")
        self.client = Groq(api_key=self.api_key)

    def generate_documentation(self, context: str, model: str, doc_type: str) -> str:
        """
        Generates documentation using the Groq API.
        
        Args:
            context (str): The code or context to summarize.
            model (str): The LLM model to use (e.g., 'llama-3.3-70b-versatile').
            doc_type (str): The type of documentation ('readme', 'api_docs').
            
        Returns:
            str: The generated documentation.
        """
        
        prompts = {
            "readme": """
            You are an expert technical writer. 
            Generate a comprehensive README.md for the following codebase. 
            
            CRITICAL INSTRUCTION: 
            1. The FIRST line MUST be the actual Project Name as a top-level header (# Project Name). 
            2. Do NOT use generic headings like "Project Title & Description". 
            3. You MUST include a "Usage Examples" section with actual code blocks.
            
            Include sections for:
            - Key Features
            - Installation Instructions
            - Usage Examples (MUST include code blocks)
            - Project Structure (if apparent)
            
            Codebase Context:
            {context}
            
            Output strictly valid Markdown.
            """,
            
            "api_docs": """
            You are an expert technical writer.
            Generate detailed API Documentation or Developer Guide for the following codebase.
            Focus on explaining the key modules, classes, and functions.
            
            Codebase Context:
            {context}
            
            Output strictly valid Markdown.
            """
        }
        
        prompt_template = prompts.get(doc_type, prompts["readme"])
        formatted_prompt = prompt_template.format(context=context[:60000]) # Example truncation to avoid context limits
        
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": formatted_prompt,
                    }
                ],
                model=model,
                temperature=0.5,
                max_tokens=4096,
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            return f"Error generating documentation: {e}"
