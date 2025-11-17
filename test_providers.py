#!/usr/bin/env python3
"""
Test script for LLM provider model listing functionality

This script tests that each provider:
1. Can fetch models from SDK APIs when real API keys are provided (primary method)
2. Falls back to config when API keys are invalid or API calls fail
3. Properly formats the model data structure
"""

import os
import sys
from typing import Dict, Any
from dotenv import load_dotenv

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from llmprovider.openai_provider import OpenAIProvider
from llmprovider.anthropic_provider import AnthropicProvider
from llmprovider.google_provider import GoogleProvider
from llmprovider.xai_provider import xAIProvider
from config import AVAILABLE_MODELS

load_dotenv()


class ProviderTester:
    """Test provider model listing functionality"""

    def __init__(self):
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

    def validate_model_structure(self, models: Dict[str, Any], provider_name: str) -> bool:
        """Validate the structure of returned models"""
        if not models:
            return False
        
        for model_id, model_info in models.items():
            required_fields = ['name', 'provider', 'endpoint', 'api_key_env']
            for field in required_fields:
                if field not in model_info:
                    print(f"   Missing field '{field}' in model {model_id}")
                    return False
            
            if model_info['provider'] != provider_name:
                print(f"   Provider mismatch in model {model_id}: expected {provider_name}, got {model_info['provider']}")
                return False
        
        return True

    def test_openai_provider(self):
        """Test OpenAI provider model listing"""
        self.print_header("Testing OpenAI Provider")
        
        # Test with dummy key (should fall back to config)
        print("\n1. Testing with dummy key (config fallback):")
        provider = OpenAIProvider("dummy_key", AVAILABLE_MODELS)
        models = provider.get_models()
        
        if len(models) > 0 and self.validate_model_structure(models, "OpenAI"):
            self.print_result(
                "OpenAI Config Fallback",
                True,
                f"Found {len(models)} models from config"
            )
            for model_id in list(models.keys())[:2]:
                print(f"   - {model_id}: {models[model_id]['name']}")
        else:
            self.print_result("OpenAI Config Fallback", False, "No models or invalid structure")
        
        # Test with real API key if available
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key:
            print("\n2. Testing with real API key (SDK call):")
            try:
                provider = OpenAIProvider(api_key, None)
                models = provider.get_models()
                
                if len(models) > 0 and self.validate_model_structure(models, "OpenAI"):
                    self.print_result(
                        "OpenAI SDK Call",
                        True,
                        f"Found {len(models)} models from API"
                    )
                    for model_id in list(models.keys())[:3]:
                        print(f"   - {model_id}: {models[model_id]['name']}")
                else:
                    self.print_result("OpenAI SDK Call", False, "No models or invalid structure")
            except Exception as e:
                self.print_result("OpenAI SDK Call", False, f"Error: {str(e)}")
        else:
            print("\n2. Skipping real API key test (OPENAI_API_KEY not set)")

    def test_anthropic_provider(self):
        """Test Anthropic provider model listing"""
        self.print_header("Testing Anthropic Provider")
        
        # Test with dummy key (should fall back to config)
        print("\n1. Testing with dummy key (config fallback):")
        provider = AnthropicProvider("dummy_key", AVAILABLE_MODELS)
        models = provider.get_models()
        
        if len(models) > 0 and self.validate_model_structure(models, "Anthropic"):
            self.print_result(
                "Anthropic Config Fallback",
                True,
                f"Found {len(models)} models from config"
            )
            for model_id in list(models.keys())[:2]:
                print(f"   - {model_id}: {models[model_id]['name']}")
        else:
            self.print_result("Anthropic Config Fallback", False, "No models or invalid structure")
        
        # Test with real API key if available
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if api_key:
            print("\n2. Testing with real API key (SDK call):")
            try:
                provider = AnthropicProvider(api_key, None)
                models = provider.get_models()
                
                if len(models) > 0 and self.validate_model_structure(models, "Anthropic"):
                    self.print_result(
                        "Anthropic SDK Call",
                        True,
                        f"Found {len(models)} models from API"
                    )
                    for model_id in list(models.keys())[:3]:
                        print(f"   - {model_id}: {models[model_id]['name']}")
                else:
                    self.print_result("Anthropic SDK Call", False, "No models or invalid structure")
            except Exception as e:
                self.print_result("Anthropic SDK Call", False, f"Error: {str(e)}")
        else:
            print("\n2. Skipping real API key test (ANTHROPIC_API_KEY not set)")

    def test_google_provider(self):
        """Test Google provider model listing"""
        self.print_header("Testing Google Provider")
        
        # Test with dummy key (should fall back to config)
        print("\n1. Testing with dummy key (config fallback):")
        provider = GoogleProvider("dummy_key", AVAILABLE_MODELS)
        models = provider.get_models()
        
        if len(models) > 0 and self.validate_model_structure(models, "Google"):
            self.print_result(
                "Google Config Fallback",
                True,
                f"Found {len(models)} models from config"
            )
            for model_id in list(models.keys())[:2]:
                print(f"   - {model_id}: {models[model_id]['name']}")
        else:
            self.print_result("Google Config Fallback", False, "No models or invalid structure")
        
        # Test with real API key if available
        api_key = os.getenv('GEMINI_API_KEY')
        if api_key:
            print("\n2. Testing with real API key (SDK call):")
            try:
                provider = GoogleProvider(api_key, None)
                models = provider.get_models()
                
                if len(models) > 0 and self.validate_model_structure(models, "Google"):
                    self.print_result(
                        "Google SDK Call",
                        True,
                        f"Found {len(models)} models from API"
                    )
                    for model_id in list(models.keys())[:3]:
                        print(f"   - {model_id}: {models[model_id]['name']}")
                else:
                    self.print_result("Google SDK Call", False, "No models or invalid structure")
            except Exception as e:
                self.print_result("Google SDK Call", False, f"Error: {str(e)}")
        else:
            print("\n2. Skipping real API key test (GEMINI_API_KEY not set)")

    def test_xai_provider(self):
        """Test xAI provider model listing"""
        self.print_header("Testing xAI Provider")
        
        # Test with dummy key (should fall back to config)
        print("\n1. Testing with dummy key (config fallback):")
        provider = xAIProvider("dummy_key", AVAILABLE_MODELS)
        models = provider.get_models()
        
        if len(models) > 0 and self.validate_model_structure(models, "xAI"):
            self.print_result(
                "xAI Config Fallback",
                True,
                f"Found {len(models)} models from config"
            )
            for model_id in list(models.keys())[:2]:
                print(f"   - {model_id}: {models[model_id]['name']}")
        else:
            self.print_result("xAI Config Fallback", False, "No models or invalid structure")
        
        # Test with real API key if available
        api_key = os.getenv('XAI_API_KEY')
        if api_key:
            print("\n2. Testing with real API key (SDK call):")
            try:
                provider = xAIProvider(api_key, None)
                models = provider.get_models()
                
                if len(models) > 0 and self.validate_model_structure(models, "xAI"):
                    self.print_result(
                        "xAI SDK Call",
                        True,
                        f"Found {len(models)} models from API"
                    )
                    for model_id in list(models.keys())[:3]:
                        print(f"   - {model_id}: {models[model_id]['name']}")
                else:
                    self.print_result("xAI SDK Call", False, "No models or invalid structure")
            except Exception as e:
                self.print_result("xAI SDK Call", False, f"Error: {str(e)}")
        else:
            print("\n2. Skipping real API key test (XAI_API_KEY not set)")

    def run_all_tests(self):
        """Run all provider tests"""
        self.print_header("LLM Provider Model Listing Tests")
        
        print("\nThis test verifies that:")
        print("1. All providers use SDK calls as the primary method when API keys are valid")
        print("2. All providers fall back to config when API calls fail or keys are invalid")
        print("3. All model data structures include required fields")
        
        self.test_openai_provider()
        self.test_anthropic_provider()
        self.test_google_provider()
        self.test_xai_provider()
        
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
        
        print("\n💡 Note: SDK API tests only run if API keys are configured in .env file")
        
        return self.failed_tests == 0


if __name__ == "__main__":
    tester = ProviderTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)
