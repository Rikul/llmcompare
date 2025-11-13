# Quick Start Guide - LLM Model Comparison Tool

## 🚀 Getting Started

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Create .env file (optional):**
   ```bash
   cp .env.example .env
   ```
   
   Then add your API keys:
   ```
   OPENAI_API_KEY=sk-...
   ANTHROPIC_API_KEY=sk-ant-...
   GOOGLE_API_KEY=AIza...
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```

4. **Open your browser:**
   Navigate to http://localhost:5000

## 🎯 First Steps

### Without API Keys (Mock Mode)
The app automatically runs in mock mode when no API keys are configured. Perfect for:
- Testing the UI
- Understanding the workflow
- Development and debugging

### With API Keys
Once you add API keys to the `.env` file, the app will automatically use real API calls.

## 📝 Features at a Glance

- ✅ Compare multiple LLMs with one prompt
- ✅ Interactive tabbed interface
- ✅ Copy responses with one click
- ✅ Modern, responsive design
- ✅ Automatic mock mode fallback
- ✅ Comprehensive error handling

## 🔧 Configuration

The app will show API key status on startup:
```
API Key Status:
  OpenAI: ✓ Configured
  Anthropic: ✗ Not configured
  Google: ✗ Not configured
```

## 🆘 Troubleshooting

### Port already in use?
Change the port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Change to any available port
```

### Module not found?
Make sure you've installed dependencies:
```bash
pip install -r requirements.txt
```

### API errors?
- Check your API keys in `.env`
- Verify your API account has credits
- Check the console for detailed error messages

## 🚀 Quick Test

Use the test script to verify everything works:
```bash
python test_app.py
```

## 📚 Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check [CUSTOM_MODELS_EXAMPLE.md](CUSTOM_MODELS_EXAMPLE.md) to add new models
- Explore the code to understand the architecture