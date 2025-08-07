#!/usr/bin/env python3
"""
Test the info buttons functionality
"""

import streamlit as st

st.set_page_config(page_title="Info Buttons Test", layout="wide")

st.title("🧠 Metric Info Buttons Test")

# Initialize session state
if 'show_test_info' not in st.session_state:
    st.session_state.show_test_info = False

# Test metric with info button
col1, col2 = st.columns([4, 1])

with col1:
    st.metric("Test Metric", "85.5/100", delta="↗️ +5.2")

with col2:
    if st.button("ℹ️", key="test_info_btn", help="Click for details"):
        st.session_state.show_test_info = True

# Show info modal if requested
if st.session_state.show_test_info:
    with st.expander("ℹ️ Test Metric Info", expanded=True):
        col1, col2 = st.columns([10, 1])
        
        with col1:
            st.write("**Description:** This is a test metric to demonstrate the info button functionality.")
            st.write("**Calculation:** Random number between 0-100 for demonstration purposes.")
            st.write("**Range:** 0-100 (higher is better)")
            st.write("**Interpretation:** 80+ = Excellent, 60-80 = Good, <60 = Needs improvement")
        
        with col2:
            if st.button("✕", key="close_test_info", help="Close"):
                st.session_state.show_test_info = False
                st.rerun()

st.write("---")
st.write("**Instructions:**")
st.write("1. Click the ℹ️ button next to the metric")
st.write("2. An info panel will expand with details")
st.write("3. Click the ✕ button to close the info panel")
st.write("4. This pattern will be used throughout the Prosora dashboard")