# 🔐 Security Guide for Prosora Intelligence Engine

## ⚠️ CRITICAL: API Key Security

### What Happened?
GitHub detected an exposed Google API key in our repository. This is a serious security issue that could lead to:
- Unauthorized API usage
- Billing charges on your account
- Rate limit exhaustion
- Potential service disruption

### ✅ Security Fixes Applied

1. **Removed hardcoded API keys** from all source files
2. **Updated config.py** to only use environment variables
3. **Created .env file** for local development
4. **Updated deployment guides** to use placeholders
5. **Added API key validation** in config

### 🛡️ Security Best Practices

#### For Local Development:
```bash
# 1. Copy your API key to .env file
echo "GEMINI_API_KEY=your_actual_api_key_here" > .env

# 2. Never commit .env files (already in .gitignore)
git status  # Should not show .env
```

#### For Streamlit Cloud Deployment:
1. Go to Streamlit Cloud deployment settings
2. Click "Advanced settings"
3. Add to secrets section:
```toml
GEMINI_API_KEY = "your_actual_api_key_here"
```

#### For Production:
- Use environment variables or secure secret management
- Rotate API keys regularly
- Monitor API usage for anomalies
- Set up billing alerts

### 🚨 If Your API Key Was Exposed:

1. **Immediately revoke** the exposed key in Google Cloud Console
2. **Generate a new API key**
3. **Update your .env file** with the new key
4. **Update Streamlit Cloud secrets** with the new key
5. **Monitor billing** for any unauthorized usage

### 📋 Security Checklist

- [ ] API keys stored in environment variables only
- [ ] .env file in .gitignore
- [ ] No hardcoded secrets in source code
- [ ] Streamlit secrets configured properly
- [ ] API key validation in place
- [ ] Regular security audits

### 🔍 How to Check for Exposed Secrets

```bash
# Search for potential API keys in your code
grep -r "AIza" . --exclude-dir=.git
grep -r "api_key" . --exclude-dir=.git
grep -r "secret" . --exclude-dir=.git
```

Remember: **Security is not optional!** Always treat API keys like passwords.