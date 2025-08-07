#!/usr/bin/env python3
"""
Prosora Intelligence Engine - Main Application
Dual-version deployment with user experience level selection
"""

import streamlit as st
import sys
import importlib
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Prosora Intelligence Engine",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

class ProsoraMainApp:
    def __init__(self):
        self.initialize_session_state()
    
    def initialize_session_state(self):
        """Initialize session state variables"""
        if 'selected_version' not in st.session_state:
            st.session_state.selected_version = None
        if 'show_version_selector' not in st.session_state:
            st.session_state.show_version_selector = True
    
    def render_version_selector(self):
        """Render version selection interface"""
        st.title("🧠 Prosora Intelligence Engine")
        st.subheader("Choose Your Experience Level")
        
        # Version comparison
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### 📊 **Standard Version**
            *Perfect for getting started quickly*
            
            **Features:**
            - ✅ Complete 5-Phase Intelligence Pipeline
            - ✅ Real RSS source integration
            - ✅ AI-powered content generation
            - ✅ Basic personalization
            - ✅ Performance tracking
            - ✅ Learning loop system
            - ✅ Demo mode for testing
            
            **Best for:**
            - First-time users
            - Quick content generation
            - Straightforward workflows
            - Learning the system
            
            **Setup time:** 2 minutes
            """)
            
            if st.button("🚀 Launch Standard Version", type="primary", use_container_width=True):
                st.session_state.selected_version = "standard"
                st.session_state.show_version_selector = False
                st.rerun()
        
        with col2:
            st.markdown("""
            ### 🎛️ **Enhanced Version**
            *Advanced controls for power users*
            
            **Features:**
            - ✅ Everything in Standard Version
            - ✅ **Advanced Personalization Controls**
            - ✅ **Smart Presets** (Thought Leader, Viral, Research)
            - ✅ **Granular Source Management**
            - ✅ **Real-time Impact Metrics**
            - ✅ **Profile Save/Load/Share**
            - ✅ **Multi-view Dashboard**
            - ✅ **Performance Analytics**
            
            **Best for:**
            - Power users and professionals
            - Team collaboration
            - Custom workflows
            - Maximum personalization
            
            **Setup time:** 5 minutes
            """)
            
            if st.button("⚡ Launch Enhanced Version", type="secondary", use_container_width=True):
                st.session_state.selected_version = "enhanced"
                st.session_state.show_version_selector = False
                st.rerun()
        
        # Feature comparison table
        st.divider()
        st.subheader("📋 Feature Comparison")
        
        comparison_data = {
            "Feature": [
                "5-Phase Intelligence Pipeline",
                "Real Source Integration",
                "AI Content Generation",
                "Basic Personalization",
                "Demo Mode",
                "Smart Presets",
                "Advanced Personalization",
                "Source Management Dashboard",
                "Real-time Impact Metrics",
                "Profile Management",
                "Multi-view Interface",
                "Performance Analytics",
                "Team Collaboration Ready"
            ],
            "Standard": [
                "✅", "✅", "✅", "✅", "✅", "❌", "❌", "❌", "❌", "❌", "❌", "Basic", "❌"
            ],
            "Enhanced": [
                "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "Advanced", "✅"
            ]
        }
        
        import pandas as pd
        df = pd.DataFrame(comparison_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Quick start guides
        st.divider()
        st.subheader("🚀 Quick Start Guides")
        
        col1, col2 = st.columns(2)
        
        with col1:
            with st.expander("📖 Standard Version Guide"):
                st.markdown("""
                **Getting Started:**
                1. Enable "Demo Mode" for safe testing
                2. Click "Generate Sample Data"
                3. Try example queries:
                   - "AI regulation impact on fintech"
                   - "Cross-domain analysis of tech policy"
                4. Explore different view modes
                5. Check analytics dashboard
                
                **Pro Tips:**
                - Use demo mode first to understand capabilities
                - Try different query complexities
                - Check the learning insights panel
                """)
        
        with col2:
            with st.expander("🎛️ Enhanced Version Guide"):
                st.markdown("""
                **Getting Started:**
                1. Choose a Smart Preset (Thought Leader, Viral, etc.)
                2. Customize your voice and style settings
                3. Configure source priorities
                4. Generate content with personalization
                5. Save your profile for future use
                
                **Pro Tips:**
                - Start with presets, then customize
                - Use real-time impact metrics to optimize
                - Export profiles to share with team
                - Explore the source management dashboard
                """)
    
    def render_version_switcher(self):
        """Render version switcher in sidebar"""
        st.sidebar.title("🧠 Prosora Intelligence")
        
        current_version = "Enhanced" if st.session_state.selected_version == "enhanced" else "Standard"
        st.sidebar.write(f"**Current:** {current_version} Version")
        
        if st.sidebar.button("🔄 Switch Version"):
            st.session_state.show_version_selector = True
            st.session_state.selected_version = None
            st.rerun()
        
        # Version-specific info
        if st.session_state.selected_version == "standard":
            st.sidebar.info("📊 Using Standard Version - Simple and powerful!")
        else:
            st.sidebar.info("⚡ Using Enhanced Version - Maximum control!")
        
        # System status
        st.sidebar.divider()
        st.sidebar.subheader("📈 System Status")
        st.sidebar.write(f"**Version:** {current_version}")
        st.sidebar.write(f"**Status:** 🟢 Active")
        st.sidebar.write(f"**Last Updated:** {datetime.now().strftime('%H:%M')}")
    
    def load_and_run_version(self, version: str):
        """Load and run the selected version"""
        try:
            if version == "standard":
                # Import and run standard dashboard
                from prosora_complete_dashboard import ProsoraCompleteDashboard
                dashboard = ProsoraCompleteDashboard()
                
                # Render version switcher in sidebar
                self.render_version_switcher()
                
                # Run the standard dashboard
                dashboard.run()
                
            elif version == "enhanced":
                # Import and run enhanced dashboard
                from prosora_enhanced_dashboard import ProsoraEnhancedDashboard
                dashboard = ProsoraEnhancedDashboard()
                
                # Render version switcher in sidebar
                self.render_version_switcher()
                
                # Run the enhanced dashboard
                dashboard.run()
                
        except ImportError as e:
            st.error(f"Error loading {version} version: {str(e)}")
            st.info("Falling back to version selector...")
            st.session_state.show_version_selector = True
            st.session_state.selected_version = None
            st.rerun()
        
        except Exception as e:
            st.error(f"Error running {version} version: {str(e)}")
            
            # Provide fallback options
            st.subheader("🔧 Troubleshooting Options")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("🔄 Retry"):
                    st.rerun()
            
            with col2:
                if st.button("🔙 Back to Selector"):
                    st.session_state.show_version_selector = True
                    st.session_state.selected_version = None
                    st.rerun()
            
            with col3:
                if st.button("🎮 Enable Demo Mode"):
                    st.session_state.demo_mode = True
                    st.rerun()
    
    def run(self):
        """Main application runner"""
        # Show version selector or run selected version
        if st.session_state.show_version_selector or st.session_state.selected_version is None:
            self.render_version_selector()
        else:
            self.load_and_run_version(st.session_state.selected_version)

# Main execution
if __name__ == "__main__":
    app = ProsoraMainApp()
    app.run()