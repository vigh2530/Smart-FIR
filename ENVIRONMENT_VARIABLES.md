# How to Add Environment Variables

## Method 1: Local Development (.env file)

### Step 1: Copy the template
```bash
cp .env.example .env
```

### Step 2: Edit .env file
```bash
# Windows (PowerShell)
notepad .env

# Linux/Mac
nano .env
```

### Step 3: Add your values
```
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=mistral
API_TIMEOUT=120
API_PORT=8501
DEBUG=False
```

### Step 4: Test locally
```bash
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('OLLAMA_HOST'))"
```

---

## Method 2: Vercel Deployment

### Step 1: Via Vercel Dashboard
1. Go to **Vercel Dashboard** → Your Project
2. Click **Settings** → **Environment Variables**
3. Add new variable:
   - **Name**: `OLLAMA_HOST`
   - **Value**: `http://your-ollama-server:11434`
4. Click "Add"
5. Repeat for other variables

### Step 2: Via Vercel CLI
```bash
# Install Vercel CLI
npm i -g vercel

# Link to your project
vercel link

# Add environment variable
vercel env add OLLAMA_HOST
# Follow prompts to enter value

# Deploy with new variables
vercel deploy
```

### Step 3: Via vercel.json (Advanced)
```json
{
  "env": {
    "OLLAMA_HOST": "@ollama_host",
    "API_TIMEOUT": "120"
  }
}
```

---

## Method 3: Docker Deployment

### Using docker-compose.yml
```yaml
services:
  app:
    environment:
      - OLLAMA_HOST=http://ollama:11434
      - OLLAMA_MODEL=mistral
      - API_TIMEOUT=120
      - DEBUG=false
```

### Using Docker run
```bash
docker run -e OLLAMA_HOST=http://ollama:11434 \
           -e OLLAMA_MODEL=mistral \
           -p 8501:8501 \
           fir-app
```

---

## Method 4: GitHub Secrets (for CI/CD)

### Step 1: Add to GitHub Secrets
1. Go to **GitHub Repository** → **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Add variables:
   - Name: `OLLAMA_HOST`
   - Value: `http://your-server:11434`

### Step 2: Use in GitHub Actions
Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy

on: [push]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Vercel
        env:
          OLLAMA_HOST: ${{ secrets.OLLAMA_HOST }}
          VERCEL_TOKEN: ${{ secrets.VERCEL_TOKEN }}
        run: vercel deploy --prod
```

---

## Common Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `OLLAMA_HOST` | Ollama server URL | `http://localhost:11434` |
| `OLLAMA_MODEL` | Model to use | `mistral`, `gemma3:1b`, `llama2` |
| `API_TIMEOUT` | Request timeout (seconds) | `120` |
| `API_PORT` | Streamlit port | `8501` |
| `DEBUG` | Enable debug mode | `True`, `False` |
| `LOG_LEVEL` | Logging level | `INFO`, `DEBUG`, `WARNING` |

---

## Testing Environment Variables

### Python Script
```python
import os
from dotenv import load_dotenv

load_dotenv()

ollama_host = os.getenv("OLLAMA_HOST")
ollama_model = os.getenv("OLLAMA_MODEL", "mistral")  # With default

print(f"Ollama Host: {ollama_host}")
print(f"Model: {ollama_model}")
```

### Command Line
```bash
# Windows
echo %OLLAMA_HOST%

# Linux/Mac
echo $OLLAMA_HOST
```

---

## Security Best Practices

✅ **DO:**
- Store sensitive data in `.env` file
- Add `.env` to `.gitignore`
- Use strong credentials for production
- Rotate API keys regularly
- Use environment variables for all config

❌ **DON'T:**
- Commit `.env` file to GitHub
- Hardcode secrets in code
- Share `.env` files via email
- Use same credentials for dev/prod

---

## Vercel Specific Setup

### For Vercel Deployment:
```bash
# 1. Create .env.local (ignored by Vercel)
cp .env.example .env.local

# 2. Set values for local testing
# OLLAMA_HOST=http://localhost:11434

# 3. In Vercel Dashboard, set production env vars:
# OLLAMA_HOST=http://your-production-ollama:11434

# 4. Deploy
vercel deploy --prod
```

### Multiple Environments
```
.env.local          (development - git ignored)
.env.production     (production values - git ignored)
vercel.json         (public config - commited)
```

---

## Troubleshooting

**Issue: "Environment variable not found"**
```python
# Add debug info
import os
print("Available env vars:", list(os.environ.keys()))
```

**Issue: ".env file not loading"**
```bash
# Ensure python-dotenv is installed
pip install python-dotenv

# Check file exists and is in correct location
ls -la .env
```

**Issue: Different values in Vercel vs Local**
- Check Vercel Dashboard for override variables
- Use `vercel env pull` to sync local variables
- Restart Vercel deployment after changes
