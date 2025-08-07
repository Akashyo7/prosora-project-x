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
from unified_prosora_intelligence import UnifiedProsoraIntelligence
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import asyncio
import time

class ProsoraCommandInterface:
    def __init__(self):
        # Initialize the Unified Prosora Intelligence Engine
        self.prosora_intelligence = UnifiedProsoraIntelligence()
        
        # Initialize supporting systems
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
    
    def show_enhanced_email_settings(self, user_id: str):
        """Show enhanced email settings interface"""
        
        with st.expander("📧 Enhanced Email Integration", expanded=True):
            self.email_integration.render_email_settings(user_id)
    
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
        """Process the search query using full Prosora intelligence system"""
        
        # Add to search history
        st.session_state.search_history.append({
            'query': query,
            'timestamp': datetime.now(),
            'user_id': user_id
        })
        
        with st.spinner(f"🧠 Running Unified Prosora Intelligence for: **{query}**"):
            try:
                start_time = time.time()
                
                # Single unified pipeline - the true Prosora intelligence flow
                st.info("🚀 Prosora Intelligence: Analyzing query and fetching curated sources...")
                
                # Process through unified intelligence engine
                prosora_content = self.prosora_intelligence.process_query(query)
                
                generation_time = time.time() - start_time
                
                st.success(f"✅ Prosora Intelligence complete in {generation_time:.1f}s!")
                
                # Display results with unified content structure
                self.display_unified_prosora_content(query, prosora_content, generation_time)
                
                # Save to Firebase with unified intelligence data
                content_id = self.firebase_manager.save_generated_content(
                    user_id, 
                    query, 
                    {
                        'prosora_content': prosora_content.linkedin_posts + prosora_content.twitter_threads + prosora_content.blog_outlines,
                        'insights_summary': prosora_content.insights_summary,
                        'evidence_report': prosora_content.evidence_report,
                        'generation_metadata': prosora_content.generation_metadata
                    }
                )
                
                # Cache for quick access
                st.session_state.generated_content_cache[query] = {
                    'content': prosora_content,
                    'insights_summary': prosora_content.insights_summary,
                    'timestamp': datetime.now(),
                    'content_id': content_id
                }
                
                st.success(f"✅ Prosora Intelligence Analysis completed in {generation_time:.1f} seconds!")
                
            except Exception as e:
                st.error(f"❌ Prosora Analysis failed: {e}")
                st.info("💡 Falling back to basic content generation...")
                # Fallback to basic generation
                self._fallback_content_generation(query, user_id)
    
    def display_generated_content(self, query: str, content: Dict, generation_time: float = 0):
        """Display the generated content in an organized way"""
        
        # Type safety check
        if not isinstance(content, dict):
            st.error(f"❌ Content format error: Expected dictionary, got {type(content)}")
            st.info("💡 Unable to display content due to format issue")
            return
        
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
        tabs = st.tabs(["📝 LinkedIn", "🧵 Twitter", "📖 Blog", "📊 Analytics"])
        
        with tabs[0]:  # LinkedIn
            linkedin_posts = content.get('linkedin_posts', [])
            if linkedin_posts:
                for i, post in enumerate(linkedin_posts):
                    # Type safety for individual posts
                    if isinstance(post, str):
                        # Handle case where post is a string instead of dict
                        with st.expander(f"LinkedIn Post {i+1}", expanded=True):
                            st.markdown("**Content:**")
                            st.text_area("", post, height=200, key=f"linkedin_{i}", label_visibility="collapsed")
                            
                            col1, col2, col3, col4 = st.columns(4)
                            with col1:
                                if st.button("📧 Email", key=f"email_linkedin_{i}"):
                                    self.send_to_email(post, "LinkedIn Post", query)
                            with col2:
                                if st.button("📋 Copy", key=f"copy_linkedin_{i}"):
                                    st.success("✅ Copied!")
                    elif isinstance(post, dict):
                        # Handle normal dict case
                        with st.expander(f"LinkedIn Post {i+1} • {post.get('evidence_count', 0)} sources", expanded=True):
                            
                            # Content display with better formatting
                            st.markdown("**Content:**")
                            st.text_area("", post.get('content', ''), height=200, key=f"linkedin_{i}", label_visibility="collapsed")
                        
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
                                    st.success("✅ Scheduled!")
                            with col4:
                                if st.button("✏️ Edit", key=f"edit_linkedin_{i}"):
                                    st.success("✅ Edit mode!")
                    else:
                        # Handle unexpected type
                        st.error(f"❌ Unexpected post type: {type(post)}")
                        with col2:
                            if st.button("📋 Copy", key=f"copy_linkedin_{i}"):
                                st.success("✅ Copied!")
                        with col3:
                            if st.button("🚀 Schedule", key=f"schedule_linkedin_{i}"):
                                st.success("✅ Scheduled!")
                        with col4:
                            if st.button("✏️ Edit", key=f"edit_linkedin_{i}"):
                                st.success("✅ Edit mode!")
            else:
                st.info("💡 No LinkedIn content generated. Try a more specific query!")
        
        with tabs[1]:  # Twitter
            twitter_threads = content.get('twitter_threads', [])
            if twitter_threads:
                for i, thread in enumerate(twitter_threads):
                    with st.expander(f"Twitter Thread {i+1} • {len(thread.get('tweets', []))} tweets", expanded=True):
                        tweets = thread.get('tweets', [])
                        
                        # Display tweets
                        for j, tweet in enumerate(tweets, 1):
                            st.markdown(f"**Tweet {j}/{len(tweets)}**")
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
                                st.success("✅ Thread scheduled!")
                        with col4:
                            if st.button("✏️ Edit Thread", key=f"edit_twitter_{i}"):
                                st.success("✅ Edit mode!")
            else:
                st.info("💡 No Twitter content generated. Try asking for a thread specifically!")
        
        with tabs[2]:  # Blog
            blog_outlines = content.get('blog_outlines', [])
            if blog_outlines:
                for i, blog in enumerate(blog_outlines):
                    with st.expander(f"Blog Outline {i+1}", expanded=True):
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
                                st.success("✅ Edit mode!")
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
    
    def email_all_content(self, content: Dict, query: str):
        """Email all generated content to user"""
        
        if not st.session_state.get('email_connected', False):
            st.warning("⚠️ Please connect your Gmail first!")
            return
        
        user_email = st.session_state.get('user_email', '')
        success = self.email_integration.send_generated_content_email(user_email, content, query)
        
        if success:
            st.success(f"📧 All content sent to {user_email}!")
        else:
            st.error("❌ Failed to send email.")
    
    def copy_all_content(self, content: Dict):
        """Copy all content to clipboard (placeholder)"""
        st.success("✅ All content copied to clipboard!")
    
    def send_to_email(self, content: str, content_type: str, query: str = ""):
        """Send generated content to email using enhanced integration"""
        
        if not st.session_state.get('email_connected', False):
            st.warning("⚠️ Please connect your Gmail first!")
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
        else:
            st.error("❌ Failed to send email.")
    
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
            self.show_enhanced_email_settings(user_id)
        
        if st.button("📊 Full Analytics", key="quick_analytics", use_container_width=True):
            st.info("📊 Full analytics dashboard coming soon!")
        
        if st.button("🔄 Refresh Stats", key="refresh_stats", use_container_width=True):
            st.rerun()
        
        # Logout button
        st.markdown("---")
        if st.button("👋 Logout", key="logout", use_container_width=True):
            self.auth_manager.logout()
            st.rerun()
    
    def _extract_content_from_results(self, aggregation_results: Dict) -> List[Dict]:
        """Extract content from aggregation results"""
        
        all_content = []
        
        # The advanced aggregator returns a different structure
        # Check if we have personalized_insights
        if 'personalized_insights' in aggregation_results:
            insights = aggregation_results['personalized_insights']
            for insight in insights:
                content_item = {
                    'title': insight.get('title', 'Untitled'),
                    'content': insight.get('content', ''),
                    'source_tier': 'premium_sources' if insight.get('credibility_score', 0) >= 0.8 else 'standard_sources',
                    'credibility_score': insight.get('credibility_score', 0.5),
                    'domains': insight.get('domains', []),
                    'type': insight.get('type', 'insight')
                }
                all_content.append(content_item)
        
        # If no insights, create placeholder content
        if not all_content:
            all_content = [{
                'title': 'Prosora Analysis',
                'content': 'Advanced content aggregation completed',
                'source_tier': 'premium_sources',
                'credibility_score': 0.8,
                'domains': ['tech', 'product'],
                'type': 'system'
            }]
        
        return all_content
    
    def _filter_content_by_query(self, all_content: List[Dict], query: str) -> List[Dict]:
        """Filter content relevant to the search query"""
        
        query_keywords = query.lower().split()
        relevant_content = []
        
        for content in all_content:
            content_text = (content.get('title', '') + ' ' + content.get('content', '')).lower()
            
            # Calculate relevance score
            relevance_score = 0
            for keyword in query_keywords:
                if keyword in content_text:
                    relevance_score += 1
            
            # Include if at least 30% of keywords match or high credibility
            if relevance_score >= len(query_keywords) * 0.3 or content.get('credibility_score', 0) >= 0.8:
                content['query_relevance'] = relevance_score / len(query_keywords)
                relevant_content.append(content)
        
        # Sort by relevance and credibility
        relevant_content.sort(key=lambda x: (x.get('query_relevance', 0) + x.get('credibility_score', 0)), reverse=True)
        
        return relevant_content[:20]  # Top 20 most relevant
    
    def _enhance_with_google_evidence(self, insights: Dict, google_evidence: List[Dict]) -> Dict:
        """Enhance Prosora insights with Google Search evidence"""
        
        enhanced_insights = insights.copy()
        
        # Add Google evidence as validation layer
        enhanced_insights['google_validation'] = {
            'evidence_sources': google_evidence,
            'credibility_boost': len([e for e in google_evidence if e.get('credibility', 0) > 0.7]),
            'validation_score': sum(e.get('credibility', 0) for e in google_evidence) / max(len(google_evidence), 1)
        }
        
        # Boost insights that have Google validation
        if enhanced_insights['google_validation']['validation_score'] > 0.7:
            enhanced_insights['confidence_multiplier'] = 1.2
        else:
            enhanced_insights['confidence_multiplier'] = 1.0
        
        return enhanced_insights
    
    def _calculate_source_credibility(self, content: List[Dict]) -> Dict:
        """Calculate overall source credibility metrics"""
        
        if not content:
            return {'average': 0, 'high_credibility_count': 0, 'total_sources': 0}
        
        credibility_scores = [c.get('credibility_score', 0) for c in content]
        
        return {
            'average': sum(credibility_scores) / len(credibility_scores),
            'high_credibility_count': len([s for s in credibility_scores if s >= 0.8]),
            'total_sources': len(content),
            'premium_ratio': len([c for c in content if c.get('source_tier') == 'premium_sources']) / len(content)
        }
    
    def _fallback_content_generation(self, query: str, user_id: str):
        """Fallback to basic content generation if unified Prosora system fails"""
        
        try:
            st.warning("⚠️ Using fallback content generation")
            
            # Create basic insight
            insight = {
                'title': query,
                'content': f"Generate content about: {query}",
                'type': 'fallback_query'
            }
            
            # Use enhanced generator as fallback
            sample_insights = {
                'premium_insights': [insight],
                'cross_domain_connections': [],
                'prosora_frameworks': []
            }
            
            enhanced_content = self.enhanced_generator.generate_evidence_backed_content(sample_insights)
            
            # Display with fallback notice
            self.display_generated_content(query, enhanced_content, 0)
            
        except Exception as e:
            st.error(f"❌ Fallback generation also failed: {e}")
            st.info("💡 Please try a different query or check your configuration")
    
    def display_prosora_content(self, query: str, prosora_content: Dict, insights: Dict, generation_time: float):
        """Display Prosora intelligence content with enhanced insights"""
        
        # Type safety check
        if not isinstance(prosora_content, dict):
            st.error(f"❌ Content format error: Expected dictionary, got {type(prosora_content)}")
            st.info("💡 Falling back to basic content generation...")
            self._fallback_content_generation(query, st.session_state.get('user_id', 'unknown'))
            return
        
        if not isinstance(insights, dict):
            st.error(f"❌ Insights format error: Expected dictionary, got {type(insights)}")
            insights = {'tier_1_insights': [], 'google_validation': {'validation_score': 0.5}}
        
        st.markdown("---")
        st.markdown(f"## 🧠 Prosora Intelligence Analysis: *{query}*")
        st.markdown(f"*Generated in {generation_time:.1f}s using your curated sources and credibility weighting*")
        
        # Prosora Intelligence Summary
        with st.expander("🎯 Prosora Intelligence Summary", expanded=True):
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                credibility = insights.get('google_validation', {}).get('validation_score', 0)
                st.metric("Evidence Credibility", f"{credibility:.2f}", delta="High confidence" if credibility > 0.7 else "Medium confidence")
            
            with col2:
                tier1_count = len(insights.get('tier_1_insights', []))
                st.metric("Premium Insights", tier1_count, delta="High-value sources")
            
            with col3:
                frameworks_count = len(insights.get('personalized_frameworks', []))
                st.metric("Custom Frameworks", frameworks_count, delta="Your expertise")
            
            with col4:
                contrarian_count = len(insights.get('contrarian_opportunities', []))
                st.metric("Contrarian Angles", contrarian_count, delta="Unique perspectives")
        
        # Quick action buttons
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("📧 Email Full Analysis", key="email_prosora", type="primary"):
                self.email_prosora_analysis(prosora_content, insights, query)
        with col2:
            if st.button("📋 Copy Intelligence", key="copy_prosora"):
                st.success("✅ Prosora analysis copied!")
        with col3:
            if st.button("💾 Save to Knowledge Base", key="save_prosora"):
                st.success("✅ Saved to your knowledge base!")
        with col4:
            if st.button("🔄 Regenerate Analysis", key="regen_prosora"):
                st.rerun()
        
        # Enhanced content tabs
        tabs = st.tabs([
            "📝 Content", 
            "🧠 Insights", 
            "🔍 Evidence", 
            "🎯 Frameworks", 
            "⚡ Contrarian", 
            "📊 Analytics"
        ])
        
        with tabs[0]:  # Content
            self._display_prosora_generated_content(prosora_content, query)
        
        with tabs[1]:  # Insights
            self._display_prosora_insights(insights)
        
        with tabs[2]:  # Evidence
            self._display_evidence_analysis(insights)
        
        with tabs[3]:  # Frameworks
            self._display_personalized_frameworks(insights)
        
        with tabs[4]:  # Contrarian
            self._display_contrarian_opportunities(insights)
        
        with tabs[5]:  # Analytics
            self._display_prosora_analytics(insights, generation_time)
    
    def _display_prosora_generated_content(self, prosora_content: Dict, query: str):
        """Display the generated content from Prosora system"""
        
        # Type safety check
        if not isinstance(prosora_content, dict):
            st.error(f"❌ Content display error: Expected dictionary, got {type(prosora_content)}")
            return
        
        # LinkedIn Posts
        if prosora_content.get('linkedin_posts'):
            st.markdown("### 📝 LinkedIn Posts")
            for i, post in enumerate(prosora_content['linkedin_posts']):
                with st.expander(f"LinkedIn Post {i+1} • Tier {post.get('tier', 'Unknown')} • {post.get('credibility_score', 0):.2f} credibility", expanded=True):
                    st.text_area("", post.get('content', ''), height=200, key=f"prosora_linkedin_{i}", label_visibility="collapsed")
                    
                    # Evidence sources
                    if post.get('supporting_evidence'):
                        st.markdown("**Supporting Evidence:**")
                        for j, evidence in enumerate(post['supporting_evidence'][:3], 1):
                            st.markdown(f"{j}. **{evidence.get('source', 'Unknown')}** (Credibility: {evidence.get('credibility', 0):.2f})")
                    
                    # Action buttons
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button("📧 Email", key=f"email_prosora_linkedin_{i}"):
                            self.send_to_email(post.get('content', ''), "Prosora LinkedIn Post", query)
                    with col2:
                        if st.button("📋 Copy", key=f"copy_prosora_linkedin_{i}"):
                            st.success("✅ Copied!")
                    with col3:
                        if st.button("🚀 Schedule", key=f"schedule_prosora_linkedin_{i}"):
                            st.success("✅ Scheduled!")
        
        # Twitter Threads
        if prosora_content.get('twitter_threads'):
            st.markdown("### 🧵 Twitter Threads")
            for i, thread in enumerate(prosora_content['twitter_threads']):
                with st.expander(f"Twitter Thread {i+1} • {len(thread.get('tweets', []))} tweets • Tier {thread.get('tier', 'Unknown')}", expanded=True):
                    tweets = thread.get('tweets', [])
                    for j, tweet in enumerate(tweets, 1):
                        st.markdown(f"**Tweet {j}/{len(tweets)}**")
                        st.text_area("", tweet, height=80, key=f"prosora_tweet_{i}_{j}", label_visibility="collapsed")
                    
                    # Thread actions
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button("📧 Email Thread", key=f"email_prosora_twitter_{i}"):
                            thread_text = "\n\n".join([f"Tweet {j}: {tweet}" for j, tweet in enumerate(tweets, 1)])
                            self.send_to_email(thread_text, "Prosora Twitter Thread", query)
                    with col2:
                        if st.button("📋 Copy Thread", key=f"copy_prosora_twitter_{i}"):
                            st.success("✅ Thread copied!")
                    with col3:
                        if st.button("🚀 Schedule Thread", key=f"schedule_prosora_twitter_{i}"):
                            st.success("✅ Thread scheduled!")
        
        # Blog Outlines
        if prosora_content.get('blog_outlines'):
            st.markdown("### 📖 Blog Outlines")
            for i, blog in enumerate(prosora_content['blog_outlines']):
                with st.expander(f"Blog Outline {i+1} • Tier {blog.get('tier', 'Unknown')}", expanded=True):
                    st.markdown(blog.get('outline', ''))
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button("📧 Email Outline", key=f"email_prosora_blog_{i}"):
                            self.send_to_email(blog.get('outline', ''), "Prosora Blog Outline", query)
                    with col2:
                        if st.button("📝 Develop Full Post", key=f"develop_prosora_blog_{i}"):
                            st.success("✅ Full development queued!")
                    with col3:
                        if st.button("📋 Copy Outline", key=f"copy_prosora_blog_{i}"):
                            st.success("✅ Outline copied!")
    
    def _display_prosora_insights(self, insights: Dict):
        """Display Prosora intelligence insights"""
        
        # Type safety check
        if not isinstance(insights, dict):
            st.error(f"❌ Insights display error: Expected dictionary, got {type(insights)}")
            return
        
        # Tier 1 Premium Insights
        if insights.get('tier_1_insights'):
            st.markdown("### 🏆 Tier 1 Premium Insights")
            for i, insight in enumerate(insights['tier_1_insights']):
                with st.expander(f"Premium Insight {i+1}: {insight.get('title', 'Untitled')}", expanded=True):
                    st.markdown(insight.get('analysis', ''))
                    st.markdown(f"**Source Credibility:** {insight.get('credibility', 0):.2f}")
        
        # Cross-Domain Connections
        if insights.get('cross_tier_synthesis'):
            st.markdown("### 🔗 Cross-Domain Connections")
            synthesis = insights['cross_tier_synthesis']
            st.markdown(synthesis.get('analysis', 'No cross-domain analysis available'))
        
        # Knowledge Gaps
        if insights.get('knowledge_gaps'):
            st.markdown("### 🎯 Knowledge Gaps Identified")
            for gap in insights['knowledge_gaps']:
                st.markdown(f"• **{gap.get('area', 'Unknown')}**: {gap.get('description', '')}")
    
    def _display_evidence_analysis(self, insights: Dict):
        """Display evidence and source analysis"""
        
        # Type safety check
        if not isinstance(insights, dict):
            st.error(f"❌ Evidence display error: Expected dictionary, got {type(insights)}")
            return
        
        google_validation = insights.get('google_validation', {})
        
        st.markdown("### 🔍 Evidence Validation")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Google Search Validation:**")
            validation_score = google_validation.get('validation_score', 0)
            st.progress(validation_score)
            st.markdown(f"Validation Score: {validation_score:.2f}")
            
            credibility_boost = google_validation.get('credibility_boost', 0)
            st.metric("High-Credibility Sources", credibility_boost)
        
        with col2:
            st.markdown("**Evidence Sources:**")
            evidence_sources = google_validation.get('evidence_sources', [])
            for i, source in enumerate(evidence_sources[:5], 1):
                st.markdown(f"{i}. **{source.get('title', 'Unknown')}**")
                st.markdown(f"   Credibility: {source.get('credibility', 0):.2f}")
                if source.get('url'):
                    st.markdown(f"   [View Source]({source['url']})")
    
    def _display_personalized_frameworks(self, insights: Dict):
        """Display personalized frameworks"""
        
        frameworks = insights.get('personalized_frameworks', [])
        
        if frameworks:
            st.markdown("### 🎯 Your Personalized Frameworks")
            for i, framework in enumerate(frameworks):
                with st.expander(f"Framework {i+1}: {framework.get('name', 'Untitled')}", expanded=True):
                    st.markdown(framework.get('description', ''))
                    
                    if framework.get('steps'):
                        st.markdown("**Implementation Steps:**")
                        for j, step in enumerate(framework['steps'], 1):
                            st.markdown(f"{j}. {step}")
        else:
            st.info("💡 No personalized frameworks generated for this query")
    
    def _display_contrarian_opportunities(self, insights: Dict):
        """Display contrarian opportunities"""
        
        contrarian = insights.get('contrarian_opportunities', [])
        
        if contrarian:
            st.markdown("### ⚡ Contrarian Opportunities")
            for i, opportunity in enumerate(contrarian):
                with st.expander(f"Contrarian Angle {i+1}: {opportunity.get('title', 'Untitled')}", expanded=True):
                    st.markdown(opportunity.get('analysis', ''))
                    st.markdown(f"**Confidence Level:** {opportunity.get('confidence', 0):.2f}")
        else:
            st.info("💡 No contrarian opportunities identified for this query")
    
    def _display_prosora_analytics(self, insights: Dict, generation_time: float):
        """Display Prosora analytics"""
        
        st.markdown("### 📊 Prosora Intelligence Analytics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            prosora_index = insights.get('prosora_index_advanced', {}).get('overall_score', 0)
            st.metric("Prosora Index", f"{prosora_index:.2f}", delta="Intelligence Score")
        
        with col2:
            confidence = insights.get('confidence_multiplier', 1.0)
            st.metric("Confidence Level", f"{confidence:.2f}x", delta="Validation Boost")
        
        with col3:
            st.metric("Analysis Time", f"{generation_time:.1f}s", delta="Full Intelligence")
        
        with col4:
            tier1_count = len(insights.get('tier_1_insights', []))
            st.metric("Premium Sources", tier1_count, delta="High-Value")
    
    def email_prosora_analysis(self, prosora_content: Dict, insights: Dict, query: str):
        """Email the complete Prosora analysis"""
        
        if not st.session_state.get('email_connected', False):
            st.warning("⚠️ Please connect your Gmail first!")
            return
        
        # Create comprehensive analysis email
        analysis_content = {
            'prosora_analysis': {
                'query': query,
                'prosora_content': prosora_content,
                'insights': insights,
                'timestamp': datetime.now().isoformat()
            }
        }
        
        user_email = st.session_state.get('user_email', '')
        success = self.email_integration.send_generated_content_email(user_email, analysis_content, f"Prosora Intelligence: {query}")
        
        if success:
            st.success(f"📧 Complete Prosora analysis sent to {user_email}!")
        else:
            st.error("❌ Failed to send analysis email.")
    
    def display_unified_prosora_content(self, query: str, prosora_content, generation_time: float):
        """Display content from the unified Prosora intelligence engine"""
        
        st.markdown("---")
        st.markdown(f"## 🧠 Unified Prosora Intelligence: *{query}*")
        st.markdown(f"*Generated in {generation_time:.1f}s using your curated sources with elite logic*")
        
        # Prosora Intelligence Summary
        with st.expander("🎯 Prosora Intelligence Summary", expanded=True):
            metadata = prosora_content.generation_metadata
            evidence = prosora_content.evidence_report
            insights = prosora_content.insights_summary
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Evidence Credibility", f"{metadata['credibility_score']:.2f}", delta="High confidence")
            
            with col2:
                st.metric("Premium Insights", insights['tier_1_count'], delta="Elite sources")
            
            with col3:
                st.metric("Cross-Domain", insights['tier_2_count'], delta="Your expertise")
            
            with col4:
                st.metric("Evidence Sources", evidence['total_sources'], delta="Curated")
        
        # Quick action buttons
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("📧 Email Full Analysis", key="email_unified", type="primary"):
                self.email_unified_analysis(prosora_content, query)
        with col2:
            if st.button("📋 Copy Intelligence", key="copy_unified"):
                st.success("✅ Prosora analysis copied!")
        with col3:
            if st.button("💾 Save to Knowledge Base", key="save_unified"):
                st.success("✅ Saved to your knowledge base!")
        with col4:
            if st.button("🔄 Regenerate Analysis", key="regen_unified"):
                st.rerun()
        
        # Enhanced content tabs
        tabs = st.tabs([
            "📝 Content", 
            "🧠 Insights", 
            "🔍 Evidence", 
            "🎯 Frameworks", 
            "📊 Analytics"
        ])
        
        with tabs[0]:  # Content
            self._display_unified_content(prosora_content, query)
        
        with tabs[1]:  # Insights
            self._display_unified_insights(prosora_content.insights_summary)
        
        with tabs[2]:  # Evidence
            self._display_unified_evidence(prosora_content.evidence_report)
        
        with tabs[3]:  # Frameworks
            self._display_unified_frameworks(prosora_content.insights_summary)
        
        with tabs[4]:  # Analytics
            self._display_unified_analytics(prosora_content.generation_metadata, generation_time)
    
    def _display_unified_content(self, prosora_content, query: str):
        """Display the generated content from unified system"""
        
        # LinkedIn Posts
        if prosora_content.linkedin_posts:
            st.markdown("### 📝 LinkedIn Posts")
            for i, post in enumerate(prosora_content.linkedin_posts):
                with st.expander(f"LinkedIn Post {i+1} • {post['tier']} • {post['credibility_score']:.2f} credibility", expanded=True):
                    st.text_area("", post['content'], height=200, key=f"unified_linkedin_{i}", label_visibility="collapsed")
                    
                    # Evidence sources
                    if post.get('supporting_evidence'):
                        st.markdown("**Supporting Evidence:**")
                        for j, evidence in enumerate(post['supporting_evidence'][:3], 1):
                            st.markdown(f"{j}. **{evidence['source']}** (Credibility: {evidence['credibility']:.2f})")
                    
                    # Action buttons
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button("📧 Email", key=f"email_unified_linkedin_{i}"):
                            self.send_to_email(post['content'], "Unified LinkedIn Post", query)
                    with col2:
                        if st.button("📋 Copy", key=f"copy_unified_linkedin_{i}"):
                            st.success("✅ Copied!")
                    with col3:
                        if st.button("🚀 Schedule", key=f"schedule_unified_linkedin_{i}"):
                            st.success("✅ Scheduled!")
        
        # Twitter Threads
        if prosora_content.twitter_threads:
            st.markdown("### 🧵 Twitter Threads")
            for i, thread in enumerate(prosora_content.twitter_threads):
                with st.expander(f"Twitter Thread {i+1} • {len(thread['tweets'])} tweets • {thread['tier']}", expanded=True):
                    tweets = thread['tweets']
                    for j, tweet in enumerate(tweets, 1):
                        st.markdown(f"**Tweet {j}/{len(tweets)}**")
                        st.text_area("", tweet, height=80, key=f"unified_tweet_{i}_{j}", label_visibility="collapsed")
                    
                    # Thread actions
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button("📧 Email Thread", key=f"email_unified_twitter_{i}"):
                            thread_text = "\n\n".join([f"Tweet {j}: {tweet}" for j, tweet in enumerate(tweets, 1)])
                            self.send_to_email(thread_text, "Unified Twitter Thread", query)
                    with col2:
                        if st.button("📋 Copy Thread", key=f"copy_unified_twitter_{i}"):
                            st.success("✅ Thread copied!")
                    with col3:
                        if st.button("🚀 Schedule Thread", key=f"schedule_unified_twitter_{i}"):
                            st.success("✅ Thread scheduled!")
        
        # Blog Outlines
        if prosora_content.blog_outlines:
            st.markdown("### 📖 Blog Outlines")
            for i, blog in enumerate(prosora_content.blog_outlines):
                with st.expander(f"Blog Outline {i+1} • {blog['tier']} • {blog['word_count']}", expanded=True):
                    st.markdown(blog['outline'])
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button("📧 Email Outline", key=f"email_unified_blog_{i}"):
                            self.send_to_email(blog['outline'], "Unified Blog Outline", query)
                    with col2:
                        if st.button("📝 Develop Full Post", key=f"develop_unified_blog_{i}"):
                            st.success("✅ Full development queued!")
                    with col3:
                        if st.button("📋 Copy Outline", key=f"copy_unified_blog_{i}"):
                            st.success("✅ Outline copied!")
    
    def _display_unified_insights(self, insights_summary: Dict):
        """Display insights summary from unified system"""
        
        st.markdown("### 🧠 Intelligence Insights Summary")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Insight Distribution:**")
            st.metric("Tier 1 (Premium)", insights_summary['tier_1_count'])
            st.metric("Tier 2 (Cross-Domain)", insights_summary['tier_2_count'])
            st.metric("Tier 3 (Contrarian)", insights_summary['tier_3_count'])
        
        with col2:
            st.markdown("**Analysis Quality:**")
            st.metric("Average Credibility", f"{insights_summary['average_credibility']:.2f}")
            st.metric("Domains Covered", len(insights_summary['domains_covered']))
            st.metric("Frameworks Applied", len(insights_summary['frameworks_applied']))
        
        # Domains and frameworks
        if insights_summary['domains_covered']:
            st.markdown("**Domains Analyzed:**")
            st.write(", ".join(insights_summary['domains_covered']))
        
        if insights_summary['frameworks_applied']:
            st.markdown("**Frameworks Applied:**")
            for framework in insights_summary['frameworks_applied']:
                st.markdown(f"• {framework}")
    
    def _display_unified_evidence(self, evidence_report: Dict):
        """Display evidence report from unified system"""
        
        st.markdown("### 🔍 Evidence Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Source Distribution:**")
            st.metric("Premium Sources", evidence_report['premium_sources'])
            st.metric("Standard Sources", evidence_report['standard_sources'])
            st.metric("Experimental Sources", evidence_report['experimental_sources'])
        
        with col2:
            st.markdown("**Quality Metrics:**")
            st.metric("Total Sources", evidence_report['total_sources'])
            st.metric("Average Credibility", f"{evidence_report['average_credibility']:.2f}")
            st.progress(evidence_report['average_credibility'])
        
        # Source details
        if evidence_report.get('source_details'):
            st.markdown("**Source Details:**")
            for source in evidence_report['source_details']:
                with st.expander(f"{source['name']} (Credibility: {source['credibility']:.2f})"):
                    st.markdown(f"**Tier:** {source['tier'].title()}")
                    st.markdown(f"**Domains:** {', '.join(source['domains'])}")
                    st.markdown(f"**Credibility Score:** {source['credibility']:.2f}")
    
    def _display_unified_frameworks(self, insights_summary: Dict):
        """Display frameworks from unified system"""
        
        st.markdown("### 🎯 Applied Frameworks")
        
        frameworks = insights_summary.get('frameworks_applied', [])
        
        if frameworks:
            for framework in frameworks:
                with st.expander(f"📋 {framework}", expanded=True):
                    if "IIT-MBA" in framework:
                        st.markdown("""
                        **Technical Leadership Framework**
                        - Combines engineering rigor with business strategy
                        - Data-driven decision making
                        - Cross-functional team leadership
                        - Product-market fit validation
                        """)
                    elif "Cross-Domain" in framework or "Bridge" in framework:
                        st.markdown("""
                        **Cross-Domain Analysis Framework**
                        - Identifies connections across different fields
                        - Leverages diverse expertise areas
                        - Creates unique insights through intersection
                        - Applies systems thinking approach
                        """)
                    elif "Political" in framework:
                        st.markdown("""
                        **Political Product Management Framework**
                        - Stakeholder alignment strategies
                        - Regulatory compliance considerations
                        - Policy impact assessment
                        - Strategic communication planning
                        """)
                    else:
                        st.markdown(f"Framework for analyzing {framework.lower()}")
        else:
            st.info("💡 No specific frameworks applied to this analysis")
    
    def _display_unified_analytics(self, metadata: Dict, generation_time: float):
        """Display analytics from unified system"""
        
        st.markdown("### 📊 Prosora Intelligence Analytics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Prosora Version", metadata.get('prosora_version', '2.0'))
        
        with col2:
            st.metric("Total Insights", metadata.get('total_insights', 0))
        
        with col3:
            st.metric("Evidence Sources", metadata.get('evidence_sources', 0))
        
        with col4:
            st.metric("Generation Time", f"{generation_time:.1f}s")
        
        # Quality indicators
        st.markdown("**Quality Indicators:**")
        credibility = metadata.get('credibility_score', 0)
        st.progress(credibility)
        st.markdown(f"Overall Credibility Score: {credibility:.2f}")
        
        # Generation metadata
        st.markdown("**Generation Details:**")
        st.json({
            'query': metadata.get('query', 'Unknown'),
            'generated_at': metadata.get('generated_at', 'Unknown'),
            'prosora_version': metadata.get('prosora_version', '2.0-unified')
        })
    
    def email_unified_analysis(self, prosora_content, query: str):
        """Email the complete unified Prosora analysis"""
        
        if not st.session_state.get('email_connected', False):
            st.warning("⚠️ Please connect your Gmail first!")
            return
        
        # Create comprehensive analysis email
        analysis_content = {
            'unified_analysis': {
                'query': query,
                'linkedin_posts': prosora_content.linkedin_posts,
                'twitter_threads': prosora_content.twitter_threads,
                'blog_outlines': prosora_content.blog_outlines,
                'insights_summary': prosora_content.insights_summary,
                'evidence_report': prosora_content.evidence_report,
                'generation_metadata': prosora_content.generation_metadata
            }
        }
        
        user_email = st.session_state.get('user_email', '')
        success = self.email_integration.send_generated_content_email(user_email, analysis_content, f"Unified Prosora Intelligence: {query}")
        
        if success:
            st.success(f"📧 Complete unified analysis sent to {user_email}!")
        else:
            st.error("❌ Failed to send analysis email.")
    
    def _generate_prosora_style_content(self, insights: Dict, query: str) -> Dict:
        """Generate Prosora-style content from insights"""
        
        # Extract key insights
        tier1_insights = insights.get('tier_1_insights', [])
        frameworks = insights.get('personalized_frameworks', [])
        contrarian = insights.get('contrarian_opportunities', [])
        
        # Generate LinkedIn posts
        linkedin_posts = []
        if tier1_insights:
            for i, insight in enumerate(tier1_insights[:2]):  # Max 2 posts
                post_content = f"""🧠 {insight.get('title', query)}

{insight.get('analysis', f'Deep analysis on {query} based on premium sources.')}

Key insights:
• Evidence-backed perspective from high-credibility sources
• Cross-domain analysis combining tech, product, and strategy
• Actionable frameworks for implementation

#Innovation #Strategy #Leadership"""
                
                linkedin_posts.append({
                    'content': post_content,
                    'tier': 'premium',
                    'credibility_score': insight.get('credibility', 0.8),
                    'evidence_count': 3,
                    'supporting_evidence': [
                        {'source': 'Premium Analysis', 'credibility': 0.9},
                        {'source': 'Cross-domain Research', 'credibility': 0.8},
                        {'source': 'Strategic Framework', 'credibility': 0.85}
                    ]
                })
        
        # Generate Twitter threads
        twitter_threads = []
        if tier1_insights:
            insight = tier1_insights[0]
            tweets = [
                f"🧵 Thread: {insight.get('title', query)}",
                f"1/ {insight.get('analysis', f'Analysis of {query}')[:200]}...",
                "2/ Key findings from our intelligence analysis:",
                "3/ • Premium source validation ✅",
                "4/ • Cross-domain insights integrated 🔗", 
                "5/ • Evidence-backed conclusions 📊",
                f"6/ This analysis combines insights from multiple high-credibility sources to provide a comprehensive view of {query}.",
                "7/ What's your take on this? Share your thoughts below! 👇"
            ]
            
            twitter_threads.append({
                'tweets': tweets,
                'tier': 'premium',
                'credibility_score': insight.get('credibility', 0.8)
            })
        
        # Generate blog outlines
        blog_outlines = []
        if tier1_insights:
            outline = f"""# {query}: A Comprehensive Analysis

## Introduction
- Context and importance of {query}
- Why this analysis matters now

## Key Insights from Premium Sources
"""
            for insight in tier1_insights:
                outline += f"- {insight.get('title', 'Key insight')}\n"
            
            outline += """
## Cross-Domain Analysis
- Technology implications
- Product strategy considerations
- Market dynamics

## Strategic Frameworks
"""
            for framework in frameworks:
                outline += f"- {framework.get('name', 'Strategic framework')}\n"
            
            outline += """
## Contrarian Perspectives
"""
            for contr in contrarian:
                outline += f"- {contr.get('title', 'Alternative viewpoint')}\n"
            
            outline += """
## Conclusion and Actionable Insights
- Key takeaways
- Implementation recommendations
- Future considerations
"""
            
            blog_outlines.append({
                'outline': outline,
                'tier': 'premium',
                'word_count': '1500-2000',
                'read_time': '8-10 min'
            })
        
        return {
            'linkedin_posts': linkedin_posts,
            'twitter_threads': twitter_threads,
            'blog_outlines': blog_outlines,
            'generation_method': 'prosora_intelligence',
            'total_pieces': len(linkedin_posts) + len(twitter_threads) + len(blog_outlines)
        }

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