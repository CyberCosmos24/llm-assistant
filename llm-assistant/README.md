llm-assistant

Requirements
- Python 3.10 or newer
- Local Ollama server with the llama3.1 model

Setup
- Install dependencies: pip install -r requirements.txt

Usage
- Analyze logs: PYTHONPATH=src python cli/run.py analyze <path_to_log_file>
- Chat with the model: PYTHONPATH=src python cli/run.py chat
- Pull Cloudflare logs: PYTHONPATH=src python cli/run.py pull-cloudflare <zone_id> --api-token <token> [--start <ts> --end <ts> --limit <n> --analyze]
- Pull Wazuh alerts: PYTHONPATH=src python cli/run.py pull-wazuh <base_url> --username <user> --password <pass> [--limit <n> --verify-ssl/--no-verify-ssl --analyze]

Data
- Fetched Cloudflare logs are stored in data/cloudflare
- Fetched Wazuh alerts are stored in data/wazuh
