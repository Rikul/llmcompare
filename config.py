"""
Configuration file for LLM Model Comparison Tool

NOTE: Model configurations have been moved to their respective provider files.
- OpenAI models: llmprovider/openai_provider.py
- Anthropic models: llmprovider/anthropic_provider.py
- Google models: llmprovider/google_provider.py
- xAI models: llmprovider/xai_provider.py

This allows for easier maintenance as each provider manages its own model versions.
To update model versions, edit the get_models() method in the respective provider file.
"""

# This file is kept for any future application-wide configuration needs
# Model configurations are now handled directly in provider files
