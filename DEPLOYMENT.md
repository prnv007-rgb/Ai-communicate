# 🚀 Complete Deployment Guide

Comprehensive step-by-step instructions for deploying the AI Communication Coach application locally and on cloud platforms.

---

## 📋 Table of Contents

1. [Local Deployment](#-local-deployment)
2. [Streamlit Cloud Deployment](#-streamlit-cloud-deployment)
3. [Hugging Face Spaces Deployment](#-hugging-face-spaces-deployment)
4. [AWS EC2 Deployment](#-aws-ec2-deployment)
5. [Troubleshooting](#-troubleshooting)
6. [Performance Optimization](#-performance-optimization)

---

## 🖥️ Local Deployment

Perfect for development, testing, and video recording.

### Prerequisites

- **Python:** 3.11
- **RAM:** Minimum 2GB, Recommended 4GB+
- **Storage:** ~500MB for dependencies
- **Internet:** Required for initial setup only

### Step-by-Step Installation

#### 1. Download Project Files

**Option A: Using Git (Recommended)**
```bash
git clone https://github.com/prnv007-rgb/Ai-communicate.git
```

**Option B: Download ZIP**
1. Go to GitHub repository
2. Click green "Code" button → "Download ZIP"
3. Extract to a folder
4. Open terminal/command prompt in that folder

#### 2. Verify Python Installation

```bash
# Check Python version
python --version
# Should show: Python 3.8.x or higher

# If "python" doesn't work, try:
python3 --version
```

**Don't have Python?** Download from [python.org/downloads](https://python.org/downloads)

#### 3. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

You'll see `(venv)` appear in your terminal.

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Why virtual environment?**
- Keeps dependencies isolated
- Prevents conflicts with other projects
- Easy to delete and recreate

#### 4. Upgrade pip

```bash
python -m pip install --upgrade pip
```

#### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

**Expected time:** 3-5 minutes

**What's being installed:**
- Streamlit (web framework)
- spaCy (NLP library)
- sentence-transformers (semantic similarity)
- vaderSentiment (sentiment analysis)
- PyTorch (ML framework)
- pandas (data handling)

**Progress indicators:**
```
Collecting streamlit==1.28.0
  Downloading streamlit-1.28.0-py2.py3-none-any.whl (8.4 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 8.4/8.4 MB 2.1 MB/s eta 0:00:00
Installing collected packages: ...
Successfully installed ...
```

#### 6. Download spaCy Language Model

```bash
python -m spacy download en_core_web_sm
```

This downloads the English language model (~13MB).

#### 7. Verify Installation

```bash
python -c "import spacy, streamlit, sentence_transformers; print('✅ All packages loaded successfully!')"
```

Expected output: `✅ All packages loaded successfully!`

#### 8. Run the Application

```bash
streamlit run app.py
```

**Expected output:**
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.1.100:8501
```

**What happens:**
- Streamlit starts a local web server
- Browser opens automatically
- If not, manually open: `http://localhost:8501`

#### 9. Test the Application

1. Paste a transcript in the text area
2. Enter duration (e.g., 52 seconds)
3. Click "🔍 Analyze Score"
4. View results!

#### 10. Stopping the Application

Press `Ctrl + C` in the terminal.

### Quick Reference Commands

```bash
# Activate environment
venv\Scripts\activate          # Windows
source venv/bin/activate       # Mac/Linux

# Run app
streamlit run app.py

# Run on different port
streamlit run app.py --server.port 8502

# Deactivate environment
deactivate

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

---

## ☁️ Streamlit Cloud Deployment

**Free, automatic deployment from GitHub.** Best for public demos.

### Prerequisites

- GitHub account (free)
- Streamlit Cloud account (free at [streamlit.io](https://streamlit.io))
- Project pushed to GitHub

### Step 1: Prepare Your Repository

#### Create `.gitignore`

Create a file named `.gitignore` in your project root:

```gitignore
# Virtual environment
venv/
env/

# Python cache
__pycache__/
*.pyc
*.pyo
*.pyd

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Environment variables
.env
.env.local

# Logs
*.log
```

#### Verify `requirements.txt`

Ensure your `requirements.txt` contains:

```txt
streamlit==1.28.0
spacy==3.7.0
pandas==2.1.1
vaderSentiment==3.3.2
sentence-transformers==2.2.2
torch==2.1.0
openpyxl==3.1.2
https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.0/en_core_web_sm-3.7.0-py3-none-any.whl
```

**⚠️ Important:** The last line installs the spaCy model directly.

#### Optional: Create `.streamlit/config.toml`

For custom theme (optional):

```bash
mkdir .streamlit
```

Create `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#0066cc"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"

[server]
maxUploadSize = 5
```

### Step 2: Push to GitHub

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: AI Communication Coach"

# Create repository on GitHub first (github.com/new)
# Then connect:
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPO-NAME.git

# Push
git branch -M main
git push -u origin main
```

### Step 3: Deploy on Streamlit Cloud

1. **Visit:** [share.streamlit.io](https://share.streamlit.io)

2. **Sign in** with GitHub

3. **Click:** "New app"

4. **Fill form:**
   - **Repository:** Select your repository
   - **Branch:** `main`
   - **Main file path:** `app.py`
   - **App URL (optional):** Choose custom subdomain

5. **Advanced settings (click to expand):**
   - **Python version:** 3.10
   - **Secrets:** Leave empty (none needed)

6. **Click:** "Deploy!"

### Step 4: Monitor Deployment

You'll see build logs:

```
[12:00:00] 🎬 Starting build...
[12:00:15] 📦 Cloning repository...
[12:00:30] 🐍 Setting up Python 3.10...
[12:01:00] 📥 Installing dependencies...
[12:03:00] ⚡ Building application...
[12:03:30] ✅ Deployment successful!
```

**Total time:** 5-10 minutes

### Step 5: Access Your App

Your app will be live at:
```
https://YOUR-USERNAME-YOUR-REPO-NAME.streamlit.app
```

**Share this link in your submission!**

### Updating Your App

Any push to GitHub automatically triggers redeployment:

```bash
# Make changes to code
git add .
git commit -m "Updated scoring logic"
git push

# Streamlit Cloud detects changes and redeploys automatically
```

### Streamlit Cloud Features

- ✅ **Automatic HTTPS**
- ✅ **Free subdomain**
- ✅ **Auto-redeploy on git push**
- ✅ **Usage analytics**
- ✅ **Community support**

**Limits (Free tier):**
- 1 GB RAM
- 1 CPU core
- 1 concurrent user
- Perfect for demos!

---

## 🤗 Hugging Face Spaces Deployment

**Free ML app hosting with better ML infrastructure.**

### Step 1: Create Account

1. Go to [huggingface.co/join](https://huggingface.co/join)
2. Sign up (free)
3. Verify email

### Step 2: Create New Space

1. Click your profile → **"New Space"**

2. **Fill form:**
   - **Space name:** `communication-analyzer`
   - **License:** MIT
   - **Select SDK:** **Streamlit**
   - **Space hardware:** CPU basic (free)
   - **Visibility:** Public

3. Click **"Create Space"**

### Step 3: Upload Files

You'll see a page with Git instructions. Two methods:

#### Method A: Web Interface (Easiest)

1. Click **"Files"** tab
2. Click **"Add file"** → **"Upload files"**
3. Upload these files:
   - `app.py`
   - `scorer.py`
   - `requirements.txt`
   - `README.md`
4. Click **"Commit to main"**

#### Method B: Git CLI

```bash
# Clone your space
git clone https://huggingface.co/spaces/YOUR-USERNAME/communication-analyzer
cd communication-analyzer

# Copy your files
cp /path/to/your/app.py .
cp /path/to/your/scorer.py .
cp /path/to/your/requirements.txt .
cp /path/to/your/README.md .

# Commit and push
git add .
git commit -m "Add communication analyzer"
git push
```

### Step 4: Configure Requirements

HF Spaces uses the same `requirements.txt` format:

```txt
streamlit==1.28.0
spacy==3.7.0
pandas==2.1.1
vaderSentiment==3.3.2
sentence-transformers==2.2.2
torch==2.1.0
https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.0/en_core_web_sm-3.7.0-py3-none-any.whl
```

### Step 5: Wait for Build

- Building: 3-5 minutes
- Check **"Logs"** tab for progress
- Status changes: Building → Building succeeded → Running

### Step 6: Access Your App

URL: `https://huggingface.co/spaces/YOUR-USERNAME/communication-analyzer`

### HF Spaces Features

- ✅ **Better for ML apps** (optimized infrastructure)
- ✅ **GPU options** (paid)
- ✅ **Persistent storage**
- ✅ **API access**
- ✅ **Community features** (likes, comments)

---

## 🌐 AWS EC2 Deployment

**For production or learning cloud deployment.** Uses AWS Free Tier.

### Prerequisites

- AWS account (free tier eligible)
- SSH client (Terminal/PuTTY)
- Basic command line knowledge

### Step 1: Launch EC2 Instance

1. **Login to AWS Console:** [console.aws.amazon.com](https://console.aws.amazon.com)

2. **Navigate:** Services → EC2 → Launch Instance

3. **Configure:**

   **Name:** `communication-analyzer`

   **AMI:** Ubuntu Server 22.04 LTS (Free tier eligible)

   **Instance type:** t2.micro (1 vCPU, 1 GB RAM) ✅ Free tier

   **Key pair:**
   - Click "Create new key pair"
   - Name: `communication-key`
   - Type: RSA
   - Format: .pem (Mac/Linux) or .ppk (Windows/PuTTY)
   - Download and save securely

   **Network settings:**
   - ✅ Allow SSH traffic (port 22)
   - ✅ Allow HTTPS traffic (port 443)
   - ✅ Allow HTTP traffic (port 80)

   **Storage:** 8 GB gp3 (default, free tier)

4. **Click:** "Launch instance"

### Step 2: Configure Security Group

1. Go to: EC2 → Security Groups
2. Select your instance's security group
3. Click "Edit inbound rules"
4. Add rule:
   - **Type:** Custom TCP
   - **Port:** 8501
   - **Source:** Anywhere-IPv4 (0.0.0.0/0)
   - **Description:** Streamlit app
5. Save

### Step 3: Connect to Instance

**Get Public IP:**
- EC2 Dashboard → Instances → Select your instance
- Copy "Public IPv4 address" (e.g., 3.141.59.26)

**Connect via SSH:**

**Mac/Linux:**
```bash
# Set permissions on key file
chmod 400 communication-key.pem

# Connect
ssh -i "communication-key.pem" ubuntu@YOUR-PUBLIC-IP
```

**Windows (PowerShell):**
```powershell
ssh -i "communication-key.pem" ubuntu@YOUR-PUBLIC-IP
```

**Windows (PuTTY):**
1. Open PuTTY
2. Host: `ubuntu@YOUR-PUBLIC-IP`
3. Connection → SSH → Auth → Browse to .ppk file
4. Click Open

### Step 4: Install System Dependencies

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and tools
sudo apt install -y python3-pip python3-venv git

# Verify installation
python3 --version
pip3 --version
```

### Step 5: Clone and Setup Application

```bash
# Clone repository
git clone https://github.com/YOUR-USERNAME/communication-analyzer.git
cd communication-analyzer

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm
```

### Step 6: Run Application

**Method A: Temporary (for testing)**
```bash
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

Access at: `http://YOUR-PUBLIC-IP:8501`

**Press Ctrl+C to stop**

**Method B: Persistent with tmux**

```bash
# Install tmux
sudo apt install -y tmux

# Start tmux session
tmux new -s streamlit

# Run app
streamlit run app.py --server.port 8501 --server.address 0.0.0.0

# Detach: Press Ctrl+B, then D
# Reattach later: tmux attach -t streamlit
```

**Method C: System Service (Production)**

Create service file:
```bash
sudo nano /etc/systemd/system/streamlit.service
```

Paste this content:
```ini
[Unit]
Description=Streamlit Communication Analyzer
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/communication-analyzer
Environment="PATH=/home/ubuntu/communication-analyzer/venv/bin"
ExecStart=/home/ubuntu/communication-analyzer/venv/bin/streamlit run app.py --server.port 8501 --server.address 0.0.0.0
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Save:** Ctrl+X, Y, Enter

**Enable and start:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable streamlit
sudo systemctl start streamlit

# Check status
sudo systemctl status streamlit

# View logs
sudo journalctl -u streamlit -f
```

### Step 7: Optional - Setup Domain & HTTPS

**With Nginx reverse proxy:**

```bash
# Install Nginx
sudo apt install -y nginx

# Configure
sudo nano /etc/nginx/sites-available/streamlit
```

Paste:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }
}
```

**Enable:**
```bash
sudo ln -s /etc/nginx/sites-available/streamlit /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

**For HTTPS with Let's Encrypt:**
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

---

## 🔧 Troubleshooting

### Common Issues and Solutions

#### 1. ModuleNotFoundError: No module named 'X'

**Cause:** Package not installed or wrong environment

**Solution:**
```bash
# Verify you're in virtual environment (should see (venv))
# If not:
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Reinstall requirements
pip install -r requirements.txt

# If specific package missing:
pip install package-name
```

#### 2. Can't find model 'en_core_web_sm'

**Cause:** spaCy model not downloaded

**Solution:**
```bash
python -m spacy download en_core_web_sm

# If fails, try direct install:
pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.0/en_core_web_sm-3.7.0-py3-none-any.whl
```

#### 3. Port 8501 already in use

**Cause:** Another Streamlit instance running

**Solution:**
```bash
# Windows
netstat -ano | findstr :8501
taskkill /PID <PID> /F

# Mac/Linux
lsof -ti:8501 | xargs kill -9

# Or use different port:
streamlit run app.py --server.port 8502
```

#### 4. Streamlit Cloud: Build Failed

**Common causes:**

**Missing requirements:**
- Check all packages in `requirements.txt`
- Verify versions are compatible

**Python version mismatch:**
- Set Python version to 3.10 in settings

**Memory limit exceeded:**
- Model too large for 1GB RAM
- Use smaller model variant

**Solution:**
```txt
# Optimize requirements.txt for cloud
streamlit==1.28.0
spacy==3.7.0
sentence-transformers==2.2.2
torch==2.1.0+cpu  # CPU-only version (smaller)
vaderSentiment
pandas
```

#### 5. Slow First Load

**Cause:** Downloading transformer models (~100MB)

**Expected:** 30-60 seconds first time

**Solution:** Normal behavior. Subsequent loads are fast (cached).

#### 6. CUDA/GPU Errors

**Cause:** PyTorch looking for GPU

**Solution:** 
```python
# In scorer.py, explicitly use CPU:
import torch
torch.set_default_device('cpu')
```

Or install CPU-only PyTorch:
```bash
pip install torch==2.1.0+cpu -f https://download.pytorch.org/whl/torch_stable.html
```

#### 7. Memory Error on Free Tier

**Symptoms:**
- App crashes
- "MemoryError" in logs

**Solutions:**

1. **Use smaller model:**
   ```python
   # In scorer.py, change:
   self.embedder = SentenceTransformer('paraphrase-MiniLM-L3-v2')  # Smaller
   ```

2. **Upgrade tier** (Streamlit Cloud paid or AWS t2.small)

#### 8. Git Push Failed

**Cause:** Large files in repo

**Solution:**
```bash
# Don't commit these:
echo "venv/" >> .gitignore
echo "*.pyc" >> .gitignore
echo "__pycache__/" >> .gitignore

# Remove if already committed:
git rm -r --cached venv/
git commit -m "Remove venv"
git push
```

---

## ⚡ Performance Optimization

### Reduce Loading Time

```python
# In scorer.py, add caching:
import streamlit as st

@st.cache_resource
def load_models():
    """Cache models to avoid reloading"""
    sentiment = SentimentIntensityAnalyzer()
    embedder = SentenceTransformer('all-MiniLM-L6-v2')
    nlp = spacy.load("en_core_web_sm")
    return sentiment, embedder, nlp
```

### Reduce Memory Usage

1. **Use smaller spaCy model:**
   ```bash
   # Instead of en_core_web_sm
   python -m spacy download en_core_web_sm
   # 13MB, fast, sufficient for most use
   ```

2. **Disable unused spaCy components:**
   ```python
   nlp = spacy.load("en_core_web_sm", disable=["parser", "lemmatizer"])
   ```

### Optimize for Cloud Deployment

```txt
# requirements.txt for cloud (lighter)
streamlit
spacy>=3.0,<4.0
sentence-transformers
vaderSentiment
pandas
torch  # Let pip choose optimal version
```

---

## 📊 Deployment Comparison

| Feature | Local | Streamlit Cloud | HF Spaces | AWS EC2 |
|---------|-------|----------------|-----------|---------|
| **Cost** | Free | Free | Free | Free tier 1yr |
| **Setup Time** | 10 min | 15 min | 15 min | 30 min |
| **Difficulty** | ⭐ Easy | ⭐⭐ Medium | ⭐⭐ Medium | ⭐⭐⭐ Hard |
| **RAM** | Your PC | 1 GB | 2 GB | 1 GB |
| **Public URL** | ❌ | ✅ | ✅ | ✅ (manual) |
| **Auto-deploy** | ❌ | ✅ | ✅ | ❌ |
| **Best for** | Development | Demos | ML apps | Production |

---

## 🎯 Recommended Deployment Strategy

**For This Submission:**

1. ✅ **Local** - For video recording and testing
2. ✅ **Streamlit Cloud** OR **HF Spaces** - For live demo link
3. ⭐ **Document both** in README

**Timeline:**
- Local setup: 10 minutes
- Cloud deployment: 15 minutes
- **Total: 25 minutes**

---

## 📝 Deployment Checklist

Before deploying:
- [ ] All code tested locally
- [ ] `requirements.txt` complete and accurate
- [ ] `.gitignore` configured
- [ ] README.md updated with deployment links
- [ ] No sensitive data in code (API keys, passwords)
- [ ] Git repository clean (no `venv/`, `__pycache__/`)

After deploying:
- [ ] App loads successfully
- [ ] All features work
- [ ] Test with sample transcripts
- [ ] Check logs for errors
- [ ] Share link works
- [ ] Add deployment link to submission

---

## 📞 Getting Help

**Still stuck?**

1. **Check logs:**
   - Local: Terminal output
   - Streamlit Cloud: App dashboard → Logs
   - HF Spaces: Logs tab
   - AWS: `journalctl -u streamlit -f`

2. **Common fixes:**
   - Restart app
   - Clear cache: `streamlit cache clear`
   - Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`

3. **Resources:**
   - Streamlit docs: [docs.streamlit.io](https://docs.streamlit.io)
   - HF Spaces docs: [huggingface.co/docs/hub/spaces](https://huggingface.co/docs/hub/spaces)
   - AWS docs: [docs.aws.amazon.com/ec2](https://docs.aws.amazon.com/ec2)

---

**Good luck with deployment! 🚀**

*Last updated: November 2024*
