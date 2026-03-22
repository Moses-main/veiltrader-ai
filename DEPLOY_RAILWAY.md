# Railway Deployment Guide

This guide walks you through deploying VeilTrader AI on Railway.

## Prerequisites

1. Railway account (https://railway.app)
2. GitHub account connected to Railway
3. Your API keys ready

---

## Option 1: Deploy from GitHub (Recommended)

### Step 1: Push Code to GitHub
Make sure your code is pushed to GitHub (already done).

### Step 2: Connect Railway to GitHub
1. Go to https://railway.app
2. Click **New Project** → **Deploy from GitHub repo**
3. Select `veiltrader-ai` repository
4. Railway will auto-detect Python

### Step 3: Add Environment Variables

In Railway dashboard, go to **Variables** tab and add:

| Variable | Value |
|----------|-------|
| `BASE_NETWORK` | `sepolia` |
| `GROQ_API_KEY` | YOUR_GROQ_API_KEY |
| `BANKR_API_KEY` | YOUR_BANKR_API_KEY |
| `WALLET_ADDRESS` | YOUR_WALLET_ADDRESS |
| `PRIVATE_KEY` | YOUR_PRIVATE_KEY |
| `UNISWAP_API_KEY` | YOUR_UNISWAP_API_KEY |
| `DEMO_MODE` | `false` |
| `EMERGENCY_STOP` | `false` |
| `LIDO_MODE` | `false` |

### Step 4: Set Start Command

In Railway, go to **Settings** → **Start Command**:
```
python main.py
```

### Step 5: Deploy
Click **Deploy** - Railway will build and deploy automatically.

---

## Option 2: Deploy via Railway CLI

### Step 1: Install Railway CLI
```bash
npm install -g @railway/cli
```

### Step 2: Login
```bash
railway login
```

### Step 3: Initialize Project
```bash
cd veiltrader-ai
railway init
```

### Step 4: Add Variables
```bash
railway variables set BASE_NETWORK=sepolia
railway variables set GROQ_API_KEY=YOUR_GROQ_API_KEY
railway variables set BANKR_API_KEY=YOUR_BANKR_API_KEY
railway variables set WALLET_ADDRESS=YOUR_WALLET_ADDRESS
railway variables set PRIVATE_KEY=YOUR_PRIVATE_KEY
railway variables set UNISWAP_API_KEY=YOUR_UNISWAP_API_KEY
railway variables set DEMO_MODE=false
railway variables set EMERGENCY_STOP=false
railway variables set LIDO_MODE=false
```

### Step 5: Deploy
```bash
railway up
```

### Step 6: Get URL
```bash
railway domain
```

---

## Option 3: Deploy on Render

### Step 1: Create render.yaml
Already included in repository.

### Step 2: Connect GitHub
1. Go to https://render.com
2. Click **New** → **Blueprint**
3. Connect GitHub repo

### Step 3: Environment Variables
Same variables as Railway above.

### Step 4: Set Start Command
```
python main.py
```

---

## Option 4: Deploy on Fly.io

### Step 1: Install Fly CLI
```bash
curl -L https://fly.io/install.sh | sh
```

### Step 2: Launch
```bash
cd veiltrader-ai
fly launch
```

### Step 3: Set Secrets
```bash
fly secrets set BASE_NETWORK=sepolia
fly secrets set GROQ_API_KEY=YOUR_GROQ_API_KEY
fly secrets set BANKR_API_KEY=YOUR_BANKR_API_KEY
fly secrets set WALLET_ADDRESS=YOUR_WALLET_ADDRESS
fly secrets set PRIVATE_KEY=YOUR_PRIVATE_KEY
fly secrets set UNISWAP_API_KEY=YOUR_UNISWAP_API_KEY
fly secrets set DEMO_MODE=false
fly secrets set EMERGENCY_STOP=false
fly secrets set LIDO_MODE=false
```

### Step 4: Deploy
```bash
fly deploy
```

---

## Verifying Deployment

After deployment, check logs:
```bash
# Railway
railway logs

# Render
# Check dashboard

# Fly.io
fly logs
```

Test the API:
```bash
curl https://your-domain.railway.app/health
curl https://your-domain.railway.app/trade-signal
```

---

## Getting Your Deployed URL

After deployment, add the URL to Synthesis:

1. Go to Railway dashboard
2. Find your project → **Settings** → **Networking** → **Public Networking** → Enable
3. Copy the generated domain (e.g., `veiltrader-ai.up.railway.app`)
4. Update Synthesis:
```bash
curl -X POST "https://synthesis.devfolio.co/projects/0eba8f11aa224a1d90206505e9dff60b" \
  -H "Authorization: Bearer YOUR_SYNTHESIS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"deployedURL": "https://your-domain.railway.app"}'
```

---

## Troubleshooting

### 401 Error (LLM Key Rejected)
- Verify `GROQ_API_KEY` is set correctly in Railway variables
- Make sure there are NO quotes around the value
- Check for extra spaces

### Import Errors
- Railway auto-installs from `requirements.txt`
- Make sure all dependencies are listed

### App Not Starting
- Check **Logs** in Railway dashboard
- Verify start command is `python main.py`
