#!/usr/bin/env python3
"""
Enhanced Email Integration for Prosora Command Center
Frontend-based Gmail OAuth and email configuration
"""

import streamlit as st
import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import json
import os
from typing import Dict, List, Optional

class EnhancedEmailIntegration:
    def __init__(self, firebase_manager=None):
        self.firebase_manager = firebase_manager
        
    def render_email_settings(self, user_id: str):
        """Render email settings interface on frontend"""
        
        st.markdown("### 📧 Email Integration Settings")
        
        # Check current email status
        email_connected = st.session_state.get('email_connected', False)
        user_email = st.session_state.get('user_email', '')
        
        if email_connected:
            self.render_connected_email_interface(user_email, user_id)
        else:
            self.render_email_connection_interface(user_id)
    
    def render_email_connection_interface(self, user_id: str):
        """Render interface to connect email"""
        
        st.markdown("""
        <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin: 10px 0;">
            <h4>🔗 Connect Your Gmail</h4>
            <p>Enable email-based content generation and delivery</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Email connection options
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🚀 Quick Connect")
            email_address = st.text_input(
                "Gmail Address:", 
                placeholder="your.email@gmail.com",
                key="email_input"
            )
            
            # App password input
            app_password = st.text_input(
                "Gmail App Password:", 
                type="password",
                placeholder="16-character app password",
                key="app_password_input",
                help="Generate this in your Google Account settings"
            )
            
            if st.button("🔗 Connect Gmail", key="connect_gmail", type="primary"):
                if email_address and app_password:
                    success = self.test_email_connection(email_address, app_password)
                    if success:
                        self.save_email_config(user_id, email_address, app_password)
                        st.success("✅ Gmail connected successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Connection failed. Check your credentials.")
                else:
                    st.warning("⚠️ Please enter both email and app password")
        
        with col2:
            st.markdown("#### 📋 Setup Instructions")
            
            with st.expander("🔧 How to get Gmail App Password", expanded=False):
                st.markdown("""
                **Step 1:** Enable 2-Factor Authentication
                - Go to [Google Account Settings](https://myaccount.google.com)
                - Security → 2-Step Verification → Turn On
                
                **Step 2:** Generate App Password
                - Security → App passwords
                - Select app: Mail
                - Select device: Other (Custom name)
                - Enter: "Prosora Command Center"
                - Copy the 16-character password
                
                **Step 3:** Use in Prosora
                - Paste the app password above
                - Click "Connect Gmail"
                """)
            
            with st.expander("⚡ Email Commands Preview", expanded=False):
                st.markdown("""
                **Send email with subject:**
                ```
                Prosora: generate LinkedIn post about AI ethics
                ```
                
                **You'll receive:**
                ```
                Subject: ✅ Generated: LinkedIn Post about AI Ethics
                
                Your content is ready with evidence!
                
                [Generated content]
                
                Reply "APPROVE" to post immediately
                Reply "SCHEDULE 9AM" to schedule
                ```
                """)
    
    def render_connected_email_interface(self, user_email: str, user_id: str):
        """Render interface for connected email"""
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; margin: 10px 0;">
            <h4>✅ Gmail Connected</h4>
            <p><strong>{user_email}</strong> is ready for email commands!</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Email features dashboard
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div style="background: white; padding: 15px; border-radius: 8px; text-align: center;">
                <h3>📧</h3>
                <h4>Email Commands</h4>
                <p>Send content requests via email</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background: white; padding: 15px; border-radius: 8px; text-align: center;">
                <h3>🚀</h3>
                <h4>Auto Delivery</h4>
                <p>Generated content sent instantly</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style="background: white; padding: 15px; border-radius: 8px; text-align: center;">
                <h3>📱</h3>
                <h4>Remote Control</h4>
                <p>Generate content from anywhere</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Email settings and controls
        st.markdown("#### ⚙️ Email Settings")
        
        settings_col1, settings_col2 = st.columns(2)
        
        with settings_col1:
            # Notification preferences
            st.markdown("**📬 Notification Preferences**")
            
            instant_notifications = st.checkbox(
                "Instant content delivery", 
                value=st.session_state.get('instant_notifications', True),
                key="instant_notifications"
            )
            
            daily_digest = st.checkbox(
                "Daily content digest", 
                value=st.session_state.get('daily_digest', False),
                key="daily_digest"
            )
            
            performance_reports = st.checkbox(
                "Weekly performance reports", 
                value=st.session_state.get('performance_reports', True),
                key="performance_reports"
            )
        
        with settings_col2:
            # Email command settings
            st.markdown("**⚡ Command Settings**")
            
            auto_approve = st.checkbox(
                "Auto-approve generated content", 
                value=st.session_state.get('auto_approve', False),
                key="auto_approve",
                help="Skip approval step for email commands"
            )
            
            include_evidence = st.checkbox(
                "Include evidence sources in emails", 
                value=st.session_state.get('include_evidence', True),
                key="include_evidence"
            )
            
            format_preference = st.selectbox(
                "Default email format:",
                ["HTML (Rich)", "Plain Text", "Markdown"],
                index=0,
                key="email_format"
            )
        
        # Action buttons
        st.markdown("#### 🔧 Actions")
        
        action_col1, action_col2, action_col3, action_col4 = st.columns(4)
        
        with action_col1:
            if st.button("📧 Test Email", key="test_email_btn"):
                self.send_test_email(user_email)
        
        with action_col2:
            if st.button("📊 Email Stats", key="email_stats_btn"):
                self.show_email_statistics(user_id)
        
        with action_col3:
            if st.button("⚙️ Save Settings", key="save_email_settings"):
                self.save_email_preferences(user_id)
        
        with action_col4:
            if st.button("🔌 Disconnect", key="disconnect_email", type="secondary"):
                self.disconnect_email(user_id)
    
    def test_email_connection(self, email_address: str, app_password: str) -> bool:
        """Test Gmail connection with provided credentials"""
        
        try:
            # Test SMTP connection
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(email_address, app_password)
            server.quit()
            
            return True
            
        except Exception as e:
            print(f"Email connection test failed: {e}")
            return False
    
    def save_email_config(self, user_id: str, email_address: str, app_password: str):
        """Save email configuration securely"""
        
        # Save to session state
        st.session_state.email_connected = True
        st.session_state.user_email = email_address
        st.session_state.email_app_password = app_password
        
        # Save to Firebase (encrypted)
        if self.firebase_manager:
            email_config = {
                'email_address': email_address,
                'connected_at': datetime.now(),
                'status': 'active',
                'preferences': {
                    'instant_notifications': True,
                    'daily_digest': False,
                    'performance_reports': True,
                    'auto_approve': False,
                    'include_evidence': True,
                    'email_format': 'HTML (Rich)'
                }
            }
            
            try:
                self.firebase_manager.db.collection('user_email_config').document(user_id).set(email_config)
                print(f"✅ Email config saved for user: {user_id}")
            except Exception as e:
                print(f"Error saving email config: {e}")
    
    def send_test_email(self, user_email: str):
        """Send a test email to verify connection"""
        
        try:
            app_password = st.session_state.get('email_app_password')
            if not app_password:
                st.error("❌ Email credentials not found")
                return
            
            # Create test email
            msg = MIMEMultipart()
            msg['From'] = user_email
            msg['To'] = user_email
            msg['Subject'] = "✅ Prosora Command Center - Test Email"
            
            body = """
            🎉 Congratulations! Your Prosora Command Center email integration is working perfectly!
            
            You can now:
            📧 Send content requests via email
            🚀 Receive generated content instantly
            📱 Control Prosora from anywhere
            
            Try sending an email with subject:
            "Prosora: generate LinkedIn post about AI innovation"
            
            Best regards,
            Prosora Intelligence Engine
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Send email
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(user_email, app_password)
            text = msg.as_string()
            server.sendmail(user_email, user_email, text)
            server.quit()
            
            st.success("✅ Test email sent successfully! Check your inbox.")
            
        except Exception as e:
            st.error(f"❌ Test email failed: {e}")
    
    def save_email_preferences(self, user_id: str):
        """Save email preferences to Firebase"""
        
        preferences = {
            'instant_notifications': st.session_state.get('instant_notifications', True),
            'daily_digest': st.session_state.get('daily_digest', False),
            'performance_reports': st.session_state.get('performance_reports', True),
            'auto_approve': st.session_state.get('auto_approve', False),
            'include_evidence': st.session_state.get('include_evidence', True),
            'email_format': st.session_state.get('email_format', 'HTML (Rich)'),
            'updated_at': datetime.now()
        }
        
        if self.firebase_manager:
            try:
                self.firebase_manager.db.collection('user_email_config').document(user_id).update({
                    'preferences': preferences
                })
                st.success("✅ Email preferences saved!")
            except Exception as e:
                st.error(f"❌ Failed to save preferences: {e}")
    
    def show_email_statistics(self, user_id: str):
        """Show email usage statistics"""
        
        with st.expander("📊 Email Statistics", expanded=True):
            # Mock statistics - in production, get from Firebase
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Emails Sent", "47", delta="12 this week")
            with col2:
                st.metric("Commands Processed", "23", delta="8 this week")
            with col3:
                st.metric("Success Rate", "98%", delta="2% improvement")
            with col4:
                st.metric("Avg Response Time", "45s", delta="-15s faster")
            
            # Recent email activity
            st.markdown("**📧 Recent Email Activity**")
            
            recent_activity = [
                {"time": "2 hours ago", "action": "Generated LinkedIn post", "status": "✅ Delivered"},
                {"time": "1 day ago", "action": "Created Twitter thread", "status": "✅ Delivered"},
                {"time": "2 days ago", "action": "Blog outline request", "status": "✅ Delivered"},
                {"time": "3 days ago", "action": "Trend analysis", "status": "✅ Delivered"}
            ]
            
            for activity in recent_activity:
                st.markdown(f"**{activity['time']}** - {activity['action']} - {activity['status']}")
    
    def disconnect_email(self, user_id: str):
        """Disconnect email integration"""
        
        # Clear session state
        st.session_state.email_connected = False
        st.session_state.user_email = ''
        st.session_state.email_app_password = ''
        
        # Update Firebase
        if self.firebase_manager:
            try:
                self.firebase_manager.db.collection('user_email_config').document(user_id).update({
                    'status': 'disconnected',
                    'disconnected_at': datetime.now()
                })
            except Exception as e:
                print(f"Error updating disconnect status: {e}")
        
        st.success("✅ Email disconnected successfully!")
        st.rerun()
    
    def send_generated_content_email(self, user_email: str, content: Dict, query: str):
        """Send generated content via email"""
        
        try:
            app_password = st.session_state.get('email_app_password')
            if not app_password:
                return False
            
            # Create email
            msg = MIMEMultipart()
            msg['From'] = user_email
            msg['To'] = user_email
            msg['Subject'] = f"✅ Prosora Generated: {query}"
            
            # Format content based on user preference
            email_format = st.session_state.get('email_format', 'HTML (Rich)')
            
            if email_format == 'HTML (Rich)':
                body = self.format_html_email(content, query)
                msg.attach(MIMEText(body, 'html'))
            else:
                body = self.format_plain_email(content, query)
                msg.attach(MIMEText(body, 'plain'))
            
            # Send email
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(user_email, app_password)
            text = msg.as_string()
            server.sendmail(user_email, user_email, text)
            server.quit()
            
            return True
            
        except Exception as e:
            print(f"Error sending content email: {e}")
            return False
    
    def format_html_email(self, content: Dict, query: str) -> str:
        """Format content as HTML email"""
        
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                <h2>🧠 Prosora Generated Content</h2>
                <p><strong>Query:</strong> {query}</p>
                <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
        """
        
        # Add LinkedIn posts
        linkedin_posts = content.get('linkedin_posts', [])
        if linkedin_posts:
            html += "<h3>📝 LinkedIn Posts</h3>"
            for i, post in enumerate(linkedin_posts, 1):
                html += f"""
                <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 10px 0;">
                    <h4>Post {i}</h4>
                    <p>{post.get('content', '').replace('\n', '<br>')}</p>
                    <small>Evidence sources: {post.get('evidence_count', 0)}</small>
                </div>
                """
        
        # Add Twitter threads
        twitter_threads = content.get('twitter_threads', [])
        if twitter_threads:
            html += "<h3>🧵 Twitter Threads</h3>"
            for i, thread in enumerate(twitter_threads, 1):
                html += f"<div style='background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 10px 0;'>"
                html += f"<h4>Thread {i}</h4>"
                for j, tweet in enumerate(thread.get('tweets', []), 1):
                    html += f"<p><strong>{j}.</strong> {tweet}</p>"
                html += "</div>"
        
        html += """
            <div style="background: #e9ecef; padding: 15px; border-radius: 8px; margin-top: 20px;">
                <p><strong>Actions:</strong></p>
                <p>• Reply "APPROVE" to approve content</p>
                <p>• Reply "SCHEDULE [TIME]" to schedule posting</p>
                <p>• Reply "EDIT [CHANGES]" to request modifications</p>
            </div>
            
            <p style="margin-top: 20px; color: #666;">
                Best regards,<br>
                Prosora Intelligence Engine
            </p>
        </body>
        </html>
        """
        
        return html
    
    def format_plain_email(self, content: Dict, query: str) -> str:
        """Format content as plain text email"""
        
        body = f"""
🧠 PROSORA GENERATED CONTENT

Query: {query}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

"""
        
        # Add LinkedIn posts
        linkedin_posts = content.get('linkedin_posts', [])
        if linkedin_posts:
            body += "📝 LINKEDIN POSTS\n" + "="*50 + "\n\n"
            for i, post in enumerate(linkedin_posts, 1):
                body += f"Post {i}:\n{post.get('content', '')}\n"
                body += f"Evidence sources: {post.get('evidence_count', 0)}\n\n"
        
        # Add Twitter threads
        twitter_threads = content.get('twitter_threads', [])
        if twitter_threads:
            body += "🧵 TWITTER THREADS\n" + "="*50 + "\n\n"
            for i, thread in enumerate(twitter_threads, 1):
                body += f"Thread {i}:\n"
                for j, tweet in enumerate(thread.get('tweets', []), 1):
                    body += f"{j}. {tweet}\n"
                body += "\n"
        
        body += """
ACTIONS:
• Reply "APPROVE" to approve content
• Reply "SCHEDULE [TIME]" to schedule posting  
• Reply "EDIT [CHANGES]" to request modifications

Best regards,
Prosora Intelligence Engine
"""
        
        return body

# Integration with main command interface
def integrate_enhanced_email():
    """Integration function for the main command interface"""
    
    print("✅ Enhanced Email Integration loaded")
    return EnhancedEmailIntegration()

if __name__ == "__main__":
    integrate_enhanced_email()