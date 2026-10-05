# Day 6 Lab — Robust Function Calling

Files:
- `tools_v2.py` — strict tool schemas and safe calculator
- `validate.py` — argument validation
- `robust_agent.py` — OpenAI-compatible agent with retries and guards
- `inject_faults.py` — deterministic fault-injection tests
- `structured_demo.py` — free text vs JSON vs strict schema output
- `config.py` — provider/model configuration
- `.env.example` — configuration template

## Setup

```bash
python -m venv .venv
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and configure your provider.

## Run

```bash
python validate.py
python inject_faults.py
python robust_agent.py
python structured_demo.py
```

`validate.py` and `inject_faults.py` can run without a model. The agent and structured-output demo require a working OpenAI-compatible provider.

## Expected lab evidence

The fault injector contains the manual's required faults plus two student-added faults. It should finish all cases without an exception. The robust agent should return recoverable messages for malformed calls, retry a truncated response, stop repeated identical failures, and append one tool result for each tool call ID.
