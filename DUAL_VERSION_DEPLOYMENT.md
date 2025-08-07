# 🚀 Dual-Version Deployment Guide

## 📋 **Deployment Overview**

We've created a **dual-version deployment** that allows users to choose their experience level:

- **Standard Version**: Simple, powerful, perfect for getting started
- **Enhanced Version**: Advanced controls, maximum personalization

## 🎯 **Main Application Structure**

### **Entry Point**: `prosora_main_app.py`
- Version selection interface
- Feature comparison
- Quick start guides
- Version switching capability

### **Standard Version**: `prosora_complete_dashboard.py`
- Complete 5-phase intelligence pipeline
- Basic personalization
- Demo mode and sample data
- Performance tracking

### **Enhanced Version**: `prosora_enhanced_dashboard.py`
- Everything in Standard +
- Advanced personalization controls
- Smart presets system
- Granular source management
- Multi-view dashboard

## 🚀 **Streamlit Cloud Deployment**

### **Step 1: Update Repository**
Push all new files to GitHub:
```bash
git add .
git commit -m "🚀 Add dual-version deployment with user experience selection"
git push origin main
```

### **Step 2: Deploy to Streamlit Cloud**
1. Go to: **https://share.streamlit.io**
2. Sign in with GitHub account
3. Click **"New app"**
4. **Repository**: `Akashyo7/prosora-project-x`
5. **Branch**: `main`
6. **Main file path**: `prosora_main_app.py` ⭐ **(Use main app as entry point)**

### **Step 3: Add Secrets**
In Advanced settings, add:
```toml
GEMINI_API_KEY = "AIzaSyB8kyermgcBRRN27yy3UnB2KBzOQPt3_OQ"
```

### **Step 4: Deploy**
Click "Deploy!" and wait 3-5 minutes.

## 🌐 **Live App URL**
Your dual-version app will be live at:
```
https://akashyo7-prosora-project-x-prosora-main-app-main.streamlit.app
```

## 🧪 **Testing Both Versions**

### **Standard Version Testing:**
1. Select "Standard Version" from landing page
2. Enable "Demo Mode"
3. Click "Generate Sample Data"
4. Try queries: "AI regulation impact", "Tech trends analysis"
5. Test all view modes

### **Enhanced Version Testing:**
1. Select "Enhanced Version" from landing page
2. Try Smart Presets: "Thought Leader", "Viral Content"
3. Customize personalization settings
4. Test source management dashboard
5. Save and export profile

## 📊 **User Experience Flow**

### **New Users:**
1. **Landing Page** → Choose experience level
2. **Feature Comparison** → Understand differences
3. **Quick Start Guide** → Get oriented
4. **Version Launch** → Start using immediately

### **Returning Users:**
1. **Direct Access** → Last used version remembered
2. **Version Switching** → Easy toggle between versions
3. **Profile Persistence** → Settings saved across sessions

## 🎛️ **Version Switching**

Users can switch between versions anytime:
- **Sidebar Button**: "Switch Version" 
- **Seamless Transition**: No data loss
- **Context Preservation**: Settings maintained where possible

## 🔧 **File Dependencies**

### **Core Files (Required for both versions):**
- `config.py` - Configuration management
- `phase5_self_improving_intelligence.py` - Main intelligence engine
- `learning_loop_engine.py` - Learning system
- `real_source_fetcher.py` - Source integration
- All phase files (phase2-phase5)

### **Standard Version Files:**
- `prosora_complete_dashboard.py` - Main standard interface

### **Enhanced Version Files:**
- `prosora_enhanced_dashboard.py` - Enhanced interface
- `enhanced_personalization_controls.py` - Advanced controls
- `source_linking_system.py` - Source management

### **Shared Resources:**
- `prosora_sources.yaml` - Source configurations
- `requirements.txt` - Dependencies
- `.env` - Environment variables

## 🚨 **Troubleshooting**

### **Import Errors:**
- All files are in the same directory
- No relative imports needed
- Fallback to version selector on errors

### **Version Loading Issues:**
- Graceful error handling
- Automatic fallback options
- Demo mode as backup

### **Performance Optimization:**
- Lazy loading of versions
- Session state management
- Efficient resource usage

## 📈 **Analytics & Monitoring**

### **Usage Tracking:**
- Version selection preferences
- Feature usage patterns
- Error rates by version
- User journey analysis

### **Performance Metrics:**
- Load times by version
- Memory usage comparison
- API call efficiency
- User satisfaction scores

## 🎉 **Deployment Benefits**

### **For Users:**
- ✅ **Choice**: Pick the right experience level
- ✅ **Flexibility**: Switch versions anytime
- ✅ **Learning**: Grow from Standard to Enhanced
- ✅ **Consistency**: Same core intelligence engine

### **For Development:**
- ✅ **Scalability**: Easy to add new versions
- ✅ **Testing**: A/B test different interfaces
- ✅ **Maintenance**: Modular architecture
- ✅ **Analytics**: Track version preferences

## 🚀 **Ready to Deploy!**

Your Prosora Intelligence Engine now offers:
- **Two complete user experiences**
- **Seamless version switching**
- **Progressive feature disclosure**
- **Enterprise-ready architecture**

**Deploy with `prosora_main_app.py` as the main file!** 🎯