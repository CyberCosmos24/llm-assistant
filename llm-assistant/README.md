Here is a **clean, professional README** that explains **exactly how to install the project and use the CLI on both Linux and Windows**.
Everything is plain-text Markdown so you can paste it directly into GitHub.

---

# **LLM Assistant – Installation & CLI Usage Guide**

The LLM Assistant is a local cybersecurity tool that analyzes Cloudflare and Wazuh security events using a self-hosted LLaMA model (via Ollama).
It is fully compatible with the **Cloudflare Free Plan** through the GraphQL Analytics API.

This guide explains **how to install the project** and **how to use the CLI** on Linux and Windows.

---

## **1. Requirements**

Before installing, make sure you have:

* Python **3.10 or newer**
* Pip
* Git
* Ollama installed locally with the `llama3.1` model
* A Cloudflare account (Free plan is supported)
* (Optional) Wazuh Manager with API access

---

# **2. Installation (Linux)**

### **Step 1 — Install Python & Git**

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv git -y
```

### **Step 2 — Install Ollama**

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Pull the model:

```bash
ollama pull llama3.1
```

### **Step 3 — Clone the repo**

```bash
git clone https://github.com/CyberCosmos24/llm-assistant
cd llm-assistant
```

### **Step 4 — Create virtual environment**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### **Step 5 — Install dependencies**

```bash
pip install -r requirements.txt
```

### **Step 6 — Create `.env` file**

```bash
nano .env
```

Add:

```
CLOUDFLARE_API_TOKEN=<your_token>
CF_ZONE_ID=<your_zone_id>
```

Save and exit.

### **Step 7 — Set Python path**

```bash
export PYTHONPATH=src
```

---

# **3. Installation (Windows)**

### **Step 1 — Install Python**

Download Python 3.10+ from:

[https://www.python.org/downloads/windows/](https://www.python.org/downloads/windows/)

During installation, enable:

**"Add python.exe to PATH"**

### **Step 2 — Install Ollama**

Download from:

[https://ollama.com/download](https://ollama.com/download)

Then pull the model:

```powershell
ollama pull llama3.1
```

### **Step 3 — Clone the repo**

```powershell
git clone https://github.com/CyberCosmos24/llm-assistant
cd llm-assistant
```

### **Step 4 — Create virtual environment**

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### **Step 5 — Install dependencies**

```powershell
pip install -r requirements.txt
```

### **Step 6 — Create `.env` file**

Create a file named `.env` in the project root with:

```
CLOUDFLARE_API_TOKEN=<your_token>
CF_ZONE_ID=<your_zone_id>
```

### **Step 7 — Set Python path**

```powershell
set PYTHONPATH=src
```

---

# **4. Using the CLI**

Once installed, activate your environment and set the path:

### Linux

```bash
source .venv/bin/activate
export PYTHONPATH=src
```

### Windows

```powershell
.venv\Scripts\activate
set PYTHONPATH=src
```

---

# **5. CLI Commands**

## **A. Chat with the model**

Opens an interactive shell using your local LLaMA model.

```bash
python cli/run.py chat
```

---

## **B. Analyze a log file**

Input can be JSON or JSONL.

```bash
python cli/run.py analyze <path_to_file>
```

Example:

```bash
python cli/run.py analyze data/logs/cloudflare/test.jsonl
```

---

## **C. Pull Cloudflare firewall events (Free Plan Compatible)**

```bash
python cli/run.py pull-cloudflare <zone_id> --api-token <token> \
  --start <timestamp> --end <timestamp> --limit <number> --analyze
```

If `.env` contains the values, you may omit:

* `<zone_id>`
* `--api-token`

Example (using .env):

```bash
python cli/run.py pull-cloudflare --limit 200 --analyze
```

---

## **D. Pull Wazuh alerts**

```bash
python cli/run.py pull-wazuh <base_url> \
  --username <user> --password <pass> --limit <n> --no-verify-ssl --analyze
```

Example:

```bash
python cli/run.py pull-wazuh https://10.0.0.50:55000 \
  --username wazuh --password mypass --no-verify-ssl --analyze
```

---

# **6. Log Storage Locations**

All saved logs are stored under:

```
data/
  logs/
    cloudflare/    -> Cloudflare firewall events (JSONL)
    wazuh/         -> Wazuh alerts (JSONL)
```

Everything is timestamped for easy review or re-analysis.

---

# **7. Cloudflare Free Plan Notes**

This tool **does not** use any Enterprise-only endpoints like:

* `/logs/received`
* Raw HTTP request logs
* Logpull API

Instead, it uses:

**GraphQL Analytics API**
Dataset: **firewallEventsAdaptive**

This dataset works on Free, Pro, and Business plans (with sampling and rate limits).

---

# **8. Automation (Linux)**

To pull Cloudflare logs every 12 hours:

Create a script:

```bash
nano pull_cloudflare.sh
```

Paste:

```bash
#!/bin/bash
cd /home/youruser/llm-assistant
source .venv/bin/activate
export PYTHONPATH=src

END=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
START=$(date -u -d "-6 hours" +"%Y-%m-%dT%H:%M:%SZ")

python cli/run.py pull-cloudflare --start $START --end $END --limit 200
```

Make executable:

```bash
chmod +x pull_cloudflare.sh
```

Add to cron:

```bash
crontab -e
```

Add:

```
0 */12 * * * /home/youruser/llm-assistant/pull_cloudflare.sh >> /home/youruser/llm-assistant/cron.log 2>&1
```




