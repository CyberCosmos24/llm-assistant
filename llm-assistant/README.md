llm-assistant

Requirements
- Python 3.10 or newer
- Local Ollama server with the llama3.1 model

Setup
- Install dependencies: pip install -r requirements.txt

Usage
- Analyze logs: PYTHONPATH=src python cli/run.py analyze <path_to_log_file>
- Chat with the model: PYTHONPATH=src python cli/run.py chat
