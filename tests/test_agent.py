import pytest
import json
from unittest.mock import Mock, patch
import sys
import os

# Add the parent directory to the path to import the agent module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.app import app

@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

class TestChatEndpoint:
    """Test cases for the /chat endpoint."""
    
    @patch('agent.app.openai.ChatCompletion.create')
    def test_chat_success(self, mock_openai, client):
        """Test successful chat request."""
        # Mock OpenAI response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Hello! I am Assistant."
        mock_openai.return_value = mock_response
        
        # Make request
        response = client.post('/chat', 
                             json={'prompt': 'Hello, what is your name?'})
        
        # Assertions
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'answer' in data
        assert data['answer'] == "Hello! I am Assistant."
        
    def test_chat_missing_prompt(self, client):
        """Test chat request without prompt."""
        response = client.post('/chat', json={})
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'answer' in data
        
    def test_chat_empty_prompt(self, client):
        """Test chat request with empty prompt."""
        response = client.post('/chat', json={'prompt': ''})
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'answer' in data

class TestLogsEndpoint:
    """Test cases for the /logs endpoint."""
    
    @patch('agent.app.get_weaviate_client')
    @patch('agent.app.openai.Embedding.create')
    @patch('agent.app.openai.ChatCompletion.create')
    def test_logs_analysis_success(self, mock_chat, mock_embedding, mock_weaviate, client):
        """Test successful log analysis request."""
        # Mock Weaviate client
        mock_client = Mock()
        mock_query = Mock()
        mock_near_vector = Mock()
        mock_limit = Mock()
        
        # Set up the chain of mock calls
        mock_client.query = mock_query
        mock_query.get.return_value = mock_near_vector
        mock_near_vector.with_near_vector.return_value = mock_limit
        mock_limit.with_limit.return_value = mock_limit
        mock_limit.do.return_value = {
            'data': {
                'Get': {
                    'LogEntry': [
                        {'message': 'Error: Service failed', 'timestamp': '2025-01-01 10:00:00'},
                        {'message': 'Warning: High memory usage', 'timestamp': '2025-01-01 10:01:00'}
                    ]
                }
            }
        }
        mock_weaviate.return_value = mock_client
        
        # Mock OpenAI embedding response
        mock_embedding.return_value = {
            'data': [
                {
                    'embedding': [0.1, 0.2, 0.3]
                }
            ]
        }
        
        # Mock OpenAI chat response
        mock_chat_response = Mock()
        mock_chat_response.choices = [Mock()]
        mock_chat_response.choices[0].message.content = "Analysis shows errors in the service."
        mock_chat.return_value = mock_chat_response
        
        # Make request
        response = client.post('/logs', 
                             json={'question': 'Why did the service crash?'})
        
        # Assertions
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'analysis' in data
        assert data['analysis'] == "Analysis shows errors in the service."
        
    def test_logs_missing_question(self, client):
        """Test logs request without question."""
        response = client.post('/logs', json={})
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'analysis' in data
        assert 'Log analysis unavailable' in data['analysis']
        
    def test_logs_empty_question(self, client):
        """Test logs request with empty question."""
        response = client.post('/logs', json={'question': ''})
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'analysis' in data

class TestHealthCheck:
    """Test cases for basic health checks."""
    
    def test_health_check(self, client):
        """Test that the app is running."""
        response = client.get('/')
        
        # Should return 404 for root, but app should be running
        assert response.status_code == 404
        
    def test_invalid_endpoint(self, client):
        """Test invalid endpoint returns 404."""
        response = client.get('/invalid')
        
        assert response.status_code == 404

if __name__ == '__main__':
    pytest.main([__file__]) 