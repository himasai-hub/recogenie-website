import requests
import json
import os
from typing import Dict, Any
import time

# API endpoint
BASE_URL = "http://localhost:8000"

def print_response(response: Dict[str, Any]) -> None:
    """Pretty print the chatbot response"""
    print("\nResponse:")
    print("=" * 50)
    if isinstance(response, dict):
        for key, value in response.items():
            print(f"{key}: {value}")
    else:
        print(response)
    print("=" * 50 + "\n")

def test_health():
    """Test the health check endpoint"""
    print("\nTesting health check endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print_response(response.json())

def test_chat(query: str, session_id: str = None):
    """Test the chat endpoint"""
    print(f"\nTesting chat with query: '{query}'")
    
    payload = {
        "query": query,
        "session_id": session_id or "test_session"
    }
    
    response = requests.post(f"{BASE_URL}/chat", json=payload)
    print_response(response.json())
    return response.json()

def test_lead_submission(name: str, email: str, interest: str):
    """Test the lead submission endpoint"""
    print("\nTesting lead submission...")
    
    payload = {
        "name": name,
        "email": email,
        "interest": interest
    }
    
    response = requests.post(f"{BASE_URL}/submit_lead", json=payload)
    print_response(response.json())

def run_conversation_flow():
    """Test a complete conversation flow"""
    session_id = "test_session_" + str(int(time.time()))
    
    # Test 1: Initial greeting
    print("\n1. Testing initial greeting...")
    test_chat("Hi", session_id)
    
    # Test 2: Product inquiry
    print("\n2. Testing product inquiry...")
    test_chat("What AI solutions do you offer?", session_id)
    
    # Test 3: Pricing inquiry (should trigger lead collection)
    print("\n3. Testing pricing inquiry...")
    test_chat("How much does it cost?", session_id)
    
    # Test 4: Submit lead information
    print("\n4. Testing lead submission...")
    test_lead_submission(
        name="Test User",
        email="test@example.com",
        interest="AI Automation Solution"
    )
    
    # Test 5: Request human interaction
    print("\n5. Testing human interaction request...")
    test_chat("I want to speak with a human", session_id)
    
    # Test 6: Technical question
    print("\n6. Testing technical question...")
    test_chat("How does your technology work?", session_id)

if __name__ == "__main__":
    # First, test health endpoint
    test_health()
    
    # Then run through conversation flow
    run_conversation_flow() 