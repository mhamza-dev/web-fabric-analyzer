# Fabric Analyzer

A web-based fabric analysis tool.

## Setup

1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd web_fabric_analyzer
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running Locally

```bash
python app.py
```

## Deploying to Production (Render)

1. Set the Render start command to:
   ```bash
   gunicorn app:app
   ```
2. Make sure `requirements.txt` is present and includes `gunicorn`.

## Requirements
- Python 3.8+
- Flask
- Gunicorn

---

## License
MIT 