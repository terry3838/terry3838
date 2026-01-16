# Logging Mission (FastAPI)

## Setup

```bash
cd mission-logging
uv venv --python 3.12
source .venv/bin/activate
uv pip install -r requirements.txt
```

## Run

```bash
uvicorn main:app --reload
```

## Verify Logging

- Log file path: `logs/app.log`
- File rotation: `logs/app.log.1`, `logs/app.log.2`, ... (size-based)

```bash
curl http://127.0.0.1:8000/
curl http://127.0.0.1:8000/logs/demo

# Check file output
tail -n 50 logs/app.log
```

### Rotation test (optional)

```bash
for i in {1..200}; do curl -s http://127.0.0.1:8000/logs/demo > /dev/null; done
ls -l logs/
```

## What to capture for the mission
- Screenshot showing the log file exists and new entries are appended after API calls.
- Screenshot showing console output while requests are made.
- Push this folder to your GitHub repository.
