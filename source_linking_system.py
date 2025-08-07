#!/usr/bin/env python3
"""
Advanced Source Linking and Performance Enhancement System
Provides granular control over source integration and output optimization
"""

import streamlit as st
import json
import yaml
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import hashlib
import re

@dataclass
class SourceConfig:
    """Configuration for individual sources"""
    name: str
    url: str
    priority: float
    credibility_score: float
    update_frequency: str  # hourly, daily, weekly
    content_type: str  # news, analysis, research, opinion
    geographic_focus: str
    domain_expertise: List[str]
    enabled: bool
    custom_filters: Dict[str, str]
    
@dataclass
class SourcePerformance:
    """Performance metrics for sources"""
    source_name: str
    articles_fetched: int
    articles_used: int
    avg_credibility: float
    avg_engagement_contribution: float
    last_successful_fetch: datetime
    error_count: int
    usage_trend: str  # increasing, stable, decreasing

class AdvancedSourceManager:
    """Advanced source management with performance tracking"""
    
    def __init__(self):
        self.initialize_default_sources()
        self.load_source_performance()
    
    def initialize_default_sources(self):
        """Initialize default source configurations"""
        if 'source_configs' not in st.session_state:
            st.session_state.source_configs = {
                'stratechery': SourceConfig(
                    name='Stratechery',
                    url='https://stratechery.com/feed/',
                    priority=0.95,
                    credibility_score=0.92,
                    update_frequency='daily',
                    content_type='analysis',
                    geographic_focus='global',
                    domain_expertise=['technology', 'business_strategy', 'platforms'],
                    enabled=True,
                    custom_filters={'min_word_count': '500'}
                ),
                'techcrunch': SourceConfig(
                    name='TechCrunch',
                    url='https://techcrunch.com/feed/',
                    priority=0.8,
                    credibility_score=0.75,
                    update_frequency='hourly',
                    content_type='news',
                    geographic_focus='global',
                    domain_expertise=['startups', 'venture_capital', 'technology'],
                    enabled=True,
                    custom_filters={'exclude_keywords': 'sponsored,advertisement'}
                ),
                'hacker_news': SourceConfig(
                    name='Hacker News',
                    url='https://hnrss.org/frontpage',
                    priority=0.7,
                    credibility_score=0.8,
                    update_frequency='hourly',
                    content_type='discussion',
                    geographic_focus='global',
                    domain_expertise=['technology', 'programming', 'startups'],
                    enabled=True,
                    custom_filters={'min_score': '50'}
                ),
                'reuters_tech': SourceConfig(
                    name='Reuters Technology',
                    url='https://feeds.reuters.com/reuters/technologyNews',
                    priority=0.85,
                    credibility_score=0.9,
                    update_frequency='hourly',
                    content_type='news',
                    geographic_focus='global',
                    domain_expertise=['technology', 'business', 'regulation'],
                    enabled=True,
                    custom_filters={}
                ),
                'bloomberg_tech': SourceConfig(
                    name='Bloomberg Technology',
                    url='https://feeds.bloomberg.com/technology/news.rss',
                    priority=0.9,
                    credibility_score=0.88,
                    update_frequency='hourly',
                    content_type='news',
                    geographic_focus='global',
                    domain_expertise=['technology', 'finance', 'markets'],
                    enabled=True,
                    custom_filters={}
                )
            }
    
    def load_source_performance(self):
        """Load source performance metrics"""
        if 'source_performance' not in st.session_state:
            st.session_state.source_performance = {}
            # Initialize with sample data
            for source_name in st.session_state.source_configs.keys():
                st.session_state.source_performance[source_name] = SourcePerformance(
                    source_name=source_name,
                    articles_fetched=100,
                    articles_used=25,
                    avg_credibility=0.8,
                    avg_engagement_contribution=0.7,
                    last_successful_fetch=datetime.now() - timedelta(hours=1),
                    error_count=0,
                    usage_trend='stable'
                )
    
    def render_source_management_dashboard(self):
        """Render comprehensive source management interface"""
        st.title("📰 Advanced Source Management")
        
        # Source overview metrics
        self.render_source_overview()
        
        st.divider()
        
        # Source configuration tabs
        tab1, tab2, tab3, tab4 = st.tabs([
            "🔧 Source Configuration", 
            "📊 Performance Analytics", 
            "🎯 Smart Filtering", 
            "🔄 Sync & Updates"
        ])
        
        with tab1:
            self.render_source_configuration()
        
        with tab2:
            self.render_source_performance_analytics()
        
        with tab3:
            self.render_smart_filtering()
        
        with tab4:
            self.render_sync_updates()
    
    def render_source_overview(self):
        """Render source overview metrics"""
        st.subheader("📈 Source Overview")
        
        # Calculate overview metrics
        total_sources = len(st.session_state.source_configs)
        enabled_sources = sum(1 for config in st.session_state.source_configs.values() if config.enabled)
        avg_credibility = sum(config.credibility_score for config in st.session_state.source_configs.values()) / total_sources
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Sources", total_sources)
        
        with col2:
            st.metric("Active Sources", enabled_sources)
        
        with col3:
            st.metric("Avg Credibility", f"{avg_credibility:.2f}")
        
        with col4:
            # Calculate total articles from performance data
            total_articles = sum(perf.articles_fetched for perf in st.session_state.source_performance.values())
            st.metric("Articles Fetched", total_articles)
    
    def render_source_configuration(self):
        """Render individual source configuration"""
        st.subheader("🔧 Source Configuration")
        
        # Source selector
        source_names = list(st.session_state.source_configs.keys())
        selected_source = st.selectbox("Select Source to Configure:", source_names)
        
        if selected_source:
            config = st.session_state.source_configs[selected_source]
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Basic Settings:**")
                
                # Enable/disable toggle
                config.enabled = st.checkbox(
                    "Source Enabled", 
                    value=config.enabled,
                    key=f"enabled_{selected_source}"
                )
                
                # Priority slider
                config.priority = st.slider(
                    "Priority Weight:",
                    0.0, 1.0, config.priority, 0.05,
                    help="Higher priority sources are weighted more heavily",
                    key=f"priority_{selected_source}"
                )
                
                # Credibility score
                config.credibility_score = st.slider(
                    "Credibility Score:",
                    0.0, 1.0, config.credibility_score, 0.05,
                    help="Manual credibility assessment",
                    key=f"credibility_{selected_source}"
                )
                
                # Update frequency
                config.update_frequency = st.selectbox(
                    "Update Frequency:",
                    ["hourly", "daily", "weekly"],
                    index=["hourly", "daily", "weekly"].index(config.update_frequency),
                    key=f"frequency_{selected_source}"
                )
            
            with col2:
                st.write("**Content Settings:**")
                
                # Content type
                config.content_type = st.selectbox(
                    "Content Type:",
                    ["news", "analysis", "research", "opinion", "discussion"],
                    index=["news", "analysis", "research", "opinion", "discussion"].index(config.content_type),
                    key=f"content_type_{selected_source}"
                )
                
                # Geographic focus
                config.geographic_focus = st.selectbox(
                    "Geographic Focus:",
                    ["global", "north_america", "europe", "asia", "us_only"],
                    index=["global", "north_america", "europe", "asia", "us_only"].index(config.geographic_focus),
                    key=f"geo_focus_{selected_source}"
                )
                
                # Domain expertise (multiselect)
                expertise_options = [
                    "technology", "business_strategy", "startups", "venture_capital",
                    "artificial_intelligence", "fintech", "healthcare", "regulation",
                    "markets", "programming", "platforms", "cybersecurity"
                ]
                
                config.domain_expertise = st.multiselect(
                    "Domain Expertise:",
                    expertise_options,
                    default=config.domain_expertise,
                    key=f"expertise_{selected_source}"
                )
            
            # Custom filters section
            st.write("**Custom Filters:**")
            self.render_custom_filters(config, selected_source)
            
            # Save configuration
            if st.button("💾 Save Configuration", key=f"save_{selected_source}"):
                st.session_state.source_configs[selected_source] = config
                st.success(f"Configuration saved for {config.name}!")
    
    def render_custom_filters(self, config: SourceConfig, source_key: str):
        """Render custom filters interface"""
        col1, col2 = st.columns(2)
        
        with col1:
            # Keyword filters
            include_keywords = st.text_input(
                "Include Keywords (comma-separated):",
                value=config.custom_filters.get('include_keywords', ''),
                key=f"include_kw_{source_key}"
            )
            
            exclude_keywords = st.text_input(
                "Exclude Keywords (comma-separated):",
                value=config.custom_filters.get('exclude_keywords', ''),
                key=f"exclude_kw_{source_key}"
            )
        
        with col2:
            # Numeric filters
            min_word_count = st.number_input(
                "Minimum Word Count:",
                value=int(config.custom_filters.get('min_word_count', 0)),
                min_value=0,
                key=f"min_words_{source_key}"
            )
            
            min_score = st.number_input(
                "Minimum Score (if applicable):",
                value=int(config.custom_filters.get('min_score', 0)),
                min_value=0,
                key=f"min_score_{source_key}"
            )
        
        # Update custom filters
        config.custom_filters.update({
            'include_keywords': include_keywords,
            'exclude_keywords': exclude_keywords,
            'min_word_count': str(min_word_count),
            'min_score': str(min_score)
        })
    
    def render_source_performance_analytics(self):
        """Render source performance analytics"""
        st.subheader("📊 Source Performance Analytics")
        
        # Performance overview table
        performance_data = []
        for source_name, perf in st.session_state.source_performance.items():
            config = st.session_state.source_configs.get(source_name)
            if config:
                usage_rate = (perf.articles_used / perf.articles_fetched * 100) if perf.articles_fetched > 0 else 0
                performance_data.append({
                    'Source': config.name,
                    'Enabled': '✅' if config.enabled else '❌',
                    'Priority': f"{config.priority:.2f}",
                    'Articles Fetched': perf.articles_fetched,
                    'Articles Used': perf.articles_used,
                    'Usage Rate': f"{usage_rate:.1f}%",
                    'Avg Credibility': f"{perf.avg_credibility:.2f}",
                    'Engagement Contribution': f"{perf.avg_engagement_contribution:.2f}",
                    'Errors': perf.error_count,
                    'Trend': perf.usage_trend
                })
        
        if performance_data:
            import pandas as pd
            df = pd.DataFrame(performance_data)
            st.dataframe(df, use_container_width=True)
            
            # Performance insights
            st.subheader("🔍 Performance Insights")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Top performing sources
                st.write("**Top Performing Sources:**")
                top_sources = sorted(performance_data, key=lambda x: float(x['Usage Rate'].rstrip('%')), reverse=True)[:3]
                for i, source in enumerate(top_sources, 1):
                    st.write(f"{i}. {source['Source']} ({source['Usage Rate']})")
            
            with col2:
                # Sources needing attention
                st.write("**Sources Needing Attention:**")
                problem_sources = [s for s in performance_data if s['Errors'] > 0 or float(s['Usage Rate'].rstrip('%')) < 10]
                if problem_sources:
                    for source in problem_sources[:3]:
                        st.write(f"⚠️ {source['Source']} - {source['Errors']} errors, {source['Usage Rate']} usage")
                else:
                    st.write("✅ All sources performing well!")
    
    def render_smart_filtering(self):
        """Render smart filtering interface"""
        st.subheader("🎯 Smart Content Filtering")
        
        # Global filtering rules
        st.write("**Global Filtering Rules:**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Content quality filters
            st.write("*Content Quality:*")
            min_credibility = st.slider("Minimum Credibility Threshold:", 0.0, 1.0, 0.6, 0.05)
            min_word_count = st.number_input("Minimum Article Length:", value=200, min_value=0)
            
            # Freshness filters
            st.write("*Freshness:*")
            max_age_hours = st.number_input("Maximum Article Age (hours):", value=72, min_value=1)
            prioritize_recent = st.checkbox("Prioritize Recent Content", value=True)
        
        with col2:
            # Topic relevance filters
            st.write("*Topic Relevance:*")
            relevance_threshold = st.slider("Relevance Threshold:", 0.0, 1.0, 0.5, 0.05)
            
            # Language and region filters
            st.write("*Language & Region:*")
            languages = st.multiselect("Languages:", ["English", "Spanish", "French", "German"], default=["English"])
            regions = st.multiselect("Regions:", ["Global", "US", "Europe", "Asia"], default=["Global"])
        
        # Advanced filtering rules
        with st.expander("🔬 Advanced Filtering Rules"):
            st.write("**Semantic Filtering:**")
            
            col1, col2 = st.columns(2)
            
            with col1:
                semantic_similarity = st.checkbox("Enable Semantic Similarity Filtering", value=True)
                if semantic_similarity:
                    similarity_threshold = st.slider("Similarity Threshold:", 0.0, 1.0, 0.7, 0.05)
                
                duplicate_detection = st.checkbox("Duplicate Content Detection", value=True)
            
            with col2:
                sentiment_filtering = st.checkbox("Sentiment-based Filtering", value=False)
                if sentiment_filtering:
                    sentiment_preference = st.selectbox("Sentiment Preference:", 
                                                      ["Neutral", "Positive", "Negative", "Mixed"])
                
                trending_boost = st.checkbox("Boost Trending Topics", value=True)
        
        # Apply filters button
        if st.button("🎯 Apply Smart Filters"):
            self.apply_smart_filters({
                'min_credibility': min_credibility,
                'min_word_count': min_word_count,
                'max_age_hours': max_age_hours,
                'relevance_threshold': relevance_threshold,
                'languages': languages,
                'regions': regions
            })
            st.success("Smart filters applied successfully!")
    
    def apply_smart_filters(self, filter_config: Dict):
        """Apply smart filtering configuration"""
        # Store filter configuration in session state
        st.session_state.smart_filters = filter_config
        
        # This would integrate with the actual content fetching system
        # For now, we'll just store the configuration
        pass
    
    def render_sync_updates(self):
        """Render sync and updates interface"""
        st.subheader("🔄 Sync & Updates")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Manual Sync Controls:**")
            
            if st.button("🔄 Sync All Sources"):
                self.sync_all_sources()
            
            if st.button("🧹 Clear Cache"):
                self.clear_source_cache()
            
            if st.button("📊 Refresh Performance Data"):
                self.refresh_performance_data()
        
        with col2:
            st.write("**Automatic Sync Settings:**")
            
            auto_sync_enabled = st.checkbox("Enable Auto-Sync", value=True)
            
            if auto_sync_enabled:
                sync_interval = st.selectbox("Sync Interval:", 
                                           ["15 minutes", "30 minutes", "1 hour", "2 hours", "4 hours"])
                
                sync_on_query = st.checkbox("Sync on New Query", value=True)
        
        # Sync status
        st.write("**Sync Status:**")
        
        # Mock sync status data
        sync_status = {
            'last_sync': datetime.now() - timedelta(minutes=15),
            'next_sync': datetime.now() + timedelta(minutes=45),
            'sources_synced': 5,
            'articles_updated': 23,
            'errors': 0
        }
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Last Sync", sync_status['last_sync'].strftime("%H:%M"))
        
        with col2:
            st.metric("Articles Updated", sync_status['articles_updated'])
        
        with col3:
            st.metric("Sync Errors", sync_status['errors'])
    
    def sync_all_sources(self):
        """Sync all enabled sources"""
        with st.spinner("Syncing all sources..."):
            # Mock sync process
            import time
            time.sleep(2)
            st.success("All sources synced successfully!")
    
    def clear_source_cache(self):
        """Clear source cache"""
        with st.spinner("Clearing cache..."):
            # Mock cache clearing
            import time
            time.sleep(1)
            st.success("Cache cleared successfully!")
    
    def refresh_performance_data(self):
        """Refresh performance data"""
        with st.spinner("Refreshing performance data..."):
            # Mock performance data refresh
            import time
            time.sleep(1)
            st.success("Performance data refreshed!")
    
    def get_active_source_configs(self) -> Dict[str, SourceConfig]:
        """Get all active source configurations"""
        return {name: config for name, config in st.session_state.source_configs.items() if config.enabled}
    
    def get_source_priorities(self) -> Dict[str, float]:
        """Get source priority weights"""
        return {name: config.priority for name, config in st.session_state.source_configs.items() if config.enabled}

# Usage example
if __name__ == "__main__":
    source_manager = AdvancedSourceManager()
    source_manager.render_source_management_dashboard()