# LLM Assistant

A simple, modular assistant powered by large language models (LLMs) for natural language tasks, automation, and integration with various APIs.

## Features

- **Modular Design**: Easily extendable with custom plugins and tools.
- **LLM Integration**: Supports popular models like GPT, Llama, and Grok via APIs.
- **Task Automation**: Handles conversations, code generation, and data analysis.
- **Lightweight**: Minimal dependencies for quick setup and deployment.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/CyberCosmos24/llm-assistant.git
   cd llm-assistant
   ```

2. Install dependencies (Python 3.8+ required):
   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   - Create a `.env` file in the root directory.
   - Add your API keys (e.g., `OPENAI_API_KEY=your_key_here`).

## Usage

### Quick Start

Run the assistant in interactive mode:
```
python main.py
```

Example interaction:
```
User: What is the capital of France?
Assistant: The capital of France is Paris.
```

### API Integration

To integrate with external services:
```python
from llm_assistant import Assistant

assistant = Assistant(model="gpt-3.5-turbo")
response = assistant.query("Summarize this text: [your text here]")
# LLM Assistant  
A fully offline-capable cybersecurity assistant that works **exclusively with Cloudflare’s Free tier** and local LLaMA models.

## Description
Local security event analyzer designed for users on Cloudflare’s Free plan.  
It pulls firewall events using the publicly available GraphQL Analytics API (firewallEventsAdaptive dataset – the only firewall log source accessible on the Free tier), optionally combines them with Wazuh alerts, normalizes everything to JSONL, and lets a self-hosted LLaMA 3.1 model (via Ollama) summarize threats, classify attacks, and recommend fixes — all without sending any data to third-party clouds.

## Key Features
- 100% compatible with Cloudflare Free tier (no paid features or Logpull required)  
- Pulls firewall events via the official GraphQL Analytics API  
- Optional integration with Wazuh alerts through its REST API  
- Normalizes logs to clean JSONL format  
- Runs analysis completely locally using Ollama + LLaMA 3.1 (70B or 8B)  
- Interactive CLI for chatting with the model and running one-click workflows  
- Zero data leaves your machine after logs are downloaded  

## Requirements
- Python 3.10 or newer  
- Ollama installed with the llama3.1 model (`ollama pull llama3.1`)  
- Cloudflare Free tier account (a Zone ID and API token with Zone Analytics read permission)  
- Optional: Wazuh manager with API access  

## Quick Installation
```bash
git clone https://github.com/CyberCosmos24/llm-assistant.git
cd llm-assistant
pip install -r requirements.txt

# Start Ollama (run in background or use the desktop app)
ollama serve &
ollama pull llama3.1
```

## Configuration (.env)
Create a `.env` file in the project root (optional – you can also use CLI flags):
```
CLOUDFLARE_API_TOKEN=your_token_here
CF_ZONE_ID=your_zone_id_here
```

## Usage Examples
```bash
# Interactive chat with the local model
python cli/run.py chat

# Pull the last 500 firewall events from your Free tier zone and auto-analyze
python cli/run.py pull-cloudflare --start "2025-11-01T00:00:00Z" --limit 500 --analyze

# Analyze an already downloaded log file
python cli/run.py analyze data/logs/cloudflare/latest_events.jsonl
```

All logs are saved with timestamps under:
- `data/logs/cloudflare/`
- `data/logs/wazuh/` (if used)

## Why It Works on Free Tier Only
This project deliberately avoids every Cloudflare endpoint that requires a paid plan:
- No Logpull  
- No /zones/:id/logs/received  
- No raw HTTP request logs  

It relies solely on the GraphQL `firewallEventsAdaptive` dataset, which is available on every Cloudflare plan, including Free.



