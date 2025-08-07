#!/usr/bin/env python3
"""
Firebase Integration for Prosora Intelligence Engine
Handles data persistence, user management, and real-time sync
"""

import firebase_admin
from firebase_admin import credentials, firestore, auth
import json
from datetime import datetime
from typing import Dict, List, Optional
import streamlit as st

class ProsoraFirebaseManager:
    def __init__(self, config_path: str = None):
        self.db = None
        self.setup_firebase(config_path)
    
    def setup_firebase(self, config_path: str = None):
        """Initialize Firebase with your project configuration"""
        
        try:
            # Check if Firebase is already initialized
            if not firebase_admin._apps:
                if config_path:
                    # Use service account key file
                    cred = credentials.Certificate(config_path)
                    firebase_admin.initialize_app(cred)
                else:
                    # Try to use the firebase_config.json file
                    try:
                        cred = credentials.Certificate("firebase_config.json")
                        firebase_admin.initialize_app(cred)
                    except Exception:
                        # Use default credentials (for development)
                        firebase_admin.initialize_app()
            
            self.db = firestore.client()
            print("🔥 Firebase initialized successfully")
            
        except Exception as e:
            print(f"Firebase initialization error: {e}")
            self.db = None
    
    def save_generated_content(self, user_id: str, query: str, content: Dict) -> str:
        """Save generated content to Firebase"""
        
        if not self.db:
            return None
        
        try:
            doc_data = {
                'user_id': user_id,
                'query': query,
                'content': content,
                'timestamp': datetime.now(),
                'status': 'generated',
                'engagement_metrics': {},
                'feedback': {},
                'version': 1
            }
            
            # Add to Firestore
            doc_ref = self.db.collection('prosora_content').add(doc_data)
            doc_id = doc_ref[1].id
            
            print(f"💾 Content saved to Firebase: {doc_id}")
            return doc_id
            
        except Exception as e:
            print(f"Error saving content: {e}")
            return None
    
    def get_user_content(self, user_id: str, limit: int = 10) -> List[Dict]:
        """Get user's recent content from Firebase"""
        
        if not self.db:
            return []
        
        try:
            docs = (self.db.collection('prosora_content')
                   .where('user_id', '==', user_id)
                   .order_by('timestamp', direction=firestore.Query.DESCENDING)
                   .limit(limit)
                   .stream())
            
            content_list = []
            for doc in docs:
                data = doc.to_dict()
                data['id'] = doc.id
                content_list.append(data)
            
            return content_list
            
        except Exception as e:
            print(f"Error fetching content: {e}")
            return []
    
    def save_user_preferences(self, user_id: str, preferences: Dict):
        """Save user preferences and settings"""
        
        if not self.db:
            return False
        
        try:
            self.db.collection('user_preferences').document(user_id).set({
                'preferences': preferences,
                'updated_at': datetime.now()
            }, merge=True)
            
            return True
            
        except Exception as e:
            print(f"Error saving preferences: {e}")
            return False
    
    def get_user_preferences(self, user_id: str) -> Dict:
        """Get user preferences from Firebase"""
        
        if not self.db:
            return {}
        
        try:
            doc = self.db.collection('user_preferences').document(user_id).get()
            if doc.exists:
                return doc.to_dict().get('preferences', {})
            return {}
            
        except Exception as e:
            print(f"Error fetching preferences: {e}")
            return {}
    
    def save_performance_data(self, content_id: str, platform: str, metrics: Dict):
        """Save content performance data"""
        
        if not self.db:
            return False
        
        try:
            self.db.collection('performance_data').add({
                'content_id': content_id,
                'platform': platform,
                'metrics': metrics,
                'timestamp': datetime.now()
            })
            
            return True
            
        except Exception as e:
            print(f"Error saving performance data: {e}")
            return False
    
    def get_performance_analytics(self, user_id: str, days: int = 30) -> Dict:
        """Get performance analytics for user"""
        
        if not self.db:
            return {}
        
        try:
            # Get content from last N days
            cutoff_date = datetime.now() - timedelta(days=days)
            
            # This is a simplified version - in production you'd use more complex queries
            docs = (self.db.collection('prosora_content')
                   .where('user_id', '==', user_id)
                   .where('timestamp', '>=', cutoff_date)
                   .stream())
            
            analytics = {
                'total_content': 0,
                'platforms': {},
                'avg_engagement': 0,
                'top_performing': []
            }
            
            for doc in docs:
                data = doc.to_dict()
                analytics['total_content'] += 1
                
                # Process platform data
                content = data.get('content', {})
                for platform in ['linkedin_posts', 'twitter_threads', 'blog_outlines']:
                    if platform in content and content[platform]:
                        analytics['platforms'][platform] = analytics['platforms'].get(platform, 0) + len(content[platform])
            
            return analytics
            
        except Exception as e:
            print(f"Error fetching analytics: {e}")
            return {}
    
    def create_email_notification_request(self, user_id: str, content: str, content_type: str):
        """Create email notification request"""
        
        if not self.db:
            return False
        
        try:
            self.db.collection('email_notifications').add({
                'user_id': user_id,
                'content': content,
                'content_type': content_type,
                'status': 'pending',
                'created_at': datetime.now()
            })
            
            return True
            
        except Exception as e:
            print(f"Error creating email notification: {e}")
            return False

class ProsoraAuthManager:
    """Handle OAuth and user authentication"""
    
    def __init__(self):
        self.setup_auth()
    
    def setup_auth(self):
        """Setup authentication"""
        # Placeholder for OAuth setup
        pass
    
    def google_oauth_login(self):
        """Handle Google OAuth login"""
        
        # Placeholder for Google OAuth
        # In production, you'd implement actual OAuth flow
        
        if 'user_authenticated' not in st.session_state:
            st.session_state.user_authenticated = False
        
        if not st.session_state.user_authenticated:
            st.markdown("### 🔐 Login to Prosora")
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🔑 Login with Google", key="google_login"):
                    # Simulate successful login
                    st.session_state.user_authenticated = True
                    st.session_state.user_id = "akash@prosora.in"
                    st.session_state.user_name = "Akash"
                    st.success("✅ Logged in successfully!")
                    st.rerun()
            
            return False
        
        return True
    
    def get_current_user(self) -> Dict:
        """Get current authenticated user"""
        
        if st.session_state.get('user_authenticated', False):
            return {
                'id': st.session_state.get('user_id', ''),
                'name': st.session_state.get('user_name', ''),
                'email': st.session_state.get('user_id', '')
            }
        
        return {}
    
    def logout(self):
        """Logout current user"""
        
        st.session_state.user_authenticated = False
        st.session_state.user_id = None
        st.session_state.user_name = None
        st.success("👋 Logged out successfully!")

# Firebase configuration helper
def setup_firebase_config():
    """Helper to setup Firebase configuration"""
    
    st.markdown("### 🔥 Firebase Configuration")
    
    st.write("To enable Firebase integration:")
    st.write("1. Create a Firebase project at https://console.firebase.google.com")
    st.write("2. Enable Firestore Database")
    st.write("3. Download service account key")
    st.write("4. Upload the key file or set environment variables")
    
    # File uploader for service account key
    uploaded_file = st.file_uploader("Upload Firebase Service Account Key", type=['json'])
    
    if uploaded_file:
        try:
            config_data = json.load(uploaded_file)
            
            # Save config (in production, store securely)
            with open("firebase_config.json", "w") as f:
                json.dump(config_data, f)
            
            st.success("✅ Firebase configuration saved!")
            st.info("Restart the application to apply changes.")
            
        except Exception as e:
            st.error(f"Error processing config file: {e}")
    
    # Manual configuration
    with st.expander("Manual Configuration"):
        project_id = st.text_input("Firebase Project ID")
        private_key = st.text_area("Private Key")
        client_email = st.text_input("Client Email")
        
        if st.button("Save Manual Config"):
            if project_id and private_key and client_email:
                config = {
                    "type": "service_account",
                    "project_id": project_id,
                    "private_key": private_key.replace("\\n", "\n"),
                    "client_email": client_email
                }
                
                with open("firebase_config.json", "w") as f:
                    json.dump(config, f)
                
                st.success("✅ Manual configuration saved!")

# Usage example
def demo_firebase_integration():
    """Demo Firebase integration"""
    
    # Initialize Firebase manager
    firebase_manager = ProsoraFirebaseManager("firebase_config.json")
    
    # Test saving content
    sample_content = {
        "linkedin_posts": [{"content": "Sample LinkedIn post", "evidence_count": 2}],
        "twitter_threads": [],
        "blog_outlines": []
    }
    
    # Save content
    doc_id = firebase_manager.save_generated_content("test_user", "AI regulation", sample_content)
    print(f"Saved content with ID: {doc_id}")
    
    # Get user content
    user_content = firebase_manager.get_user_content("test_user")
    print(f"Retrieved {len(user_content)} content items")
    
    return firebase_manager

if __name__ == "__main__":
    demo_firebase_integration()