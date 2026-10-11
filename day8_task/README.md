# Day 8 Task

## Run the project

Open this folder in VS Code and run these commands in the terminal:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Copy `.env.example` to `.env`, then edit the model settings if needed.

```powershell
python 1_ingest.py
python 2_search.py
python task_agent.py
```

To save the agent output:

```powershell
python task_agent.py > run_log.txt
```

Check the output and complete `results.md` using your own run.

Note: This is a fresh starter project based on the Day 8 task sheet. If your class lab has its own versions of the other handbook documents or configuration, use those files and keep `5_agentic_rag.py` unchanged as instructed.
