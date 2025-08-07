#!/usr/bin/env python3
"""
Prosora Command Center Launcher
Launch the streamlined Google-like interface
"""

import streamlit as st
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    """Launch the Prosora Command Center"""
    
    # Set page config
    st.set_page_config(
        page_title="Prosora Intelligence Command Center",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="collapsed",
        menu_items={
            'Get Help': 'https://prosora.in/help',
            'Report a bug': 'https://prosora.in/support',
            'About': "Prosora Intelligence Engine - Generate evidence-backed content instantly"
        }
    )
    
    # Custom CSS for enhanced styling
    st.markdown("""
    <style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom styling */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Enhanced search container */
    .search-container {
        background: white;
        border-radius: 24px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        padding: 25px;
        margin: 30px 0;
        border: 1px solid #e8eaed;
    }
    
    /* Button styling */
    .stButton > button {
        border-radius: 20px;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    
    /* Metrics styling */
    .metric-container {
        background: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin: 10px 0;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 12px;
        padding: 12px 24px;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        border-radius: 8px;
        background-color: #f8f9fa;
    }
    
    /* Success/Error message styling */
    .stSuccess, .stError, .stWarning, .stInfo {
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    try:
        # Import and run the command interface
        from prosora_command_interface import ProsoraCommandInterface
        
        # Initialize and render
        command_interface = ProsoraCommandInterface()
        command_interface.render_command_interface()
        
    except ImportError as e:
        st.error(f"❌ Import Error: {e}")
        st.info("💡 Make sure all required files are in the same directory")
        
        # Show setup instructions
        with st.expander("🔧 Setup Instructions", expanded=True):
            st.markdown("""
            ### Required Files:
            - `prosora_command_interface.py`
            - `enhanced_content_generator.py`
            - `google_evidence_search.py`
            - `firebase_integration.py`
            - `requirements.txt`
            
            ### Installation:
            ```bash
            pip install -r requirements.txt
            streamlit run launch_prosora_command_center.py
            ```
            
            ### Firebase Setup:
            1. Create Firebase project
            2. Enable Firestore
            3. Download service account key
            4. Configure in the app
            """)
    
    except Exception as e:
        st.error(f"❌ Application Error: {e}")
        st.info("💡 Please check your configuration and try again")
        
        # Debug information
        with st.expander("🐛 Debug Information"):
            st.code(f"Error: {str(e)}")
            st.code(f"Python Path: {sys.path}")
            st.code(f"Current Directory: {os.getcwd()}")

if __name__ == "__main__":
    main()