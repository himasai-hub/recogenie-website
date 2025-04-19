import os
import json
import fitz  # PyMuPDF
import numpy as np
from typing import Dict, List, Optional
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import openai
from collections import defaultdict
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="RecoGenie Chatbot API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configure OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise ValueError("Please set OPENAI_API_KEY in .env file")

# Initialize sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Global variables
CHUNK_SIZE = 250  # tokens (approximate)
MAX_HISTORY = 5
LEADS_FILE = "leads.json"
CONTACT_EMAIL = os.getenv("CONTACT_EMAIL", "hello@recogenie.com")

# System message to restrict responses
SYSTEM_MESSAGE = """You are RecoGenie's AI assistant, powered by OpenAI. 
You must ONLY provide information that is contained in the provided context.
If you're unsure or the information isn't in the context, direct users to contact hello@recogenie.com.
Always maintain a professional and helpful tone.
End your responses with '- Powered by OpenAI' on a new line."""

# Initialize conversation memory
conversations = defaultdict(list)

class ChatInput(BaseModel):
    query: str
    session_id: Optional[str] = None

class LeadInfo(BaseModel):
    name: str
    email: str
    interest: str

# RAG System Implementation
class RAGSystem:
    def __init__(self):
        self.documents = []
        self.embeddings = None
        self.load_documents()
        self.build_index()

    def load_documents(self):
        """Load and process documents from the docs folder"""
        docs_dir = "docs"
        
        # Load PDF
        try:
            pdf_path = os.path.join(docs_dir, "Recogenie.pdf")
            if os.path.exists(pdf_path):
                doc = fitz.open(pdf_path)
                for page in doc:
                    self.documents.extend(self.chunk_text(page.get_text()))
        except Exception as e:
            print(f"Error loading PDF: {e}")

        # Load Markdown files
        for md_file in ["FAQ.md", "About.md"]:
            try:
                md_path = os.path.join(docs_dir, md_file)
                if os.path.exists(md_path):
                    with open(md_path, 'r') as f:
                        content = f.read()
                        self.documents.extend(self.chunk_text(content))
            except Exception as e:
                print(f"Error loading {md_file}: {e}")

    def chunk_text(self, text: str) -> List[str]:
        """Split text into chunks of approximately CHUNK_SIZE tokens"""
        words = text.split()
        chunks = []
        current_chunk = []
        current_size = 0

        for word in words:
            current_size += len(word.split())
            if current_size > CHUNK_SIZE:
                chunks.append(" ".join(current_chunk))
                current_chunk = [word]
                current_size = len(word.split())
            else:
                current_chunk.append(word)

        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks

    def build_index(self):
        """Build embeddings index from document chunks"""
        if not self.documents:
            print("Warning: No documents loaded")
            return

        # Create embeddings
        self.embeddings = model.encode(self.documents)

    def get_relevant_chunks(self, query: str, k: int = 3) -> List[str]:
        """Retrieve k most relevant chunks for the query"""
        if not self.embeddings is not None:
            return []

        # Get query embedding
        query_embedding = model.encode([query])[0]

        # Calculate similarities
        similarities = cosine_similarity([query_embedding], self.embeddings)[0]
        
        # Get top k indices
        top_indices = np.argsort(similarities)[-k:][::-1]
        
        # Return relevant chunks
        return [self.documents[i] for i in top_indices]

# Initialize RAG system
rag_system = RAGSystem()

def save_lead(lead_info: Dict):
    """Save lead information to JSON file"""
    try:
        leads = []
        if os.path.exists(LEADS_FILE):
            with open(LEADS_FILE, 'r') as f:
                leads = json.load(f)
        
        lead_info['timestamp'] = datetime.now().isoformat()
        leads.append(lead_info)
        
        with open(LEADS_FILE, 'w') as f:
            json.dump(leads, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving lead: {e}")
        return False

def detect_lead_intent(query: str) -> bool:
    """Detect if user shows buying intent"""
    buying_intent_phrases = [
        "price", "cost", "how much", "trial", "demo",
        "purchase", "buy", "get started", "sign up"
    ]
    return any(phrase in query.lower() for phrase in buying_intent_phrases)

def detect_human_request(query: str) -> bool:
    """Detect if user wants to talk to a human"""
    human_request_phrases = [
        "human", "person", "agent", "representative",
        "talk to someone", "speak with someone", "schedule",
        "call", "meeting", "support"
    ]
    return any(phrase in query.lower() for phrase in human_request_phrases)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/chat")
async def chat(chat_input: ChatInput):
    try:
        query = chat_input.query
        session_id = chat_input.session_id or "default"
        
        # Get conversation history
        history = conversations[session_id][-MAX_HISTORY:] if conversations[session_id] else []
        
        # Check for human request
        if detect_human_request(query):
            response = {
                "reply": f"I understand you'd like to speak with someone directly. You can reach our team at {CONTACT_EMAIL}. We typically respond within 24 hours.\n\nWould you like to continue chatting with me in the meantime?\n\n- Powered by OpenAI",
                "human_requested": True
            }
            return response

        # Check for buying intent
        if detect_lead_intent(query):
            response = {
                "reply": f"Great to hear your interest! To better assist you, please share:\n1. Your name\n2. Email address\n3. What specific solution interests you?\n\nOr you can email us directly at {CONTACT_EMAIL}\n\n- Powered by OpenAI",
                "lead_intent": True
            }
            return response

        # Get relevant context from RAG system
        relevant_chunks = rag_system.get_relevant_chunks(query)
        context = "\n".join(relevant_chunks)

        if not context:
            return {
                "reply": f"I apologize, but I can only provide information about RecoGenie's services and capabilities. For specific questions not covered in our documentation, please contact us at {CONTACT_EMAIL}.\n\n- Powered by OpenAI"
            }

        # Prepare messages for OpenAI
        messages = [
            {"role": "system", "content": SYSTEM_MESSAGE},
            {"role": "user", "content": f"Context:\n{context}\n\nUser Query: {query}"}
        ]

        # Add relevant history if available
        for msg in history[-2:]:  # Only include last 2 messages for context
            messages.append({"role": "user" if msg["role"] == "user" else "assistant", "content": msg["content"]})

        # Get response from OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=300,
            temperature=0.7,
            stop=None
        )

        # Extract and format the response
        chatbot_response = response.choices[0].message['content'].strip()
        if not chatbot_response.endswith("- Powered by OpenAI"):
            chatbot_response += "\n\n- Powered by OpenAI"

        # Update conversation history
        conversations[session_id].append({"role": "user", "content": query})
        conversations[session_id].append({"role": "assistant", "content": chatbot_response})

        return {"reply": chatbot_response}

    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        return {
            "reply": f"I apologize, but I encountered an error. Please contact our support team at {CONTACT_EMAIL} for assistance.\n\n- Powered by OpenAI"
        }

@app.post("/submit_lead")
async def submit_lead(lead_info: LeadInfo):
    """Endpoint to submit lead information"""
    lead_data = lead_info.dict()
    if save_lead(lead_data):
        return {
            "status": "success",
            "message": "Thank you! Our team will contact you shortly.",
            "lead_collected": True
        }
    else:
        raise HTTPException(status_code=500, detail="Failed to save lead information")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 