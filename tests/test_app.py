#!/usr/bin/env python3
"""
Test script for the LLM Comparison Flask app
"""

import requests
import json
import sys
import time
import os
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

class AppTester:
    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url
        self.passed_tests = 0
        self.failed_tests = 0
    
    def print_header(self, text: str):
        """Print a formatted header"""
        print(f"\n{'='*60}")
        print(f"{text:^60}")
        print(f"{'='*60}")
    
    def print_result(self, test_name: str, success: bool, details: str = ""):
        """Print test result"""
        icon = "✅" if success else "❌"
        status = "PASSED" if success else "FAILED"
        print(f"{icon} {test_name}: {status}")
        if details:
            print(f"   {details}")
        
        if success:
            self.passed_tests += 1
        else:
            self.failed_tests += 1
    
    def test_server_connection(self) -> bool:
        """Test if server is running"""
        try:
            response = requests.get(self.base_url, timeout=5)
            success = response.status_code == 200
            self.print_result(
                "Server Connection",
                success,
                f"Status code: {response.status_code}"
            )
            return success
        except requests.exceptions.ConnectionError:
            self.print_result(
                "Server Connection",
                False,
                "Could not connect. Is the Flask app running? (python app.py)"
            )
            return False
        except Exception as e:
            self.print_result("Server Connection", False, str(e))
            return False
    
    def test_health_endpoint(self):
        """Test health check endpoint"""
        try:
            response = requests.get(f"{self.base_url}/health")
            if response.status_code == 200:
                data = response.json()
                self.print_result(
                    "Health Check Endpoint",
                    True,
                    f"Models available: {data.get('models_available', 0)}"
                )
            else:
                self.print_result(
                    "Health Check Endpoint",
                    False,
                    f"Status code: {response.status_code}"
                )
        except Exception as e:
            self.print_result("Health Check Endpoint", False, str(e))
    
    def test_models_endpoint(self):
        """Test models endpoint"""
        try:
            response = requests.get(f"{self.base_url}/api/models")
            if response.status_code == 200:
                models = response.json()
                self.print_result(
                    "Models Endpoint",
                    True,
                    f"Found {len(models)} models"
                )
                
                # List models
                print("\n   Available models:")
                for model_id, info in models.items():
                    print(f"   - {info['name']} ({info['provider']})")
                    
                return models
            else:
                self.print_result(
                    "Models Endpoint",
                    False,
                    f"Status code: {response.status_code}"
                )
                return {}
        except Exception as e:
            self.print_result("Models Endpoint", False, str(e))
            return {}
    
    def test_compare_endpoint(self, models: Dict[str, Any]):
        """Test comparison endpoint"""
        if not models:
            print("\n   Skipping comparison test (no models available)")
            return
        
        # Check if API keys are configured
        api_keys_configured = any([
            os.getenv('OPENAI_API_KEY'),
            os.getenv('ANTHROPIC_API_KEY'),
            os.getenv('GOOGLE_API_KEY')
        ])
        
        # Select first model
        model_id = list(models.keys())[0]
        
        test_data = {
            "prompt": "What is the capital of France?",
            "model_id": model_id
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/api/get_model_response",
                json=test_data,
                headers={"Content-Type": "application/json"}
            )
            
            if not api_keys_configured:
                # Should return 503 if no API keys
                success = response.status_code == 503
                self.print_result(
                    "Comparison Endpoint - No API Keys",
                    success,
                    f"Status code: {response.status_code} (expected 503 without API keys)"
                )
            else:
                if response.status_code == 200:
                    result = response.json()
                    self.print_result(
                        "Comparison Endpoint",
                        True,
                        f"Got response from {result['model_name']}"
                    )
                    
                    # Show response details
                    print("\n   Response details:")
                    status_icon = "✓" if result['status'] == 'success' else "✗"
                    print(f"   {status_icon} {result['model_name']}: {result['status']}")
                else:
                    self.print_result(
                        "Comparison Endpoint",
                        False,
                        f"Status code: {response.status_code}"
                    )
        except Exception as e:
            self.print_result("Comparison Endpoint", False, str(e))
    
    def test_error_handling(self):
        """Test error handling"""
        # Test with empty prompt
        test_data = {
            "prompt": "",
            "model_id": "gpt-3.5-turbo"
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/api/get_model_response",
                json=test_data,
                headers={"Content-Type": "application/json"}
            )
            
            success = response.status_code == 400
            self.print_result(
                "Error Handling - Empty Prompt",
                success,
                f"Status code: {response.status_code}"
            )
        except Exception as e:
            self.print_result("Error Handling - Empty Prompt", False, str(e))
        
        # Test with no models
        test_data = {
            "prompt": "Test prompt",
            "model_id": None
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/api/get_model_response",
                json=test_data,
                headers={"Content-Type": "application/json"}
            )
            
            success = response.status_code == 400
            self.print_result(
                "Error Handling - No Models",
                success,
                f"Status code: {response.status_code}"
            )
        except Exception as e:
            self.print_result("Error Handling - No Models", False, str(e))
    
    def run_all_tests(self):
        """Run all tests"""
        self.print_header("LLM Comparison App Test Suite")
        
        # Check server connection first
        if not self.test_server_connection():
            print("\n⚠️  Cannot proceed with tests. Please start the Flask app first.")
            print("   Run: python app.py")
            return
        
        # Run other tests
        print("\n📋 Running tests...")
        
        self.test_health_endpoint()
        models = self.test_models_endpoint()
        self.test_compare_endpoint(models)
        self.test_error_handling()
        
        # Summary
        self.print_header("Test Summary")
        total_tests = self.passed_tests + self.failed_tests
        print(f"\nTotal Tests: {total_tests}")
        print(f"Passed: {self.passed_tests} ✅")
        print(f"Failed: {self.failed_tests} ❌")
        
        if self.failed_tests == 0:
            print("\n🎉 All tests passed!")
        else:
            print(f"\n⚠️  {self.failed_tests} test(s) failed.")
        
        print("\n💡 Note: Tests run in mock mode by default.")
        print("   To test with real APIs, add API keys to .env file")


if __name__ == "__main__":
    # Allow custom URL if provided
    url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:5000"
    
    tester = AppTester(url)
    tester.run_all_tests()
