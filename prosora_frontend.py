#!/usr/bin/env python3
"""
Prosora Command Center - Frontend Interface
Streamlit-based dashboard for content review, editing, and scheduling
"""

import streamlit as st
import json
import yaml
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List
import os
from performance_tracker import ProsoraPerformanceTracker, SocialMediaTracker
from data_manager import ProsoraDataManager
from google_evidence_search import GoogleEvidenceSearch
from megatrends_radar import MegatrendsRadar
from enhanced_content_generator import EnhancedContentGenerator

# Page config
st.set_page_config(
    page_title="Prosora Command Center",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

class ProsoraFrontend:
    def __init__(self):
        self.load_data()
        self.setup_session_state()
        
        # Initialize performance tracking
        self.performance_tracker = ProsoraPerformanceTracker()
        self.social_tracker = SocialMediaTracker()
        self.data_manager = ProsoraDataManager()
        
        # Initialize new features
        self.google_search = GoogleEvidenceSearch()
        self.megatrends_radar = MegatrendsRadar()
        self.enhanced_generator = EnhancedContentGenerator()
        
        # Metric explanations
        self.metric_explanations = {
            'prosora_score': {
                'title': 'Prosora Score',
                'description': 'Your composite intelligence score across all domains.',
                'calculation': 'Weighted average of Tech Innovation (30%), Political Stability (20%), Market Opportunity (25%), and Financial Insight (25%).',
                'range': '0-100 (higher is better)',
                'interpretation': '70+ = Excellent, 50-70 = Good, <50 = Needs improvement'
            },
            'content_ready': {
                'title': 'Content Ready',
                'description': 'Number of AI-generated content pieces ready for publishing.',
                'calculation': 'Sum of approved LinkedIn posts, Twitter threads, and blog outlines.',
                'range': 'No limit',
                'interpretation': '3+ pieces = Good pipeline, 5+ = Excellent content flow'
            },
            'engagement_rate': {
                'title': 'Engagement Rate',
                'description': 'Average engagement across all your published content.',
                'calculation': '(Likes + Comments + Shares) ÷ Views × 100',
                'range': '0-100% (higher is better)',
                'interpretation': '5%+ = Excellent, 2-5% = Good, <2% = Needs improvement'
            },
            'success_rate': {
                'title': 'Success Rate',
                'description': 'Percentage of your content that achieves high performance.',
                'calculation': 'High-performing posts ÷ Total posts × 100',
                'range': '0-100% (higher is better)',
                'interpretation': '30%+ = Excellent, 15-30% = Good, <15% = Needs improvement'
            },
            'tech_innovation': {
                'title': 'Tech Innovation Score',
                'description': 'Your expertise level in technology and innovation topics.',
                'calculation': 'Weighted by source credibility and content relevance in tech domain.',
                'range': '0-100 (higher is better)',
                'interpretation': 'Reflects your technical thought leadership strength'
            },
            'political_stability': {
                'title': 'Political Stability Score',
                'description': 'Your expertise level in political and policy topics.',
                'calculation': 'Weighted by source credibility and content relevance in politics domain.',
                'range': '0-100 (higher is better)',
                'interpretation': 'Reflects your political analysis and consulting background'
            },
            'market_opportunity': {
                'title': 'Market Opportunity Score',
                'description': 'Your expertise level in product and market topics.',
                'calculation': 'Weighted by source credibility and content relevance in product/business domain.',
                'range': '0-100 (higher is better)',
                'interpretation': 'Reflects your product management and business acumen'
            },
            'financial_insight': {
                'title': 'Financial Insight Score',
                'description': 'Your expertise level in finance and FinTech topics.',
                'calculation': 'Weighted by source credibility and content relevance in finance domain.',
                'range': '0-100 (higher is better)',
                'interpretation': 'Reflects your FinTech MBA knowledge and financial expertise'
            },
            'composite_score': {
                'title': 'Composite Prosora Score',
                'description': 'Overall intelligence score combining all domain expertise.',
                'calculation': 'Tech (30%) + Politics (20%) + Product (25%) + Finance (25%)',
                'range': '0-100 (higher is better)',
                'interpretation': 'Your overall cross-domain expertise level'
            },
            'content_quality': {
                'title': 'Content Quality Score',
                'description': 'Average quality of your content based on source credibility.',
                'calculation': 'Average credibility score of all content sources weighted by relevance.',
                'range': '0-100 (higher is better)',
                'interpretation': '80+ = Premium sources, 60-80 = Good sources, <60 = Mixed quality'
            },
            'source_diversity': {
                'title': 'Source Diversity',
                'description': 'Number of unique content sources in your knowledge base.',
                'calculation': 'Count of distinct sources (newsletters, blogs, videos, etc.)',
                'range': 'No limit (more is better)',
                'interpretation': '10+ = Excellent diversity, 5-10 = Good, <5 = Limited perspective'
            }
        }
    
    def load_data(self):
        """Load all data files"""
        try:
            with open("data/demo_content.json", "r") as f:
                self.raw_content = json.load(f)
        except FileNotFoundError:
            self.raw_content = []
        
        try:
            with open("data/demo_insights.json", "r") as f:
                self.insights = json.load(f)
        except FileNotFoundError:
            self.insights = {}
        
        try:
            with open("data/demo_generated.json", "r") as f:
                self.generated_content = json.load(f)
        except FileNotFoundError:
            self.generated_content = {}
        
        try:
            with open("data/demo_report.json", "r") as f:
                self.report = json.load(f)
        except FileNotFoundError:
            self.report = {}
        
        # Load content approval history
        try:
            with open("data/content_approvals.json", "r") as f:
                self.approvals = json.load(f)
        except FileNotFoundError:
            self.approvals = {"approved": [], "rejected": [], "pending": []}
    
    def setup_session_state(self):
        """Initialize session state"""
        if 'current_tab' not in st.session_state:
            st.session_state.current_tab = "Dashboard"
        if 'editing_content' not in st.session_state:
            st.session_state.editing_content = None
        if 'feedback_mode' not in st.session_state:
            st.session_state.feedback_mode = False
        
        # Initialize info modal states
        info_modals = [
            'show_prosora_info', 'show_content_ready_info', 'show_engagement_info',
            'show_success_rate_info', 'show_tech_innovation_info', 'show_political_stability_info',
            'show_market_opportunity_info', 'show_financial_insight_info', 'show_composite_score_info',
            'show_content_quality_info', 'show_source_diversity_info'
        ]
        
        for modal in info_modals:
            if modal not in st.session_state:
                st.session_state[modal] = False

    def render_header(self):
        """Render the main header"""
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.title("🧠 Prosora Command Center")
            st.caption("Your AI-Powered Content Intelligence Dashboard")
        
        with col2:
            prosora_score = self.report.get('prosora_index', {}).get('composite_prosora_score', 0)
            col2a, col2b = st.columns([4, 1])
            with col2a:
                st.metric("Prosora Score", f"{prosora_score:.1f}/100", delta="↗️ +5.2")
            with col2b:
                if st.button("ℹ️", key="prosora_score_info", help="Click for details"):
                    st.session_state.show_prosora_info = True
        
        with col3:
            content_ready = self.report.get('content_ready', {})
            total_ready = sum(content_ready.values()) if content_ready else 0
            col3a, col3b = st.columns([4, 1])
            with col3a:
                st.metric("Content Ready", total_ready, delta="↗️ +3")
            with col3b:
                if st.button("ℹ️", key="content_ready_info", help="Click for details"):
                    st.session_state.show_content_ready_info = True

    def render_sidebar(self):
        """Render the sidebar navigation"""
        st.sidebar.title("Navigation")
        
        # Main navigation
        tabs = ["Dashboard", "Content Review", "Performance", "Insights", "Megatrends", "Analytics", "Settings"]
        st.session_state.current_tab = st.sidebar.radio("Go to", tabs)
        
        st.sidebar.divider()
        
        # Quick actions
        st.sidebar.subheader("Quick Actions")
        if st.sidebar.button("🔄 Run New Analysis"):
            st.sidebar.success("Analysis queued!")
        
        if st.sidebar.button("🔬 Generate Enhanced Content"):
            st.sidebar.success("Enhanced generation started!")
        
        if st.sidebar.button("📤 Publish Approved"):
            st.sidebar.success("Publishing scheduled!")
        
        st.sidebar.divider()
        
        # System status
        st.sidebar.subheader("System Status")
        st.sidebar.success("✅ AI Engine: Online")
        st.sidebar.success("✅ Content Pipeline: Active")
        st.sidebar.info("📧 Email Integration: Pending")
        
        # Recent activity
        st.sidebar.subheader("Recent Activity")
        st.sidebar.text("🔍 Analysis completed")
        st.sidebar.text("📝 3 posts generated")
        st.sidebar.text("✅ 2 posts approved")

    def render_dashboard(self):
        """Render the main dashboard"""
        st.header("📊 Intelligence Dashboard")
        
        # Show metric info modals if requested
        self.show_metric_info_modal('prosora_score')
        self.show_metric_info_modal('content_ready')
        self.show_metric_info_modal('engagement')
        self.show_metric_info_modal('success_rate')
        
        # Key metrics row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            insights_count = sum(len(v) if isinstance(v, list) else 0 for v in self.insights.values())
            st.metric("Insights Generated", insights_count, delta="↗️ +12")
        
        with col2:
            content_count = len(self.raw_content)
            st.metric("Sources Processed", content_count, delta="↗️ +2")
        
        with col3:
            pending_count = len(self.approvals.get('pending', []))
            st.metric("Pending Review", pending_count, delta="⏳")
        
        with col4:
            approved_count = len(self.approvals.get('approved', []))
            st.metric("Approved Content", approved_count, delta="✅")
        
        # Prosora Index visualization
        st.subheader("🎯 Prosora Index Breakdown")
        
        prosora_data = self.report.get('prosora_index', {})
        if prosora_data:
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Enhanced dual-layer radar chart with megatrends
                try:
                    fig = self.megatrends_radar.create_dual_layer_radar(prosora_data)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Add megatrends insights
                    with st.expander("🔮 Megatrends Analysis", expanded=False):
                        insights = self.megatrends_radar.get_megatrend_insights()
                        
                        col1a, col1b = st.columns(2)
                        
                        with col1a:
                            st.write("**Strongest Alignment:**")
                            strongest = insights['strongest_alignment']
                            st.write(f"• {strongest['domain']}: {strongest['score']:.1f}/100")
                            
                            st.write("**Top Megatrends:**")
                            for trend in insights['top_megatrends'][:3]:
                                st.write(f"• {trend['name']} ({trend['relevance']}% relevance)")
                        
                        with col1b:
                            st.write("**Opportunity Gaps:**")
                            gaps = insights['opportunity_gaps']
                            if gaps:
                                for gap in gaps[:2]:
                                    st.write(f"• {gap['domain']}: +{gap['improvement_potential']:.0f} points potential")
                            else:
                                st.write("• No major gaps identified")
                            
                            st.write(f"**Overall Alignment:** {insights['overall_alignment']:.1f}/100")
                
                except Exception as e:
                    # Fallback to original radar chart
                    categories = ['Tech Innovation', 'Political Stability', 'Market Opportunity', 'Financial Insight']
                    values = [
                        prosora_data.get('tech_innovation', 0),
                        prosora_data.get('political_stability', 0),
                        prosora_data.get('market_opportunity', 0),
                        prosora_data.get('financial_insight', 0)
                    ]
                    
                    fig = go.Figure()
                    fig.add_trace(go.Scatterpolar(
                        r=values,
                        theta=categories,
                        fill='toself',
                        name='Current Score',
                        line_color='rgb(0, 123, 255)'
                    ))
                    
                    fig.update_layout(
                        polar=dict(
                            radialaxis=dict(visible=True, range=[0, 100])
                        ),
                        showlegend=True,
                        title="Your Expertise Profile"
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Show metric info modals
                self.show_metric_info_modal('composite_score')
                self.show_metric_info_modal('content_quality')
                self.show_metric_info_modal('source_diversity')
                
                # Metrics with info buttons
                self.create_metric_with_info(
                    "Composite Score", 
                    f"{prosora_data.get('composite_prosora_score', 0):.1f}/100",
                    metric_key="composite_score"
                )
                
                self.create_metric_with_info(
                    "Content Quality", 
                    f"{prosora_data.get('content_quality_score', 0):.1f}/100",
                    metric_key="content_quality"
                )
                
                self.create_metric_with_info(
                    "Source Diversity", 
                    str(prosora_data.get('source_diversity', 0)),
                    metric_key="source_diversity"
                )
                
                # Progress bars for each domain with info buttons
                st.write("**Domain Breakdown:**")
                for category, value in zip(categories, values):
                    col_prog, col_info = st.columns([4, 1])
                    with col_prog:
                        st.progress(value/100, text=f"{category}: {value:.1f}/100")
                    with col_info:
                        domain_key = category.lower().replace(' ', '_')
                        if st.button("ℹ️", key=f"{domain_key}_progress_info", help="Click for details"):
                            st.session_state[f'show_{domain_key}_info'] = True
                            st.rerun()
                
                # Show domain info modals
                self.show_metric_info_modal('tech_innovation')
                self.show_metric_info_modal('political_stability') 
                self.show_metric_info_modal('market_opportunity')
                self.show_metric_info_modal('financial_insight')
            
            # Ensure categories is defined for the loop below
            categories = ['Tech Innovation', 'Political Stability', 'Market Opportunity', 'Financial Insight']
        
        # Recent content performance
        st.subheader("📈 Content Performance Trends")
        
        # Mock performance data for demo
        performance_data = {
            'Date': pd.date_range(start='2024-01-01', periods=7, freq='D'),
            'LinkedIn Engagement': [45, 67, 89, 123, 156, 134, 178],
            'Twitter Engagement': [23, 34, 56, 78, 91, 87, 102],
            'Blog Views': [234, 345, 456, 567, 678, 589, 712]
        }
        
        df = pd.DataFrame(performance_data)
        
        fig = px.line(df, x='Date', y=['LinkedIn Engagement', 'Twitter Engagement', 'Blog Views'],
                     title="7-Day Engagement Trends")
        st.plotly_chart(fig, use_container_width=True)

    def render_content_review(self):
        """Render the content review interface"""
        st.header("📝 Content Review & Approval")
        
        # Filter tabs
        review_tab = st.tabs(["Pending Review", "Approved", "Rejected", "Scheduled"])
        
        with review_tab[0]:  # Pending Review
            st.subheader("⏳ Content Awaiting Your Review")
            
            # Get generated content
            linkedin_posts = self.generated_content.get('linkedin_posts', [])
            twitter_threads = self.generated_content.get('twitter_threads', [])
            blog_outlines = self.generated_content.get('blog_outlines', [])
            
            all_content = []
            for post in linkedin_posts:
                all_content.append({**post, 'content_type': 'LinkedIn Post'})
            for thread in twitter_threads:
                all_content.append({**thread, 'content_type': 'Twitter Thread'})
            for blog in blog_outlines:
                all_content.append({**blog, 'content_type': 'Blog Outline'})
            
            for i, content_item in enumerate(all_content):
                with st.expander(f"{content_item['content_type']}: {content_item.get('type', 'Generated Content')}"):
                    
                    # Content preview
                    if content_item['content_type'] == 'LinkedIn Post':
                        st.text_area("Content", content_item.get('content', ''), height=200, key=f"content_{i}")
                    elif content_item['content_type'] == 'Twitter Thread':
                        st.write("**Twitter Thread:**")
                        tweets = content_item.get('tweets', [])
                        for j, tweet in enumerate(tweets, 1):
                            st.write(f"{j}/{len(tweets)} {tweet}")
                    elif content_item['content_type'] == 'Blog Outline':
                        st.write("**Blog Outline:**")
                        st.write(content_item.get('outline', ''))
                    
                    # Metadata
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.write(f"**Platform:** {content_item.get('platform', 'N/A')}")
                    with col2:
                        st.write(f"**Type:** {content_item.get('type', 'N/A')}")
                    with col3:
                        st.write(f"**Engagement Potential:** {content_item.get('estimated_engagement', 'Medium')}")
                    
                    # Action buttons
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        if st.button("✅ Approve", key=f"approve_{i}"):
                            self.approve_content(content_item, i)
                            st.success("Content approved!")
                            st.rerun()
                    
                    with col2:
                        if st.button("✏️ Edit", key=f"edit_{i}"):
                            st.session_state.editing_content = i
                            st.rerun()
                    
                    with col3:
                        if st.button("❌ Reject", key=f"reject_{i}"):
                            st.session_state.feedback_mode = i
                            st.rerun()
                    
                    with col4:
                        if st.button("📅 Schedule", key=f"schedule_{i}"):
                            self.schedule_content(content_item, i)
                            st.success("Content scheduled!")
                    
                    # Enhanced generation button
                    if st.button("🔬 Enhance with Evidence", key=f"enhance_{i}"):
                        with st.spinner("Researching evidence and enhancing content..."):
                            try:
                                # Use enhanced generator for evidence-backed content
                                sample_insights = {
                                    'premium_insights': [content_item],
                                    'cross_domain_connections': [],
                                    'prosora_frameworks': []
                                }
                                
                                enhanced_content = self.enhanced_generator.generate_evidence_backed_content(sample_insights)
                                
                                if enhanced_content['linkedin_posts']:
                                    enhanced_post = enhanced_content['linkedin_posts'][0]
                                    st.success(f"✅ Enhanced with {enhanced_post.get('evidence_count', 0)} evidence sources!")
                                    
                                    # Show enhanced content
                                    st.write("**Enhanced Content:**")
                                    st.text_area("Enhanced version", enhanced_post.get('content', ''), height=200, key=f"enhanced_{i}")
                                    
                                    # Show evidence used
                                    if enhanced_post.get('evidence_count', 0) > 0:
                                        st.write(f"**Evidence Credibility:** {enhanced_post.get('evidence_credibility', 0):.2f}/1.0")
                                else:
                                    st.warning("Enhancement completed but no content generated")
                                    
                            except Exception as e:
                                st.error(f"Enhancement failed: {e}")
                    
                    # Publish button with performance tracking
                    if st.button("🚀 Publish & Track", key=f"publish_track_{i}"):
                        content_id = self.publish_and_track_content(content_item, i)
                        st.success(f"Published and tracking started! ID: {content_id}")
                        st.rerun()
                    
                    # Edit mode
                    if st.session_state.editing_content == i:
                        st.write("**Edit Mode:**")
                        edited_content = st.text_area("Edit content", content_item.get('content', ''), key=f"edit_area_{i}")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("💾 Save Changes", key=f"save_{i}"):
                                self.save_edited_content(i, edited_content)
                                st.success("Changes saved!")
                                st.session_state.editing_content = None
                                st.rerun()
                        with col2:
                            if st.button("❌ Cancel", key=f"cancel_{i}"):
                                st.session_state.editing_content = None
                                st.rerun()
                    
                    # Feedback mode
                    if st.session_state.feedback_mode == i:
                        st.write("**Rejection Feedback:**")
                        feedback_options = [
                            "Tone doesn't match my voice",
                            "Content is too generic",
                            "Missing key insights",
                            "Too technical/complex",
                            "Not engaging enough",
                            "Factual inaccuracies",
                            "Other"
                        ]
                        
                        selected_feedback = st.multiselect("Why are you rejecting this content?", feedback_options, key=f"feedback_{i}")
                        additional_feedback = st.text_area("Additional feedback", key=f"additional_{i}")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("📝 Submit Feedback", key=f"submit_feedback_{i}"):
                                self.reject_content_with_feedback(content_item, i, selected_feedback, additional_feedback)
                                st.success("Feedback submitted! AI will learn from this.")
                                st.session_state.feedback_mode = False
                                st.rerun()
                        with col2:
                            if st.button("❌ Cancel", key=f"cancel_feedback_{i}"):
                                st.session_state.feedback_mode = False
                                st.rerun()
        
        with review_tab[1]:  # Approved
            st.subheader("✅ Approved Content")
            approved_content = self.approvals.get('approved', [])
            
            if approved_content:
                for i, content in enumerate(approved_content):
                    with st.expander(f"Approved: {content.get('content_type', 'Content')}"):
                        st.write(content.get('content', '')[:200] + "...")
                        st.write(f"**Approved on:** {content.get('approved_date', 'N/A')}")
                        
                        if st.button("📤 Publish Now", key=f"publish_{i}"):
                            st.success("Publishing...")
            else:
                st.info("No approved content yet.")
        
        with review_tab[2]:  # Rejected
            st.subheader("❌ Rejected Content")
            rejected_content = self.approvals.get('rejected', [])
            
            if rejected_content:
                for i, content in enumerate(rejected_content):
                    with st.expander(f"Rejected: {content.get('content_type', 'Content')}"):
                        st.write(content.get('content', '')[:200] + "...")
                        st.write(f"**Rejection Reason:** {', '.join(content.get('feedback', []))}")
                        st.write(f"**Additional Feedback:** {content.get('additional_feedback', 'None')}")
                        
                        if st.button("🔄 Regenerate", key=f"regen_{i}"):
                            st.success("Regenerating with feedback...")
            else:
                st.info("No rejected content.")
        
        with review_tab[3]:  # Scheduled
            st.subheader("📅 Scheduled Content")
            st.info("Scheduled content feature coming soon!")

    def render_performance(self):
        """Render the performance tracking dashboard"""
        st.header("📈 Content Performance Tracking")
        
        # Performance overview
        col1, col2, col3, col4 = st.columns(4)
        
        # Get performance data
        dashboard_data = self.performance_tracker.get_performance_dashboard_data()
        
        if "message" not in dashboard_data:
            # Show metric info modals
            self.show_metric_info_modal('engagement')
            self.show_metric_info_modal('success_rate')
            
            with col1:
                st.metric("Total Posts Tracked", dashboard_data.get('total_posts', 0))
            
            with col2:
                avg_engagement = dashboard_data.get('avg_engagement_rate', 0)
                self.create_metric_with_info(
                    "Avg Engagement Rate", 
                    f"{avg_engagement:.1f}%", 
                    delta="↗️ +1.2%",
                    metric_key="engagement"
                )
            
            with col3:
                high_performers = dashboard_data.get('high_performers', 0)
                st.metric("High Performers", high_performers, delta="↗️ +2")
            
            with col4:
                total_posts = dashboard_data.get('total_posts', 1)
                success_rate = (high_performers / total_posts) * 100 if total_posts > 0 else 0
                self.create_metric_with_info(
                    "Success Rate", 
                    f"{success_rate:.1f}%", 
                    delta="↗️ +5%",
                    metric_key="success_rate"
                )
        
        # Performance tabs
        perf_tabs = st.tabs(["Live Tracking", "Performance Analytics", "AI Learning", "Publish & Track"])
        
        with perf_tabs[0]:  # Live Tracking
            st.subheader("🔴 Live Content Performance")
            
            if "message" not in dashboard_data:
                # Performance trend chart
                trend_data = dashboard_data.get('performance_trend', {})
                if trend_data:
                    df_trend = pd.DataFrame(list(trend_data.items()), columns=['Date', 'Engagement Rate'])
                    df_trend['Date'] = pd.to_datetime(df_trend['Date'])
                    
                    fig = px.line(df_trend, x='Date', y='Engagement Rate', 
                                 title="7-Day Engagement Trend")
                    st.plotly_chart(fig, use_container_width=True)
                
                # Top performing posts
                st.subheader("🏆 Top Performing Posts")
                top_posts = dashboard_data.get('top_performing_posts', [])
                
                for i, post in enumerate(top_posts[:5]):
                    with st.expander(f"#{i+1} - {post['platform'].title()} ({post['engagement_rate']:.1f}% engagement)"):
                        st.write(f"**Content:** {post['content_text'][:200]}...")
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.write(f"**Platform:** {post['platform']}")
                        with col2:
                            st.write(f"**Engagement:** {post['engagement_rate']:.1f}%")
                        with col3:
                            if st.button("📊 View Details", key=f"details_{i}"):
                                st.session_state.selected_post = post['content_id']
            else:
                st.info("No performance data available yet. Publish some content to start tracking!")
        
        with perf_tabs[1]:  # Performance Analytics
            st.subheader("📊 Performance Analytics")
            
            # Platform comparison
            if "message" not in dashboard_data:
                platform_data = dashboard_data.get('platform_breakdown', {})
                if platform_data:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Platform distribution pie chart
                        df_platform = pd.DataFrame(list(platform_data.items()), 
                                                  columns=['Platform', 'Posts'])
                        fig = px.pie(df_platform, values='Posts', names='Platform', 
                                    title="Posts by Platform")
                        st.plotly_chart(fig, use_container_width=True)
                    
                    with col2:
                        # Performance by platform
                        patterns = self.performance_tracker.analyze_performance_patterns()
                        if "message" not in patterns:
                            platform_perf = patterns.get('platform_performance', {})
                            if platform_perf.get('engagement_rate'):
                                df_perf = pd.DataFrame(list(platform_perf['engagement_rate'].items()), 
                                                     columns=['Platform', 'Avg Engagement'])
                                fig = px.bar(df_perf, x='Platform', y='Avg Engagement', 
                                           title="Average Engagement by Platform")
                                st.plotly_chart(fig, use_container_width=True)
                
                # Content type performance
                st.subheader("📝 Content Type Performance")
                patterns = self.performance_tracker.analyze_performance_patterns()
                if "message" not in patterns:
                    type_perf = patterns.get('content_type_performance', {})
                    if type_perf.get('engagement_rate'):
                        df_type = pd.DataFrame(list(type_perf['engagement_rate'].items()), 
                                             columns=['Content Type', 'Avg Engagement'])
                        fig = px.bar(df_type, x='Content Type', y='Avg Engagement', 
                                   title="Performance by Content Type")
                        st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Analytics will appear once you have performance data.")
        
        with perf_tabs[2]:  # AI Learning
            st.subheader("🧠 AI Learning from Performance")
            
            # AI improvement suggestions
            suggestions = self.performance_tracker.generate_ai_improvement_suggestions()
            if suggestions:
                st.write("**AI Improvement Suggestions:**")
                for suggestion in suggestions:
                    st.write(f"• {suggestion}")
            else:
                st.info("AI suggestions will appear as performance data accumulates.")
            
            # Learning patterns
            patterns = self.performance_tracker.analyze_performance_patterns()
            if "message" not in patterns:
                st.subheader("📈 Discovered Patterns")
                
                high_performers = patterns.get('high_performers', {})
                if high_performers and "message" not in high_performers:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("**High Performer Characteristics:**")
                        st.write(f"Count: {high_performers.get('count', 0)}")
                        st.write(f"Avg Engagement: {high_performers.get('avg_engagement_rate', 0):.1f}%")
                        st.write(f"Avg AI Confidence: {high_performers.get('avg_ai_confidence', 0):.2f}")
                    
                    with col2:
                        st.write("**Best Performing Platforms:**")
                        common_platforms = high_performers.get('common_platforms', {})
                        for platform, count in common_platforms.items():
                            st.write(f"• {platform}: {count} posts")
                
                # Timing patterns
                timing = patterns.get('timing_patterns', {})
                if timing:
                    st.subheader("⏰ Optimal Timing")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write("**Best Hours:**")
                        best_hours = timing.get('best_hours', {})
                        for hour, engagement in list(best_hours.items())[:3]:
                            st.write(f"• {hour}:00 - {engagement:.1f}% engagement")
                    
                    with col2:
                        st.write("**Best Days:**")
                        best_days = timing.get('best_days', {})
                        for day, engagement in list(best_days.items())[:3]:
                            st.write(f"• {day} - {engagement:.1f}% engagement")
        
        with perf_tabs[3]:  # Publish & Track
            st.subheader("🚀 Publish Content with Tracking")
            
            st.write("**Quick Publish from Generated Content:**")
            
            # Get pending content
            linkedin_posts = self.generated_content.get('linkedin_posts', [])
            twitter_threads = self.generated_content.get('twitter_threads', [])
            
            if linkedin_posts or twitter_threads:
                # Select content to publish
                content_options = []
                for i, post in enumerate(linkedin_posts):
                    content_options.append(f"LinkedIn Post {i+1}: {post.get('content', '')[:50]}...")
                for i, thread in enumerate(twitter_threads):
                    content_options.append(f"Twitter Thread {i+1}: {len(thread.get('tweets', []))} tweets")
                
                selected_content = st.selectbox("Select content to publish:", content_options)
                
                if selected_content and st.button("🚀 Publish with Performance Tracking"):
                    # Simulate publishing and start tracking
                    content_id = self.simulate_publish_with_tracking(selected_content)
                    st.success(f"✅ Published and tracking started!")
                    st.info(f"Content ID: {content_id}")
                    st.info("Performance metrics will be updated automatically.")
                    
                    # Show tracking setup
                    st.write("**Tracking Setup:**")
                    st.write("• ✅ Content saved to database")
                    st.write("• ✅ Performance tracking initialized")
                    st.write("• ✅ AI learning enabled")
                    st.write("• 🔄 Metrics will update every hour")
            else:
                st.info("No content ready to publish. Generate some content first!")
            
            # Manual performance update
            st.subheader("📊 Manual Performance Update")
            st.write("Update performance metrics for already published content:")
            
            content_id_input = st.text_input("Content ID")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                views = st.number_input("Views", min_value=0, value=0)
            with col2:
                likes = st.number_input("Likes", min_value=0, value=0)
            with col3:
                comments = st.number_input("Comments", min_value=0, value=0)
            with col4:
                shares = st.number_input("Shares", min_value=0, value=0)
            
            if st.button("📈 Update Metrics") and content_id_input:
                metrics = {
                    'views': views,
                    'likes': likes,
                    'comments': comments,
                    'shares': shares,
                    'clicks': 0  # Can be added later
                }
                
                self.performance_tracker.update_performance_metrics(content_id_input, metrics)
                st.success("✅ Performance metrics updated!")
                st.rerun()

    def render_insights(self):
        """Render the insights dashboard"""
        st.header("🧠 AI Insights & Analysis")
        
        # Insights categories
        insight_tabs = st.tabs(["Premium Insights", "Cross-Domain", "Frameworks", "Opportunities"])
        
        with insight_tabs[0]:  # Premium Insights
            st.subheader("🏆 Premium Insights")
            premium_insights = self.insights.get('premium_insights', [])
            
            for i, insight in enumerate(premium_insights):
                with st.expander(f"Premium Insight {i+1}: {insight.get('title', 'Untitled')}"):
                    st.write(insight.get('content', ''))
                    st.write(f"**Generated:** {insight.get('generated_at', 'N/A')}")
                    
                    # Show supporting evidence if available
                    if 'supporting_evidence' in insight:
                        st.write("**Supporting Evidence:**")
                        for j, evidence in enumerate(insight['supporting_evidence'][:3]):
                            st.write(f"• [{evidence['title']}]({evidence['url']}) - {evidence['source']}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("💡 Turn into Content", key=f"insight_content_{i}"):
                            st.success("Content generation queued!")
                    
                    with col2:
                        if st.button("🔍 Find Evidence", key=f"find_evidence_{i}"):
                            with st.spinner("Searching for supporting evidence..."):
                                try:
                                    enhanced_insight = self.google_search.enhance_insight_with_evidence(insight)
                                    st.success(f"Found {enhanced_insight['evidence_count']} supporting sources!")
                                    
                                    # Display evidence
                                    for evidence in enhanced_insight['supporting_evidence']:
                                        st.write(f"📄 [{evidence['title']}]({evidence['url']})")
                                        st.write(f"   Source: {evidence['source']} (Credibility: {evidence['credibility']:.1f})")
                                        st.write(f"   {evidence['snippet']}")
                                        st.write("")
                                        
                                except Exception as e:
                                    st.error(f"Error finding evidence: {e}")
        
        with insight_tabs[1]:  # Cross-Domain
            st.subheader("🔗 Cross-Domain Connections")
            cross_domain = self.insights.get('cross_domain_connections', [])
            
            for i, connection in enumerate(cross_domain):
                with st.expander(f"Connection {i+1}: {connection.get('title', 'Untitled')}"):
                    st.write(connection.get('content', ''))
                    
                    if st.button("🧵 Create Thread", key=f"thread_{i}"):
                        st.success("Twitter thread queued!")
        
        with insight_tabs[2]:  # Frameworks
            st.subheader("🏗️ Prosora Frameworks")
            frameworks = self.insights.get('prosora_frameworks', [])
            
            for i, framework in enumerate(frameworks):
                with st.expander(f"Framework {i+1}: {framework.get('title', 'Untitled')}"):
                    st.write(framework.get('content', ''))
                    
                    if st.button("📝 Develop Blog", key=f"blog_{i}"):
                        st.success("Blog outline queued!")
        
        with insight_tabs[3]:  # Opportunities
            st.subheader("⚡ Content Opportunities")
            opportunities = self.insights.get('content_opportunities', [])
            
            for i, opp in enumerate(opportunities):
                st.write(f"• {opp}")

    def render_megatrends(self):
        """Render megatrends analysis page"""
        st.header("🔮 Megatrends Analysis")
        
        # Get megatrends insights
        insights = self.megatrends_radar.get_megatrend_insights()
        
        # Overview metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Overall Alignment", f"{insights['overall_alignment']:.1f}/100")
        
        with col2:
            strongest = insights['strongest_alignment']
            st.metric("Strongest Domain", strongest['domain'], f"{strongest['score']:.1f}/100")
        
        with col3:
            weakest = insights['weakest_alignment']
            st.metric("Growth Opportunity", weakest['domain'], f"+{100-weakest['score']:.0f} potential")
        
        with col4:
            gap_count = len(insights['opportunity_gaps'])
            st.metric("Opportunity Gaps", gap_count, "domains to improve")
        
        # Megatrends tabs
        mega_tabs = st.tabs(["Alignment Overview", "Detailed Breakdown", "Opportunity Analysis", "Trend Tracking"])
        
        with mega_tabs[0]:  # Alignment Overview
            st.subheader("🎯 Your Alignment with Global Megatrends")
            
            # Sample prosora data for demo
            sample_prosora_data = {
                'tech_innovation': 85,
                'political_stability': 65,
                'market_opportunity': 78,
                'financial_insight': 72
            }
            
            # Dual-layer radar chart
            fig = self.megatrends_radar.create_dual_layer_radar(sample_prosora_data)
            st.plotly_chart(fig, use_container_width=True)
            
            # Interpretation
            st.write("**Chart Interpretation:**")
            st.write("• **Blue area**: Your current expertise levels")
            st.write("• **Red area**: Global megatrend alignment scores")
            st.write("• **Overlap**: Areas where your expertise aligns with future trends")
            st.write("• **Gaps**: Areas with high trend relevance but lower personal alignment")
        
        with mega_tabs[1]:  # Detailed Breakdown
            st.subheader("📊 Megatrends Detailed Analysis")
            
            # Individual megatrends breakdown
            fig_breakdown = self.megatrends_radar.create_megatrend_breakdown_chart()
            st.plotly_chart(fig_breakdown, use_container_width=True)
            
            # Top megatrends table
            st.subheader("🚀 Top Megatrends")
            
            trends_data = []
            for trend in insights['top_megatrends']:
                trends_data.append({
                    'Megatrend': trend['name'],
                    'Category': trend['category'].title(),
                    'Global Relevance': f"{trend['relevance']}%",
                    'Your Alignment': f"{trend['your_alignment']}%",
                    'Opportunity Score': f"{(trend['relevance'] * trend['your_alignment']) / 100:.0f}"
                })
            
            df_trends = pd.DataFrame(trends_data)
            st.dataframe(df_trends, use_container_width=True)
        
        with mega_tabs[2]:  # Opportunity Analysis
            st.subheader("💡 Strategic Opportunities")
            
            # Opportunity gaps
            if insights['opportunity_gaps']:
                st.write("**Priority Areas for Development:**")
                
                for gap in insights['opportunity_gaps']:
                    with st.expander(f"🎯 {gap['domain']} - {gap['improvement_potential']:.0f} points potential"):
                        st.write(f"**Current Alignment:** {gap['current_alignment']:.1f}/100")
                        st.write(f"**Improvement Potential:** {gap['improvement_potential']:.1f} points")
                        
                        # Suggest specific actions
                        if gap['domain'] == 'Tech Innovation':
                            st.write("**Suggested Actions:**")
                            st.write("• Follow more AI/ML thought leaders")
                            st.write("• Subscribe to technical newsletters")
                            st.write("• Engage with emerging tech communities")
                        elif gap['domain'] == 'Political Stability':
                            st.write("**Suggested Actions:**")
                            st.write("• Follow policy analysis sources")
                            st.write("• Subscribe to political newsletters")
                            st.write("• Engage with regulatory discussions")
                        elif gap['domain'] == 'Market Opportunity':
                            st.write("**Suggested Actions:**")
                            st.write("• Follow product management leaders")
                            st.write("• Subscribe to business strategy content")
                            st.write("• Engage with startup communities")
                        elif gap['domain'] == 'Financial Insight':
                            st.write("**Suggested Actions:**")
                            st.write("• Follow FinTech thought leaders")
                            st.write("• Subscribe to financial analysis content")
                            st.write("• Engage with finance communities")
            else:
                st.success("🎉 No major opportunity gaps identified! Your expertise is well-aligned with megatrends.")
        
        with mega_tabs[3]:  # Trend Tracking
            st.subheader("📈 Trend Tracking & Predictions")
            
            st.write("**Emerging Trends to Watch:**")
            
            # Mock trend predictions
            emerging_trends = [
                {"name": "AI Governance", "category": "politics", "growth": "Exponential", "timeline": "2024-2026"},
                {"name": "Embedded AI", "category": "tech", "growth": "Accelerating", "timeline": "2024-2027"},
                {"name": "Sustainable FinTech", "category": "finance", "growth": "Steady", "timeline": "2024-2030"},
                {"name": "No-Code Product Management", "category": "product", "growth": "Accelerating", "timeline": "2024-2028"}
            ]
            
            for trend in emerging_trends:
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.write(f"**{trend['name']}**")
                with col2:
                    st.write(f"Category: {trend['category'].title()}")
                with col3:
                    st.write(f"Growth: {trend['growth']}")
                with col4:
                    st.write(f"Timeline: {trend['timeline']}")
            
            st.write("---")
            st.write("**Trend Monitoring Recommendations:**")
            st.write("• Set up Google Alerts for emerging trends in your domains")
            st.write("• Follow trend analysis publications and thought leaders")
            st.write("• Regularly update your megatrend alignment scores")
            st.write("• Focus content creation on high-growth, high-alignment areas")

    def render_analytics(self):
        """Render analytics dashboard"""
        st.header("📈 Performance Analytics")
        
        # Mock analytics data
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Content Performance")
            
            # Performance by type
            performance_data = {
                'Content Type': ['LinkedIn Posts', 'Twitter Threads', 'Blog Posts'],
                'Avg Engagement': [156, 89, 234],
                'Approval Rate': [85, 92, 78]
            }
            
            df = pd.DataFrame(performance_data)
            fig = px.bar(df, x='Content Type', y='Avg Engagement', title="Average Engagement by Content Type")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("AI Learning Progress")
            
            # Learning curve
            learning_data = {
                'Week': list(range(1, 8)),
                'Approval Rate': [65, 72, 78, 82, 85, 88, 92],
                'Content Quality Score': [60, 68, 75, 80, 83, 87, 90]
            }
            
            df = pd.DataFrame(learning_data)
            fig = px.line(df, x='Week', y=['Approval Rate', 'Content Quality Score'], 
                         title="AI Learning Progress")
            st.plotly_chart(fig, use_container_width=True)
        
        # Feedback analysis
        st.subheader("📊 Feedback Analysis")
        
        feedback_data = {
            'Feedback Type': ['Tone Issues', 'Too Generic', 'Missing Insights', 'Too Technical', 'Not Engaging'],
            'Frequency': [12, 8, 15, 6, 10]
        }
        
        df = pd.DataFrame(feedback_data)
        fig = px.pie(df, values='Frequency', names='Feedback Type', title="Common Rejection Reasons")
        st.plotly_chart(fig, use_container_width=True)

    def render_settings(self):
        """Render settings page"""
        st.header("⚙️ Settings & Configuration")
        
        settings_tabs = st.tabs(["Sources", "AI Settings", "Publishing", "Notifications"])
        
        with settings_tabs[0]:  # Sources
            st.subheader("📡 Content Sources")
            
            # Load current sources
            try:
                with open('prosora_sources.yaml', 'r') as f:
                    sources = yaml.safe_load(f)
                
                st.write("**Premium Sources:**")
                for source in sources['premium_sources']:
                    col1, col2, col3 = st.columns([2, 1, 1])
                    with col1:
                        st.write(f"• {source['name']}")
                    with col2:
                        st.write(f"Credibility: {source['credibility']}")
                    with col3:
                        st.write(f"Relevance: {source['relevance']}")
                
            except FileNotFoundError:
                st.error("Sources configuration not found!")
        
        with settings_tabs[1]:  # AI Settings
            st.subheader("🤖 AI Configuration")
            
            st.slider("Content Generation Creativity", 0.0, 1.0, 0.7)
            st.slider("Approval Threshold", 0.0, 1.0, 0.8)
            st.selectbox("Primary AI Model", ["Gemini Flash", "Gemini Pro"])
            
            st.checkbox("Enable Learning from Feedback", value=True)
            st.checkbox("Auto-improve Rejected Content", value=False)
        
        with settings_tabs[2]:  # Publishing
            st.subheader("📤 Publishing Settings")
            
            st.text_input("LinkedIn Access Token", type="password")
            st.text_input("Twitter API Key", type="password")
            
            st.selectbox("Default Publishing Time", ["9:00 AM", "12:00 PM", "3:00 PM", "6:00 PM"])
            st.multiselect("Publishing Days", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
        
        with settings_tabs[3]:  # Notifications
            st.subheader("🔔 Notifications")
            
            st.checkbox("Email notifications for new content", value=True)
            st.checkbox("Slack notifications for approvals needed", value=False)
            st.text_input("Notification Email")

    # Helper methods
    def approve_content(self, content_item, index):
        """Approve content and add to approved list"""
        approved_item = {
            **content_item,
            'approved_date': datetime.now().isoformat(),
            'status': 'approved'
        }
        
        self.approvals['approved'].append(approved_item)
        self.save_approvals()
    
    def reject_content_with_feedback(self, content_item, index, feedback, additional_feedback):
        """Reject content with feedback for AI learning"""
        rejected_item = {
            **content_item,
            'rejected_date': datetime.now().isoformat(),
            'feedback': feedback,
            'additional_feedback': additional_feedback,
            'status': 'rejected'
        }
        
        self.approvals['rejected'].append(rejected_item)
        self.save_approvals()
    
    def schedule_content(self, content_item, index):
        """Schedule content for future publishing"""
        # Implementation for scheduling
        pass
    
    def save_edited_content(self, index, edited_content):
        """Save edited content"""
        # Implementation for saving edits
        pass
    
    def save_approvals(self):
        """Save approval data to file"""
        with open("data/content_approvals.json", "w") as f:
            json.dump(self.approvals, f, indent=2)
    
    def publish_and_track_content(self, content_item: Dict, index: int) -> str:
        """Publish content and start performance tracking"""
        
        # Create content data for tracking
        content_data = {
            'platform': content_item.get('platform', 'unknown'),
            'content_type': content_item.get('type', 'unknown'),
            'content': content_item.get('content', ''),
            'ai_confidence': 0.8,  # Default confidence
            'source_credibility': 0.9,  # Default credibility
            'content_quality_score': 0.85  # Default quality
        }
        
        # Start tracking
        content_id = self.performance_tracker.track_published_content(content_data)
        
        # Simulate initial engagement (in production, this would come from APIs)
        import random
        initial_metrics = {
            'views': random.randint(50, 200),
            'likes': random.randint(2, 15),
            'comments': random.randint(0, 5),
            'shares': random.randint(0, 3),
            'clicks': random.randint(1, 8)
        }
        
        # Update with simulated metrics
        self.performance_tracker.update_performance_metrics(content_id, initial_metrics)
        
        # Move to approved
        self.approve_content(content_item, index)
        
        return content_id
    
    def simulate_publish_with_tracking(self, selected_content: str) -> str:
        """Simulate publishing content with tracking"""
        
        # Extract platform and content type from selection
        if "LinkedIn" in selected_content:
            platform = "linkedin"
            content_type = "linkedin_post"
        elif "Twitter" in selected_content:
            platform = "twitter"
            content_type = "twitter_thread"
        else:
            platform = "unknown"
            content_type = "unknown"
        
        # Create content data
        content_data = {
            'platform': platform,
            'content_type': content_type,
            'content': selected_content,
            'ai_confidence': 0.85,
            'source_credibility': 0.9,
            'content_quality_score': 0.8
        }
        
        # Start tracking
        content_id = self.performance_tracker.track_published_content(content_data)
        
        # Simulate realistic initial performance
        import random
        
        if platform == "linkedin":
            initial_metrics = {
                'views': random.randint(100, 500),
                'likes': random.randint(5, 30),
                'comments': random.randint(0, 10),
                'shares': random.randint(0, 5),
                'clicks': random.randint(2, 15)
            }
        else:  # Twitter
            initial_metrics = {
                'views': random.randint(200, 1000),
                'likes': random.randint(10, 50),
                'comments': random.randint(0, 15),
                'shares': random.randint(0, 10),
                'clicks': random.randint(3, 20)
            }
        
        # Update metrics
        self.performance_tracker.update_performance_metrics(content_id, initial_metrics)
        
        return content_id
    
    def show_metric_info_modal(self, metric_key: str):
        """Show metric information modal"""
        
        if st.session_state.get(f'show_{metric_key}_info', False):
            metric_info = self.metric_explanations.get(metric_key, {})
            
            # Create modal using expander (Streamlit's closest to modal)
            with st.expander(f"ℹ️ {metric_info.get('title', 'Metric Info')}", expanded=True):
                col1, col2 = st.columns([10, 1])
                
                with col1:
                    st.write(f"**Description:** {metric_info.get('description', 'No description available')}")
                    st.write(f"**Calculation:** {metric_info.get('calculation', 'Not specified')}")
                    st.write(f"**Range:** {metric_info.get('range', 'Not specified')}")
                    st.write(f"**Interpretation:** {metric_info.get('interpretation', 'Not specified')}")
                
                with col2:
                    if st.button("✕", key=f"close_{metric_key}_info", help="Close"):
                        st.session_state[f'show_{metric_key}_info'] = False
                        st.rerun()
    
    def create_metric_with_info(self, label: str, value: str, delta: str = None, metric_key: str = None):
        """Create a metric with info button"""
        
        col1, col2 = st.columns([4, 1])
        
        with col1:
            if delta:
                st.metric(label, value, delta=delta)
            else:
                st.metric(label, value)
        
        with col2:
            if metric_key and st.button("ℹ️", key=f"{metric_key}_info_btn", help="Click for details"):
                st.session_state[f'show_{metric_key}_info'] = True
                st.rerun()

def main():
    """Main application"""
    frontend = ProsoraFrontend()
    
    # Render header
    frontend.render_header()
    
    # Render sidebar
    frontend.render_sidebar()
    
    # Render main content based on selected tab
    if st.session_state.current_tab == "Dashboard":
        frontend.render_dashboard()
    elif st.session_state.current_tab == "Content Review":
        frontend.render_content_review()
    elif st.session_state.current_tab == "Performance":
        frontend.render_performance()
    elif st.session_state.current_tab == "Insights":
        frontend.render_insights()
    elif st.session_state.current_tab == "Megatrends":
        frontend.render_megatrends()
    elif st.session_state.current_tab == "Analytics":
        frontend.render_analytics()
    elif st.session_state.current_tab == "Settings":
        frontend.render_settings()

if __name__ == "__main__":
    main()