#!/usr/bin/env python3
"""
Basic integration tests for CI/CD pipeline
"""

import requests
import json
import time
import sys

def test_health_endpoint():
    """Test the health endpoint."""
    try:
        response = requests.get('http://localhost:5001/health', timeout=5)
        print(f'Health check status: {response.status_code}')
        return response.status_code == 200
    except Exception as e:
        print(f'Health check failed: {e}')
        return False

def test_chat_endpoint():
    """Test the chat endpoint."""
    try:
        response = requests.post('http://localhost:5000/chat', 
                               json={'prompt': 'Hello'}, 
                               timeout=10)
        print(f'Chat test status: {response.status_code}')
        return response.status_code == 200
    except Exception as e:
        print(f'Chat test failed: {e}')
        return False

def main():
    """Main test function."""
    print("Starting basic integration tests...")
    
    # Wait for services to be ready
    time.sleep(10)
    
    # Run tests
    health_ok = test_health_endpoint()
    chat_ok = test_chat_endpoint()
    
    if health_ok and chat_ok:
        print("✅ All basic tests passed!")
        sys.exit(0)
    else:
        print("❌ Some tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    main() 