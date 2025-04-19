import requests
import json
import os
import pytest
from typing import Dict, Any
import time
import unittest

# API endpoint
BASE_URL = "http://localhost:8000"

class TestChatbotAPI(unittest.TestCase):
    def setUp(self):
        """Setup test case"""
        self.session_id = f"test_session_{int(time.time())}"
        
    def test_health_check(self):
        """Test health check endpoint"""
        response = requests.get(f"{BASE_URL}/health")
        data = response.json()
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["status"], "healthy")
        self.assertTrue("timestamp" in data)

    def test_initial_greeting(self):
        """Test initial greeting"""
        payload = {
            "query": "Hello",
            "session_id": self.session_id
        }
        response = requests.post(f"{BASE_URL}/chat", json=payload)
        data = response.json()
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue("reply" in data)
        self.assertTrue("Want help" in data["reply"])  # Check for greeting

    def test_product_inquiry(self):
        """Test product-related questions"""
        queries = [
            "What AI solutions do you offer?",
            "Tell me about your products",
            "What can your AI do?"
        ]
        
        for query in queries:
            payload = {
                "query": query,
                "session_id": self.session_id
            }
            response = requests.post(f"{BASE_URL}/chat", json=payload)
            data = response.json()
            
            self.assertEqual(response.status_code, 200)
            self.assertTrue("reply" in data)
            # Check for product-related keywords in response
            self.assertTrue(any(keyword in data["reply"].lower() 
                              for keyword in ["ai", "solution", "automation", "product"]))

    def test_pricing_inquiry(self):
        """Test pricing-related questions"""
        queries = [
            "How much does it cost?",
            "What are your pricing plans?",
            "Can I get a price quote?"
        ]
        
        for query in queries:
            payload = {
                "query": query,
                "session_id": self.session_id
            }
            response = requests.post(f"{BASE_URL}/chat", json=payload)
            data = response.json()
            
            self.assertEqual(response.status_code, 200)
            self.assertTrue("lead_intent" in data)
            self.assertTrue(data["lead_intent"])

    def test_human_request(self):
        """Test requests for human interaction"""
        queries = [
            "I want to speak with someone",
            "Can I talk to a human?",
            "Connect me with a representative"
        ]
        
        for query in queries:
            payload = {
                "query": query,
                "session_id": self.session_id
            }
            response = requests.post(f"{BASE_URL}/chat", json=payload)
            data = response.json()
            
            self.assertEqual(response.status_code, 200)
            self.assertTrue("human_requested" in data)
            self.assertTrue(data["human_requested"])
            self.assertTrue("hello@recogenie.com" in data["reply"].lower())  # Check for email instead of Calendly

    def test_lead_submission(self):
        """Test lead submission endpoint"""
        test_leads = [
            {
                "name": "John Doe",
                "email": "john@example.com",
                "interest": "AI Automation"
            },
            {
                "name": "Jane Smith",
                "email": "jane@example.com",
                "interest": "Custom Solutions"
            }
        ]
        
        for lead in test_leads:
            response = requests.post(f"{BASE_URL}/submit_lead", json=lead)
            data = response.json()
            
            self.assertEqual(response.status_code, 200)
            self.assertTrue("lead_collected" in data)
            self.assertTrue(data["lead_collected"])
            self.assertTrue("success" in data["status"])

    def test_conversation_memory(self):
        """Test conversation memory and context"""
        # First message
        payload1 = {
            "query": "What AI solutions do you offer?",
            "session_id": self.session_id
        }
        response1 = requests.post(f"{BASE_URL}/chat", json=payload1)
        
        # Follow-up question
        payload2 = {
            "query": "How much does the first one cost?",
            "session_id": self.session_id
        }
        response2 = requests.post(f"{BASE_URL}/chat", json=payload2)
        
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)
        self.assertTrue("lead_intent" in response2.json())

    def test_invalid_requests(self):
        """Test invalid requests and error handling"""
        # Test missing query
        payload = {
            "session_id": self.session_id
        }
        response = requests.post(f"{BASE_URL}/chat", json=payload)
        self.assertEqual(response.status_code, 422)  # Validation error

        # Test invalid lead submission
        invalid_lead = {
            "name": "Test User",
            # Missing email and interest
        }
        response = requests.post(f"{BASE_URL}/submit_lead", json=invalid_lead)
        self.assertEqual(response.status_code, 422)  # Validation error

def print_test_results(test_name: str, response: Dict[str, Any]) -> None:
    """Pretty print test results"""
    print(f"\n{'='*20} {test_name} {'='*20}")
    print(f"Status Code: {response.status_code}")
    print("Response:")
    print(json.dumps(response.json(), indent=2))
    print("="*50)

if __name__ == "__main__":
    unittest.main(verbosity=2) 