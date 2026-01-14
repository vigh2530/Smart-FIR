# Smart FIR Legal Intelligence System using ML + Ollama

## Overview
An offline AI system that analyzes FIR text and provides IPC predictions,
crime severity, explainability, FIR quality assessment, and legal awareness.

## Tech Stack
- Python 3.10
- TF-IDF + Logistic Regression
- Streamlit
- Ollama (llama3)

## Features
- IPC Section Prediction
- Top-3 IPC Recommendations
- FIR Quality Checker
- Explainable AI
- Crime Severity Analysis
- Punishment Explanation
- Hinglish FIR Support

## Installation & Setup

### Prerequisites
- Python 3.10+
- Ollama (https://ollama.com)
- Docker & Docker Compose (for containerized deployment)

### Local Setup
1. Clone the repository:
```bash
git clone <repo-url>
cd Smart_FIR_Legal_AI_Ollama
```

2. Create virtual environment:
```bash
python -m venv fir
fir\Scripts\activate  # Windows
source fir/bin/activate  # Linux/Mac
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install Ollama and pull model:
```bash
ollama pull mistral  # or llama2, gemma3:1b, etc
```

5. Start Ollama service:
```bash
ollama serve
```

6. Train the ML model:
```bash
python train_model.py
```

7. Run the Streamlit app:
```bash
streamlit run app.py
```

## Docker Deployment

### Build & Run Locally
```bash
docker-compose up --build
```

Access at: http://localhost:8501

### Deploy to Cloud

#### Option A: AWS EC2
```bash
# Install Docker on EC2
sudo apt-get update
sudo apt-get install docker.io docker-compose -y

# Clone and run
git clone <repo-url>
cd Smart_FIR_Legal_AI_Ollama
docker-compose up -d
```

#### Option B: Google Cloud Run / Azure Container Instances
```bash
# Push to container registry
docker tag fir-app gcr.io/<project>/fir-app:latest
docker push gcr.io/<project>/fir-app:latest

# Deploy (follow platform-specific guides)
```

#### Option C: Heroku
```bash
heroku login
heroku create fir-legal-ai
git push heroku main
```

## Production Notes
- Set Ollama timeout higher in `ollama/ollama_client.py` for slow connections
- Use environment variables for configuration
- Enable HTTPS/SSL certificates
- Set up logging and monitoring
- Consider load balancing for high traffic

## How to Run
