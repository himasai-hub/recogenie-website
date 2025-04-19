import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # Server Configuration
    PORT = int(os.getenv("PORT", 8000))
    HOST = os.getenv("HOST", "0.0.0.0")
    
    # CORS Configuration
    ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")
    
    # Security
    ENABLE_DOCS = os.getenv("ENABLE_DOCS", "False").lower() == "true"
    
    # File Paths
    DOCS_DIR = "docs"
    LEADS_FILE = "leads.json"
    
    # Contact Information
    CONTACT_EMAIL = os.getenv("CONTACT_EMAIL", "hello@recogenie.com")
    
    # Model Configuration
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"
    CHAT_MODEL = "gpt-3.5-turbo"
    MAX_TOKENS = 300
    TEMPERATURE = 0.7 