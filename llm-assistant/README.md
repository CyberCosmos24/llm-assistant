LLM Assistant

Windows installation
1. Install Python 3.10 or newer from https://www.python.org/downloads/windows/. Enable "Add python.exe to PATH" during setup.
2. Open Windows Terminal or PowerShell.
3. Clone the repository and enter the project directory.
4. Install dependencies: pip install -r requirements.txt
5. Ensure Ollama is running locally with the llama3.1 model available.

Environment configuration
1. Create a .env file in the project root.
2. Add your Cloudflare credentials:
   CLOUDFLARE_API_TOKEN=<your_api_token>
   CF_ZONE_ID=<your_zone_id>
3. If you prefer CLI flags, you can still pass --api-token and the positional zone ID instead of using the .env values.

Running the CLI on Windows
1. From the project root, run commands with the src folder on PYTHONPATH:
   set PYTHONPATH=src
   python cli/run.py <command> [options]
2. Analyze logs:
   python cli/run.py analyze <path_to_log_file>
3. Chat with the model:
   python cli/run.py chat
4. Pull Cloudflare firewall events and optionally analyze them:
   python cli/run.py pull-cloudflare <zone_id> --api-token <token> [--start <ts> --end <ts> --limit <n> --analyze]
   If CF_ZONE_ID and CLOUDFLARE_API_TOKEN are set in .env, you can omit the zone_id and --api-token values.
5. Pull Wazuh alerts:
   python cli/run.py pull-wazuh <base_url> --username <user> --password <pass> [--limit <n> --verify-ssl/--no-verify-ssl --analyze]

Data locations
- Cloudflare events are saved to data/logs/cloudflare as JSONL files.
- Wazuh alerts are saved to data/wazuh as JSONL files.
