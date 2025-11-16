import unittest
import os
from app import app
from unittest.mock import patch

class NewEndpointTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('llmprovider.service.LLMService.get_available_models')
    def test_get_available_models_success(self, mock_get_models):
        """Test the /api/available_models endpoint with mocked data"""
        mock_get_models.return_value = {
            "gpt-3.5-turbo": {
                "name": "gpt-3.5-turbo",
                "provider": "OpenAI",
                "endpoint": "chat/completions"
            }
        }
        response = self.app.get('/api/available_models')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('gpt-3.5-turbo', data)
        self.assertEqual(data['gpt-3.5-turbo']['provider'], 'OpenAI')

    @patch('llmprovider.service.LLMService.get_available_models')
    def test_get_available_models_no_keys(self, mock_get_models):
        """Test the /api/available_models endpoint with no API keys"""
        mock_get_models.return_value = {}
        response = self.app.get('/api/available_models')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data, {})

if __name__ == '__main__':
    unittest.main()
