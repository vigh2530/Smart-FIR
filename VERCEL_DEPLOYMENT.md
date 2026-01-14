# Vercel Deployment Guide

## Prerequisites
- GitHub account (repo already pushed)
- Vercel account (free at https://vercel.com)
- Ollama service running (external or self-hosted)

## Deployment Steps

### Step 1: Connect GitHub Repository
1. Go to https://vercel.com
2. Click "New Project"
3. Select "Import Git Repository"
4. Authorize GitHub and select `Smart_FIR_Legal_AI_Ollama`
5. Click "Import"

### Step 2: Configure Environment
1. Set Build & Development Settings:
   - **Framework Preset**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Output Directory**: (leave empty)

2. Add Environment Variables:
   ```
   OLLAMA_HOST=http://your-ollama-server:11434
   ```

### Step 3: Deploy
Click "Deploy" - Vercel will:
- Install dependencies
- Build Python functions
- Deploy static frontend
- Provide HTTPS URL

### Step 4: Set Up External Ollama

**Option A: Railway (Recommended)**
1. Go to https://railway.app
2. Create new project
3. Deploy from GitHub
4. Add Ollama service:
   ```bash
   docker run -d -p 11434:11434 ollama/ollama
   ollama pull mistral
   ```
5. Get public URL and add to Vercel env vars

**Option B: Self-Hosted**
Deploy Ollama on your own server with public IP:
```bash
docker run -d -p 11434:11434 ollama/ollama
ollama pull mistral
ollama serve
```

## Architecture

```
┌─────────────────────────────────────────┐
│         Vercel (Frontend + API)         │
│  ┌──────────────────────────────────┐  │
│  │  public/index.html (UI)          │  │
│  │  api/analyze.py (Serverless)     │  │
│  │  api/health.py (Health Check)    │  │
│  └──────────────────────────────────┘  │
└────────────┬──────────────────────────┘
             │ HTTPS
             ▼
    ┌─────────────────────────┐
    │  External Ollama        │
    │  (Railway/Self-Hosted)  │
    └─────────────────────────┘
```

## Testing Locally

```bash
vercel env pull  # Get environment variables
vercel dev       # Run locally on localhost:3000
```

## Monitoring & Logs

1. Go to Vercel Dashboard
2. Select your project
3. View "Deployments" → "Functions" for logs
4. Check "Monitoring" for performance metrics

## Cost Estimate (Free Tier)

- **Vercel**: Free (12 serverless function invocations/day)
- **Railway**: Free tier available ($5/month after credits)
- **Ollama Server**: Depends on hosting

## Scaling to Production

For high traffic:
1. Upgrade Vercel to Pro ($20/month)
2. Use Railway paid plan
3. Add caching (Redis)
4. Enable CDN
5. Set up monitoring (Sentry, LogRocket)

## Troubleshooting

**Issue: "Ollama Error: Connection refused"**
→ Check OLLAMA_HOST environment variable

**Issue: "Function timed out"**
→ Increase timeout in vercel.json, optimize model

**Issue: "Out of memory"**
→ Use smaller model (gemma3:1b instead of mistral)
