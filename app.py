from flask import Flask
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Import blueprints
from routes.main import main_bp
from routes.api import api_bp
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),  # Logs to file
        logging.StreamHandler()  # Also logs to console
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Register blueprints
app.register_blueprint(main_bp)
app.register_blueprint(api_bp)


if __name__ == '__main__':
    # Check for API keys and provide helpful message
    print("\n" + "="*60)
    print("LLM Model Comparison Tool")
    print("="*60)
    
    api_keys_status = {
        'OpenAI': bool(os.getenv('OPENAI_API_KEY')),
        'Anthropic': bool(os.getenv('ANTHROPIC_API_KEY')),
        'Google': bool(os.getenv('GEMINI_API_KEY')),
        'xAI': bool(os.getenv('XAI_API_KEY'))
    }
    
    print("\nAPI Key Status:")
    for provider, has_key in api_keys_status.items():
        status = "✓ Configured" if has_key else "✗ Not configured"
        print(f"  {provider}: {status}")
    
    if not any(api_keys_status.values()):
        print("\n⚠️  No API keys configured. create a .env file with your API keys.")
        exit(1)

    print("\nStarting Flask server...")
    print("Access the app at: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
