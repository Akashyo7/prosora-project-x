#!/usr/bin/env python3
"""
Production Setup Script for Prosora Intelligence Engine
Organizes files and creates production-ready structure
"""

import os
import shutil
import json
from pathlib import Path

def create_production_structure():
    """Create production-ready directory structure"""
    
    print("🏗️ Setting up production directory structure...")
    
    # Define directory structure
    directories = [
        "frontend",
        "backend/engines",
        "backend/api",
        "backend/models",
        "backend/utils",
        "data/databases",
        "data/cache",
        "docs",
        "tests",
        "config",
        ".streamlit"
    ]
    
    # Create directories
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created: {directory}/")
    
    return directories

def organize_files():
    """Organize existing files into production structure"""
    
    print("📁 Organizing files into production structure...")
    
    # File organization mapping
    file_mappings = {
        # Frontend files
        "frontend/": [
            "prosora_complete_dashboard.py",
            "launch_complete_dashboard.py",
            "test_phase*_interface.py"
        ],
        
        # Backend engine files
        "backend/engines/": [
            "phase*_*.py",
            "enhanced_unified_intelligence.py",
            "unified_prosora_intelligence.py",
            "learning_loop_engine.py",
            "real_source_fetcher.py"
        ],
        
        # Backend utilities
        "backend/utils/": [
            "data_manager.py",
            "performance_tracker.py",
            "megatrends_radar.py",
            "google_evidence_search.py"
        ],
        
        # Configuration files
        "config/": [
            "prosora_sources.yaml",
            "config.py",
            ".env.example"
        ],
        
        # Documentation
        "docs/": [
            "*.md",
            "*_GUIDE.md",
            "*_SUMMARY.md"
        ],
        
        # Tests
        "tests/": [
            "test_*.py",
            "simple_test.py"
        ]
    }
    
    # Move files (simulation - actual moving would be done manually)
    for target_dir, patterns in file_mappings.items():
        print(f"📂 {target_dir}")
        for pattern in patterns:
            print(f"   • {pattern}")
    
    print("✅ File organization plan created")

def create_requirements_txt():
    """Create production requirements.txt"""
    
    requirements = [
        "streamlit>=1.28.0",
        "plotly>=5.15.0",
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "google-generativeai>=0.3.0",
        "feedparser>=6.0.10",
        "beautifulsoup4>=4.12.0",
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
        "pyyaml>=6.0",
        "fastapi>=0.104.0",
        "uvicorn>=0.24.0",
        "sqlalchemy>=2.0.0",
        "psycopg2-binary>=2.9.0",
        "redis>=5.0.0",
        "celery>=5.3.0",
        "pydantic>=2.4.0",
        "python-multipart>=0.0.6",
        "python-jose[cryptography]>=3.3.0",
        "passlib[bcrypt]>=1.7.4"
    ]
    
    with open("requirements.txt", "w") as f:
        f.write("\n".join(requirements))
    
    print("✅ Created requirements.txt")

def create_streamlit_config():
    """Create Streamlit configuration"""
    
    config_content = """[global]
developmentMode = false

[server]
headless = true
port = 8501
enableCORS = false
maxUploadSize = 200

[theme]
base = "light"
primaryColor = "#FF6B6B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"

[browser]
gatherUsageStats = false
"""
    
    with open(".streamlit/config.toml", "w") as f:
        f.write(config_content)
    
    print("✅ Created .streamlit/config.toml")

def create_dockerfile():
    """Create production Dockerfile"""
    
    dockerfile_content = """# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    g++ \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create data directories
RUN mkdir -p data/databases data/cache

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run the application
CMD ["streamlit", "run", "frontend/prosora_complete_dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]
"""
    
    with open("Dockerfile", "w") as f:
        f.write(dockerfile_content)
    
    print("✅ Created Dockerfile")

def create_docker_compose():
    """Create docker-compose for local development"""
    
    compose_content = """version: '3.8'

services:
  prosora-app:
    build: .
    ports:
      - "8501:8501"
    environment:
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - GOOGLE_API_KEY=${GOOGLE_API_KEY}
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
    volumes:
      - ./data:/app/data
      - ./config:/app/config
    depends_on:
      - postgres
      - redis

  postgres:
    image: postgres:15
    environment:
      - POSTGRES_DB=prosora
      - POSTGRES_USER=prosora
      - POSTGRES_PASSWORD=prosora_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
"""
    
    with open("docker-compose.yml", "w") as f:
        f.write(compose_content)
    
    print("✅ Created docker-compose.yml")

def create_railway_config():
    """Create Railway deployment configuration"""
    
    railway_config = """[build]
builder = "DOCKERFILE"

[deploy]
healthcheckPath = "/_stcore/health"
healthcheckTimeout = 300
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 3

[env]
PYTHONPATH = "/app"
"""
    
    with open("railway.toml", "w") as f:
        f.write(railway_config)
    
    print("✅ Created railway.toml")

def create_vercel_config():
    """Create Vercel deployment configuration"""
    
    vercel_config = {
        "builds": [
            {
                "src": "frontend/prosora_complete_dashboard.py",
                "use": "@vercel/python"
            }
        ],
        "routes": [
            {
                "src": "/(.*)",
                "dest": "frontend/prosora_complete_dashboard.py"
            }
        ],
        "env": {
            "GEMINI_API_KEY": "@gemini_api_key",
            "GOOGLE_API_KEY": "@google_api_key"
        }
    }
    
    with open("vercel.json", "w") as f:
        json.dump(vercel_config, f, indent=2)
    
    print("✅ Created vercel.json")

def create_gitignore():
    """Create comprehensive .gitignore"""
    
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Environment variables
.env
.env.local
.env.production
.env.staging

# Database
*.db
*.sqlite
*.sqlite3

# Data files
data/databases/*.db
data/cache/*
!data/databases/.gitkeep
!data/cache/.gitkeep

# Logs
*.log
logs/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Streamlit
.streamlit/secrets.toml

# Firebase
firebase_config.json
*firebase*adminsdk*.json

# API Keys
*api_key*
*secret*
*token*

# Temporary files
tmp/
temp/
*.tmp

# Docker
.dockerignore

# Node modules (if any)
node_modules/

# Coverage reports
htmlcov/
.coverage
.coverage.*
coverage.xml
*.cover
.hypothesis/
.pytest_cache/
"""
    
    with open(".gitignore", "w") as f:
        f.write(gitignore_content)
    
    print("✅ Created .gitignore")

def create_readme():
    """Create production README"""
    
    readme_content = """# 🧠 Prosora Intelligence Engine

## Production-Ready AI Content Intelligence System

### 🚀 Quick Start

#### Local Development
```bash
# Clone repository
git clone <your-repo-url>
cd prosora-intelligence

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys

# Run the application
python launch_complete_dashboard.py
```

#### Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up --build
```

#### Cloud Deployment

**Streamlit Cloud:**
1. Connect your GitHub repository
2. Set environment variables in Streamlit Cloud dashboard
3. Deploy automatically

**Railway:**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway link
railway up
```

### 🏗️ Architecture

- **Frontend**: Streamlit Dashboard
- **Backend**: 5-Phase Intelligence Engine
- **Database**: SQLite (local) / PostgreSQL (production)
- **AI**: Google Gemini API
- **Sources**: RSS feeds, web scraping

### 📊 Features

- **Phase 1**: Smart Query Analysis
- **Phase 2**: Real Source Integration
- **Phase 3**: Voice Personalization
- **Phase 4**: Content Optimization
- **Phase 5**: Self-Improving Learning Loop

### 🔧 Configuration

Environment variables required:
- `GEMINI_API_KEY`: Google Gemini API key
- `GOOGLE_API_KEY`: Google Search API key (optional)
- `DATABASE_URL`: Database connection string (production)

### 📈 Monitoring

- Application logs via Streamlit
- Performance metrics in dashboard
- Learning analytics built-in

### 🆘 Support

See `docs/` directory for detailed documentation.

### 📄 License

Private - All rights reserved.
"""
    
    with open("README.md", "w") as f:
        f.write(readme_content)
    
    print("✅ Created production README.md")

def create_env_example():
    """Create environment variables example"""
    
    env_content = """# Prosora Intelligence Engine - Environment Variables

# AI API Keys
GEMINI_API_KEY=your_gemini_api_key_here
GOOGLE_API_KEY=your_google_api_key_here

# Database (Production)
DATABASE_URL=postgresql://user:password@localhost:5432/prosora

# Redis (Production)
REDIS_URL=redis://localhost:6379

# Firebase (Optional)
FIREBASE_CONFIG_PATH=firebase_config.json

# Application Settings
APP_NAME=Prosora Intelligence Engine
APP_VERSION=1.0.0
DEBUG_MODE=false

# Email Configuration (Optional)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_app_password

# Security
SECRET_KEY=your_secret_key_here
JWT_SECRET=your_jwt_secret_here

# External APIs (Optional)
SERP_API_KEY=your_serp_api_key
YOUTUBE_API_KEY=your_youtube_api_key
TWITTER_BEARER_TOKEN=your_twitter_token
LINKEDIN_ACCESS_TOKEN=your_linkedin_token
"""
    
    with open(".env.example", "w") as f:
        f.write(env_content)
    
    print("✅ Created .env.example")

def main():
    """Main setup function"""
    print("🚀 Prosora Intelligence Engine - Production Setup")
    print("=" * 60)
    
    try:
        # Create directory structure
        create_production_structure()
        
        # Organize files (plan)
        organize_files()
        
        # Create configuration files
        create_requirements_txt()
        create_streamlit_config()
        create_dockerfile()
        create_docker_compose()
        create_railway_config()
        create_vercel_config()
        create_gitignore()
        create_readme()
        create_env_example()
        
        print("\n🎉 Production setup completed successfully!")
        print("\n📋 Next Steps:")
        print("1. Manually move files to their respective directories")
        print("2. Set up your .env file with API keys")
        print("3. Test locally with: python launch_complete_dashboard.py")
        print("4. Deploy to your chosen platform")
        print("5. Set up monitoring and analytics")
        
        print("\n🚀 Ready for production deployment!")
        
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()