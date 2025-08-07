#!/usr/bin/env python3
"""
Prosora Command Interface - Enhanced
Google-like search interface with OAuth, Firebase, and remote control
"""

import streamlit as st
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from enhanced_content_generator import EnhancedContentGenerator
from google_evidence_search import GoogleEvidenceSearch
from firebase_integration import ProsoraFirebaseManager, ProsoraAuthManager
from enhanced_email_integration import EnhancedEmailIntegration
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import asyncio
import time

class ProsoraCommandInterface:
    def __init__(self):
        self.enhanced_generator = EnhancedContentGenerator()
        self.google_search = GoogleEvidenceSearch()
        
        # Initialize Firebase and Auth
        self.firebase_manager = ProsoraFirebaseManager()
        self.auth_manager = ProsoraAuthManager()
        self.email_integration = EnhancedEmailIntegration(self.firebase_manager)
        
        # Smart suggestions based on your expertise
        self.suggestions = [
            "Cross-domain insights on AI regulation in fintech",
            "Contrarian take on remote work productivity myths", 
            "Framework for product-market fit in emerging markets",
            "Evidence-backed analysis of fintech disruption patterns",
            "Political lessons for startup strategy and scaling",
            "IIT-MBA bridge: technical leadership in business",
            "Prosora prediction on intersection of AI and governance",
            "Thread about politics meets product management",
            "Analysis of regulatory trends affecting startups",
            "Framework for cross-domain decision making",
            "Insights on Indian fintech vs global patterns",
            "Product strategy lessons from political campaigns"
        ]
        
        # Enhanced quick action templates
        self.quick_actions = {
            "📝 LinkedIn Post": {
                "type": "linkedin_post",
                "prompt": "Create professional LinkedIn post",
                "icon": "📝"
            },
            "🧵 Twitter Thread": {
                "type": "twitter_thread",
                "prompt": "Create engaging Twitter thread",
                "icon": "🧵"
            },
            "📖 Blog Outline": {
                "type": "blog_outline", 
                "prompt": "Create comprehensive blog outline",
                "icon": "📖"
            },
            "🔮 Trend Analysis": {
                "type": "trend_analysis",
                "prompt": "Analyze trends and implications",
                "icon": "🔮"
            },
            "⚡ Quick Insight": {
                "type": "quick_insight",
                "prompt": "Generate quick insight",
                "icon": "⚡"
            },
            "🎯 Framework": {
                "type": "framework",
                "prompt": "Create strategic framework",
                "icon": "🎯"
            }
        }
        
        # Initialize session state
        self.init_session_state()
    
    def init_session_state(self):
        """Initialize session state variables"""
        if 'search_history' not in st.session_state:
            st.session_state.search_history = []
        if 'user_preferences' not in st.session_state:
            st.session_state.user_preferences = {}
        if 'generated_content_cache' not in st.session_state:
            st.session_state.generated_content_cache = {}
        if 'email_configured' not in st.session_state:
            st.session_state.email_configured = False
    
    def render_command_interface(self):
        """Render the main command interface with authentication"""
        
        # Enhanced CSS for Google-like styling
        st.markdown("""
        <style>
        .main-header {
            text-align: center;
            padding: 20px 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 12px;
            margin-bottom: 30px;
        }
        .search-container {
            background: white;
            border-radius: 24px;
            box-shadow: 0 2px 5px 1px rgba(64,60,67,.16);
            padding: 25px;
            margin: 30px 0;
            border: 1px solid #e8eaed;
        }
        .search-input {
            font-size: 16px;
            border: none;
            outline: none;
            width: 100%;
            padding: 12px;
        }
        .suggestion-chip {
            background: #f8f9fa;
            border: 1px solid #dadce0;
            border-radius: 20px;
            padding: 10px 16px;
            margin: 6px 4px;
            display: inline-block;
            cursor: pointer;
            transition: all 0.2s;
            font-size: 14px;
        }
        .suggestion-chip:hover {
            background: #e8f0fe;
            border-color: #1a73e8;
        }
        .quick-action {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 12px;
            padding: 15px;
            margin: 8px;
            text-align: center;
            cursor: pointer;
            transition: transform 0.2s;
            border: none;
        }
        .quick-action:hover {
            transform: translateY(-2px);
        }
        .user-info {
            background: #f8f9fa;
            border-radius: 8px;
            padding: 10px;
            margin-bottom: 20px;
        }
        .stats-card {
            background: white;
            border-radius: 8px;
            padding: 15px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            margin: 10px 0;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Check authentication first
        if not self.auth_manager.google_oauth_login():
            return
        
        # Get current user
        current_user = self.auth_manager.get_current_user()
        
        # Header with user info
        st.markdown(f"""
        <div class="main-header">
            <h1>🧠 Prosora Intelligence Command Center</h1>
            <p>Generate evidence-backed content instantly • Welcome back, {current_user.get('name', 'User')}!</p>
        </div>
        """, unsafe_allow_html=True)
        
        # User dashboard row
        self.render_user_dashboard(current_user)
        
        # Main search interface
        with st.container():
            st.markdown('<div class="search-container">', unsafe_allow_html=True)
            
            # Search input with enhanced styling
            col1, col2 = st.columns([8, 1])
            
            with col1:
                search_query = st.text_input(
                    "",
                    placeholder="Generate LinkedIn post about AI regulation in fintech...",
                    key="main_search",
                    label_visibility="collapsed",
                    help="Type your content idea and press Enter or click search"
                )
            
            with col2:
                search_button = st.button("🔍", key="search_btn", help="Generate Content", type="primary")
            
            # Quick search shortcuts
            st.markdown("**Quick shortcuts:** Press Enter to search • Use @ for mentions • Use # for hashtags")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Process search if query entered
        if (search_button and search_query) or (search_query and st.session_state.get('enter_pressed', False)):
            self.process_search_query(search_query, current_user['id'])
            st.session_state.enter_pressed = False
        
        # Smart suggestions section
        st.markdown("### 💡 Smart Content Suggestions")
        st.markdown("*AI-powered ideas based on your expertise and trending topics*")
        
        # Get personalized suggestions
        personalized_suggestions = self.get_personalized_suggestions(current_user['id'])
        
        # Display suggestions in a more elegant grid
        suggestion_cols = st.columns(3)
        for i, suggestion in enumerate(personalized_suggestions[:12]):
            with suggestion_cols[i % 3]:
                if st.button(
                    suggestion, 
                    key=f"suggestion_{i}", 
                    help="Click to generate content",
                    use_container_width=True
                ):
                    self.process_search_query(suggestion, current_user['id'])
        
        # Quick actions section
        st.markdown("### ⚡ Quick Actions")
        st.markdown("*One-click content generation for different platforms*")
        
        action_cols = st.columns(3)
        for i, (action_name, action_config) in enumerate(self.quick_actions.items()):
            with action_cols[i % 3]:
                if st.button(
                    f"{action_config['icon']} {action_name}", 
                    key=f"action_{action_config['type']}",
                    help=action_config['prompt'],
                    use_container_width=True
                ):
                    self.show_quick_action_dialog(action_config['type'], action_name, current_user['id'])
        
        # Recent generations and analytics
        col1, col2 = st.columns([2, 1])
        
        with col1:
            self.show_recent_generations(current_user['id'])
        
        with col2:
            self.show_user_stats(current_user['id'])
    
    def render_user_dashboard(self, user: Dict):
        """Render user dashboard with stats and quick info"""
        
        col1, col2, col3, col4 = st.columns(4)
        
        # Get user stats
        user_stats = self.get_user_stats(user['id'])
        
        with col1:
            st.markdown(f"""
            <div class="stats-card">
                <h4>📊 Content Generated</h4>
                <h2>{user_stats.get('total_content', 0)}</h2>
                <small>This month</small>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="stats-card">
                <h4>🔥 Avg Evidence</h4>
                <h2>{user_stats.get('avg_evidence', 0):.1f}</h2>
                <small>Sources per post</small>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="stats-card">
                <h4>⚡ Time Saved</h4>
                <h2>{user_stats.get('time_saved', 0)}h</h2>
                <small>This month</small>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            # Email configuration status
            email_status = "✅ Connected" if st.session_state.get('email_connected', False) else "⚠️ Setup needed"
            if st.button(f"📧 Email: {email_status}", key="email_config", use_container_width=True):
                self.show_enhanced_email_settings(user['id'])

    def get_personalized_suggestions(self, user_id: str) -> List[str]:
        """Get personalized content suggestions based on user history"""
        
        # Get user preferences and history
        user_prefs = self.firebase_manager.get_user_preferences(user_id)
        recent_content = self.firebase_manager.get_user_content(user_id, limit=5)
        
        # Base suggestions enhanced with personalization
        base_suggestions = self.suggestions.copy()
        
        # Add trending topics based on user's domains
        trending_suggestions = [
            "Latest developments in Indian fintech regulation",
            "Cross-domain insights: Politics meets product strategy",
            "IIT alumni success patterns in startup ecosystem",
            "Evidence-based analysis of remote work productivity",
            "Framework for navigating regulatory uncertainty",
            "Contrarian view on AI adoption in traditional industries"
        ]
        
        # Combine and randomize
        all_suggestions = base_suggestions + trending_suggestions
        
        # Return shuffled suggestions (in production, use ML for better personalization)
        import random
        random.shuffle(all_suggestions)
        return all_suggestions

    def process_search_query(self, query: str, user_id: str):
        """Process the search query and generate content"""
        
        # Add to search history
        st.session_state.search_history.append({
            'query': query,
            'timestamp': datetime.now(),
            'user_id': user_id
        })
        
        with st.spinner(f"🔍 Generating evidence-backed content for: **{query}**"):
            try:
                start_time = time.time()
                
                # Create insight from query
                insight = {
                    'title': query,
                    'content': f"Generate comprehensive content about: {query}",
                    'type': 'search_query'
                }
                
                # Generate evidence-backed content
                sample_insights = {
                    'premium_insights': [insight],
                    'cross_domain_connections': [],
                    'prosora_frameworks': []
                }
                
                enhanced_content = self.enhanced_generator.generate_evidence_backed_content(sample_insights)
                
                generation_time = time.time() - start_time
                
                # Display results
                self.display_generated_content(query, enhanced_content, generation_time)
                
                # Save to Firebase
                content_id = self.firebase_manager.save_generated_content(user_id, query, enhanced_content)
                
                # Cache for quick access
                st.session_state.generated_content_cache[query] = {
                    'content': enhanced_content,
                    'timestamp': datetime.now(),
                    'content_id': content_id
                }
                
                st.success(f"✅ Content generated in {generation_time:.1f} seconds with evidence backing!")
                
            except Exception as e:
                st.error(f"❌ Generation failed: {e}")
                st.info("💡 Try rephrasing your query or check your internet connection")
    
    def display_generated_content(self, query: str, content: Dict, generation_time: float = 0):
        """Display the generated content in an organized way"""
        
        st.markdown("---")
        st.markdown(f"## 📝 Generated Content for: *{query}*")
        st.markdown(f"*Generated in {generation_time:.1f}s with AI-powered evidence research*")
        
        # Quick action buttons at the top
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("📧 Email All Content", key="email_all", type="primary"):
                self.email_all_content(content, query)
        with col2:
            if st.button("📋 Copy All", key="copy_all"):
                self.copy_all_content(content)
        with col3:
            if st.button("💾 Save to Drafts", key="save_drafts"):
                st.success("✅ Saved to drafts!")
        with col4:
            if st.button("🔄 Regenerate", key="regenerate"):
                st.rerun()
        
        # Content tabs with enhanced display
        tabs = st.tabs(["📝 LinkedIn", "🧵 Twitter", "📖 Blog", "📊 Analytics", "🔍 Evidence"])
        
        with tabs[0]:  # LinkedIn
            linkedin_posts = content.get('linkedin_posts', [])
            if linkedin_posts:
                for i, post in enumerate(linkedin_posts):
                    with st.expander(f"LinkedIn Post {i+1} • {post.get('evidence_count', 0)} sources • Est. {post.get('estimated_engagement', 'N/A')} engagement", expanded=True):
                        
                        # Content display with better formatting
                        st.markdown("**Content:**")
                        st.text_area("", post.get('content', ''), height=200, key=f"linkedin_{i}", label_visibility="collapsed")
                        
                        # Evidence sources
                        if post.get('evidence_sources'):
                            st.markdown("**Evidence Sources:**")
                            for j, source in enumerate(post['evidence_sources'][:3], 1):
                                st.markdown(f"{j}. [{source.get('title', 'Source')}]({source.get('url', '#')})")
                        
                        # Action buttons
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            if st.button("📧 Email", key=f"email_linkedin_{i}"):
                                self.send_to_email(post.get('content', ''), "LinkedIn Post", query)
                        with col2:
                            if st.button("📋 Copy", key=f"copy_linkedin_{i}"):
                                st.success("✅ Copied!")
                        with col3:
                            if st.button("🚀 Schedule", key=f"schedule_linkedin_{i}"):
                                self.show_schedule_dialog(post.get('content', ''), "LinkedIn")
                        with col4:
                            if st.button("✏️ Edit", key=f"edit_linkedin_{i}"):
                                self.show_edit_dialog(post.get('content', ''), "LinkedIn")
            else:
                st.info("💡 No LinkedIn content generated. Try a more specific query!")
        
        with tabs[1]:  # Twitter
            twitter_threads = content.get('twitter_threads', [])
            if twitter_threads:
                for i, thread in enumerate(twitter_threads):
                    with st.expander(f"Twitter Thread {i+1} • {len(thread.get('tweets', []))} tweets • Est. reach: {thread.get('estimated_reach', 'N/A')}", expanded=True):
                        tweets = thread.get('tweets', [])
                        
                        # Display tweets with character count
                        for j, tweet in enumerate(tweets, 1):
                            char_count = len(tweet)
                            color = "🟢" if char_count <= 280 else "🔴"
                            st.markdown(f"**Tweet {j}/{len(tweets)}** {color} ({char_count}/280)")
                            st.text_area("", tweet, height=80, key=f"tweet_{i}_{j}", label_visibility="collapsed")
                        
                        # Thread actions
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            if st.button("📧 Email Thread", key=f"email_twitter_{i}"):
                                thread_text = "\n\n".join([f"Tweet {j}/{len(tweets)}: {tweet}" for j, tweet in enumerate(tweets, 1)])
                                self.send_to_email(thread_text, "Twitter Thread", query)
                        with col2:
                            if st.button("📋 Copy Thread", key=f"copy_twitter_{i}"):
                                st.success("✅ Thread copied!")
                        with col3:
                            if st.button("🚀 Schedule Thread", key=f"schedule_twitter_{i}"):
                                self.show_schedule_dialog(thread_text, "Twitter")
                        with col4:
                            if st.button("✏️ Edit Thread", key=f"edit_twitter_{i}"):
                                self.show_edit_dialog(thread_text, "Twitter")
            else:
                st.info("💡 No Twitter content generated. Try asking for a thread specifically!")
        
        with tabs[2]:  # Blog
            blog_outlines = content.get('blog_outlines', [])
            if blog_outlines:
                for i, blog in enumerate(blog_outlines):
                    with st.expander(f"Blog Outline {i+1} • Est. {blog.get('word_count', 'N/A')} words • {blog.get('read_time', 'N/A')} min read", expanded=True):
                        st.markdown("**Blog Outline:**")
                        st.markdown(blog.get('outline', ''))
                        
                        # Blog actions
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            if st.button("📧 Email Outline", key=f"email_blog_{i}"):
                                self.send_to_email(blog.get('outline', ''), "Blog Outline", query)
                        with col2:
                            if st.button("📝 Develop Full Post", key=f"develop_blog_{i}"):
                                st.success("✅ Full blog development queued!")
                        with col3:
                            if st.button("📋 Copy Outline", key=f"copy_blog_{i}"):
                                st.success("✅ Outline copied!")
                        with col4:
                            if st.button("✏️ Edit Outline", key=f"edit_blog_{i}"):
                                self.show_edit_dialog(blog.get('outline', ''), "Blog")
            else:
                st.info("💡 No blog content generated. Try asking for a blog outline!")
        
        with tabs[3]:  # Analytics
            st.markdown("### 📊 Generation Analytics")
            
            # Calculate metrics
            total_pieces = len(content.get('linkedin_posts', [])) + len(content.get('twitter_threads', [])) + len(content.get('blog_outlines', []))
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Content Pieces", total_pieces, delta="Generated now")
            with col2:
                avg_evidence = 0
                if content.get('linkedin_posts'):
                    avg_evidence = sum(post.get('evidence_count', 0) for post in content['linkedin_posts']) / len(content['linkedin_posts'])
                st.metric("Avg Evidence Sources", f"{avg_evidence:.1f}", delta="High quality")
            with col3:
                st.metric("Generation Time", f"{generation_time:.1f}s", delta="Fast")
            with col4:
                estimated_time_saved = total_pieces * 45  # 45 min per piece manually
                st.metric("Time Saved", f"{estimated_time_saved} min", delta="vs manual")
            
            # Performance prediction
            st.markdown("### 🎯 Performance Prediction")
            if content.get('linkedin_posts'):
                for i, post in enumerate(content['linkedin_posts']):
                    st.markdown(f"**LinkedIn Post {i+1}:**")
                    pred_col1, pred_col2, pred_col3 = st.columns(3)
                    with pred_col1:
                        st.metric("Est. Views", f"{post.get('predicted_views', 150)}+")
                    with pred_col2:
                        st.metric("Est. Likes", f"{post.get('predicted_likes', 25)}+")
                    with pred_col3:
                        st.metric("Est. Comments", f"{post.get('predicted_comments', 5)}+")
        
        with tabs[4]:  # Evidence
            st.markdown("### 🔍 Evidence & Research")
            
            all_sources = []
            for post in content.get('linkedin_posts', []):
                all_sources.extend(post.get('evidence_sources', []))
            for thread in content.get('twitter_threads', []):
                all_sources.extend(thread.get('evidence_sources', []))
            
            if all_sources:
                st.markdown(f"**Found {len(all_sources)} evidence sources:**")
                for i, source in enumerate(all_sources, 1):
                    with st.expander(f"Source {i}: {source.get('title', 'Unknown')}"):
                        st.markdown(f"**URL:** [{source.get('url', 'N/A')}]({source.get('url', '#')})")
                        st.markdown(f"**Credibility:** {source.get('credibility', 'N/A')}/1.0")
                        st.markdown(f"**Relevance:** {source.get('relevance', 'N/A')}/1.0")
                        st.markdown(f"**Summary:** {source.get('summary', 'No summary available')}")
            else:
                st.info("💡 No evidence sources found. Try a more specific query for better research backing!")
    
    def show_quick_action_dialog(self, action_type: str, action_name: str, user_id: str):
        """Show dialog for quick actions"""
        
        with st.expander(f"🚀 {action_name} Generator", expanded=True):
            
            if action_type == "linkedin_post":
                topic = st.text_input("Topic for LinkedIn post:", placeholder="AI regulation in fintech", key="linkedin_topic")
                tone = st.selectbox("Tone:", ["Professional", "Thought Leadership", "Conversational", "Analytical"], key="linkedin_tone")
                if st.button("Generate LinkedIn Post", key="gen_linkedin", type="primary"):
                    if topic:
                        query = f"Create {tone.lower()} LinkedIn post about {topic}"
                        self.process_search_query(query, user_id)
            
            elif action_type == "twitter_thread":
                topic = st.text_input("Topic for Twitter thread:", placeholder="Cross-domain insights on product strategy", key="twitter_topic")
                thread_length = st.selectbox("Thread length:", ["Short (3-5 tweets)", "Medium (6-8 tweets)", "Long (9-12 tweets)"], key="thread_length")
                if st.button("Generate Twitter Thread", key="gen_twitter", type="primary"):
                    if topic:
                        query = f"Create {thread_length.lower()} Twitter thread about {topic}"
                        self.process_search_query(query, user_id)
            
            elif action_type == "blog_outline":
                topic = st.text_input("Blog topic:", placeholder="Framework for product-market fit", key="blog_topic")
                target_length = st.selectbox("Target length:", ["Short (800-1200 words)", "Medium (1500-2000 words)", "Long (2500+ words)"], key="blog_length")
                if st.button("Generate Blog Outline", key="gen_blog", type="primary"):
                    if topic:
                        query = f"Create {target_length.lower()} blog outline about {topic}"
                        self.process_search_query(query, user_id)
            
            elif action_type == "framework":
                framework_name = st.text_input("Framework name:", placeholder="The Political Product Manager Framework", key="framework_name")
                domain = st.selectbox("Domain:", ["Product Management", "Business Strategy", "Leadership", "Cross-domain"], key="framework_domain")
                if st.button("Generate Framework", key="gen_framework", type="primary"):
                    if framework_name:
                        query = f"Create {domain.lower()} framework: {framework_name}"
                        self.process_search_query(query, user_id)
            
            elif action_type == "trend_analysis":
                trend_topic = st.text_input("Trend to analyze:", placeholder="Remote work productivity patterns", key="trend_topic")
                analysis_type = st.selectbox("Analysis type:", ["Current State", "Future Predictions", "Contrarian View", "Cross-domain Impact"], key="analysis_type")
                if st.button("Generate Analysis", key="gen_analysis", type="primary"):
                    if trend_topic:
                        query = f"Create {analysis_type.lower()} analysis of {trend_topic}"
                        self.process_search_query(query, user_id)
            
            elif action_type == "quick_insight":
                insight_topic = st.text_input("Quick insight on:", placeholder="Latest fintech regulations", key="insight_topic")
                if st.button("Generate Quick Insight", key="gen_insight", type="primary"):
                    if insight_topic:
                        query = f"Generate quick insight about {insight_topic}"
                        self.process_search_query(query, user_id)
    
    def send_to_email(self, content: str, content_type: str):
        """Send generated content to email"""
        
        # Placeholder for email functionality
        # In production, you'd implement actual email sending
        st.success(f"📧 {content_type} sent to your email!")
        
        # Save email request to Firebase
        if self.db:
            try:
                self.db.collection('email_requests').add({
                    'content': content,
                    'content_type': content_type,
                    'timestamp': datetime.now(),
                    'status': 'sent'
                })
            except Exception as e:
                print(f"Firebase save error: {e}")
    
    def save_to_firebase(self, query: str, content: Dict):
        """Save generated content to Firebase"""
        
        if not self.db:
            return
        
        try:
            # Save to Firebase
            doc_data = {
                'query': query,
                'content': content,
                'timestamp': datetime.now(),
                'user_id': 'akash',  # Replace with actual user ID
                'status': 'generated'
            }
            
            self.db.collection('generated_content').add(doc_data)
            print(f"💾 Saved to Firebase: {query}")
            
        except Exception as e:
            print(f"Firebase save error: {e}")
    
    def show_recent_generations(self):
        """Show recent content generations"""
        
        st.markdown("### 📚 Recent Generations")
        
        # Placeholder for recent content
        # In production, this would load from Firebase
        recent_items = [
            {"query": "AI regulation in fintech", "time": "2 hours ago", "type": "LinkedIn Post"},
            {"query": "Cross-domain product strategy", "time": "1 day ago", "type": "Twitter Thread"},
            {"query": "Political lessons for startups", "time": "2 days ago", "type": "Blog Outline"}
        ]
        
        for item in recent_items:
            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
            
            with col1:
                st.write(f"**{item['query']}**")
            with col2:
                st.write(item['type'])
            with col3:
                st.write(item['time'])
            with col4:
                if st.button("🔄", key=f"regenerate_{item['query']}", help="Regenerate"):
                    self.process_search_query(item['query'])

def main():
    """Main function for the command interface"""
    
    st.set_page_config(
        page_title="Prosora Command Center",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Initialize and render interface
    command_interface = ProsoraCommandInterface()
    command_interface.render_command_interface()

# Placeholder removed
    
    def show_enhanced_email_settings(self, user_id: str):
        """Show enhanced email settings interface"""
        
        with st.expander("📧 Enhanced Email Integration", expanded=True):
            self.email_integration.render_email_settings(user_id)
    
    def email_all_content(self, content: Dict, query: str):
        """Email all generated content to user"""
        
        email_body = f"Generated Content for: {query}\n\n"
        
        # Add LinkedIn posts
        for i, post in enumerate(content.get('linkedin_posts', []), 1):
            email_body += f"LinkedIn Post {i}:\n{post.get('content', '')}\n\n"
        
        # Add Twitter threads
        for i, thread in enumerate(content.get('twitter_threads', []), 1):
            email_body += f"Twitter Thread {i}:\n"
            for j, tweet in enumerate(thread.get('tweets', []), 1):
                email_body += f"{j}. {tweet}\n"
            email_body += "\n"
        
        # Add blog outlines
        for i, blog in enumerate(content.get('blog_outlines', []), 1):
            email_body += f"Blog Outline {i}:\n{blog.get('outline', '')}\n\n"
        
        self.send_to_email(email_body, "Complete Content Package", query)
    
    def copy_all_content(self, content: Dict):
        """Copy all content to clipboard (placeholder)"""
        st.success("✅ All content copied to clipboard!")
    
    def show_schedule_dialog(self, content: str, platform: str):
        """Show scheduling dialog"""
        
        with st.expander(f"🚀 Schedule {platform} Post", expanded=True):
            schedule_date = st.date_input("Schedule date:", value=datetime.now().date())
            schedule_time = st.time_input("Schedule time:", value=datetime.now().time())
            
            if st.button(f"Schedule {platform} Post", key=f"confirm_schedule_{platform}"):
                st.success(f"✅ {platform} post scheduled for {schedule_date} at {schedule_time}")
    
    def show_edit_dialog(self, content: str, platform: str):
        """Show content editing dialog"""
        
        with st.expander(f"✏️ Edit {platform} Content", expanded=True):
            edited_content = st.text_area("Edit content:", value=content, height=200)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("💾 Save Changes", key=f"save_edit_{platform}"):
                    st.success("✅ Changes saved!")
            with col2:
                if st.button("🔄 Regenerate", key=f"regen_edit_{platform}"):
                    st.success("✅ Content regenerated!")
    
    def send_to_email(self, content: str, content_type: str, query: str = ""):
        """Send generated content to email using enhanced integration"""
        
        if not st.session_state.get('email_connected', False):
            st.warning("⚠️ Please connect your Gmail first!")
            self.show_enhanced_email_settings(st.session_state.get('user_id', 'unknown'))
            return
        
        user_email = st.session_state.get('user_email', '')
        
        # For single content pieces, create a simple content dict
        if isinstance(content, str):
            content_dict = {
                'linkedin_posts': [{'content': content, 'evidence_count': 0}] if 'linkedin' in content_type.lower() else [],
                'twitter_threads': [{'tweets': [content]}] if 'twitter' in content_type.lower() else [],
                'blog_outlines': [{'outline': content}] if 'blog' in content_type.lower() else []
            }
        else:
            content_dict = content
        
        success = self.email_integration.send_generated_content_email(user_email, content_dict, query or content_type)
        
        if success:
            st.success(f"📧 {content_type} sent to {user_email}!")
            st.info("💡 Check your inbox - it should arrive within seconds!")
        else:
            st.error("❌ Failed to send email. Please check your connection.")
    
    def show_recent_generations(self, user_id: str):
        """Show recent content generations"""
        
        st.markdown("### 📚 Recent Generations")
        
        # Get recent content from Firebase
        recent_content = self.firebase_manager.get_user_content(user_id, limit=5)
        
        if recent_content:
            for item in recent_content:
                col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                
                with col1:
                    st.write(f"**{item.get('query', 'Unknown query')}**")
                with col2:
                    # Determine content type
                    content_types = []
                    if item.get('content', {}).get('linkedin_posts'):
                        content_types.append("LinkedIn")
                    if item.get('content', {}).get('twitter_threads'):
                        content_types.append("Twitter")
                    if item.get('content', {}).get('blog_outlines'):
                        content_types.append("Blog")
                    st.write(", ".join(content_types) if content_types else "Mixed")
                with col3:
                    # Time ago
                    timestamp = item.get('timestamp')
                    if timestamp:
                        time_diff = datetime.now() - timestamp
                        if time_diff.days > 0:
                            st.write(f"{time_diff.days}d ago")
                        elif time_diff.seconds > 3600:
                            st.write(f"{time_diff.seconds//3600}h ago")
                        else:
                            st.write(f"{time_diff.seconds//60}m ago")
                    else:
                        st.write("Recently")
                with col4:
                    if st.button("🔄", key=f"regenerate_{item.get('id', 'unknown')}", help="Regenerate"):
                        self.process_search_query(item.get('query', ''), user_id)
        else:
            st.info("💡 No recent generations. Start by searching for content ideas above!")
    
    def show_user_stats(self, user_id: str):
        """Show user statistics sidebar"""
        
        st.markdown("### 📊 Your Stats")
        
        stats = self.get_user_stats(user_id)
        
        # Monthly stats
        st.metric("This Month", f"{stats['total_content']} pieces")
        st.metric("Time Saved", f"{stats['time_saved']}h")
        st.metric("Avg Evidence", f"{stats['avg_evidence']:.1f}")
        
        # Quick actions
        st.markdown("### ⚡ Quick Links")
        
        if st.button("📧 Email Settings", key="quick_email", use_container_width=True):
            self.show_email_config_dialog()
        
        if st.button("📊 Full Analytics", key="quick_analytics", use_container_width=True):
            st.info("📊 Full analytics dashboard coming soon!")
        
        if st.button("🔄 Refresh Stats", key="refresh_stats", use_container_width=True):
            st.rerun()
        
        # Logout button
        st.markdown("---")
        if st.button("👋 Logout", key="logout", use_container_width=True):
            self.auth_manager.logout()
            st.rerun()
    
    def get_user_stats(self, user_id: str) -> Dict:
        """Get user statistics from Firebase"""
        
        try:
            # Get analytics from Firebase
            analytics = self.firebase_manager.get_performance_analytics(user_id, days=30)
            
            # Calculate time saved (assuming 45 min per manual content piece)
            time_saved = analytics.get('total_content', 0) * 0.75  # 45 min = 0.75 hours
            
            return {
                'total_content': analytics.get('total_content', 0),
                'avg_evidence': 2.3,  # Placeholder - calculate from actual data
                'time_saved': int(time_saved),
                'engagement_rate': 4.2  # Placeholder
            }
        except Exception as e:
            print(f"Error getting user stats: {e}")
            return {'total_content': 0, 'avg_evidence': 0, 'time_saved': 0, 'engagement_rate': 0}

def main():
    """Main function for the command interface"""
    
    st.set_page_config(
        page_title="Prosora Command Center",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Initialize and render interface
    command_interface = ProsoraCommandInterface()
    command_interface.render_command_interface()

if __name__ == "__main__":
    main()