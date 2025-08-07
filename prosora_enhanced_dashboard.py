#!/usr/bin/env python3
"""
Prosora Enhanced Dashboard with Advanced Personalization Controls
Next-generation interface with comprehensive user control system
"""

import streamlit as st
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
import numpy as np
from typing import Dict, List

# Import enhanced controls and existing phases
from enhanced_personalization_controls import PersonalizationControlCenter, UserProfile
from phase5_self_improving_intelligence import Phase5SelfImprovingIntelligence
from learning_loop_engine import LearningEngine

# Page config
st.set_page_config(
    page_title="Prosora Enhanced Intelligence Dashboard",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

class ProsoraEnhancedDashboard:
    def __init__(self):
        # Initialize personalization control center
        self.control_center = PersonalizationControlCenter()
        
        # Initialize the complete Phase 5 system
        if 'prosora_engine' not in st.session_state:
            with st.spinner("🚀 Initializing Enhanced Prosora Intelligence Engine..."):
                st.session_state.prosora_engine = Phase5SelfImprovingIntelligence()
        self.engine = st.session_state.prosora_engine
        
        # Initialize session state
        if 'enhanced_results' not in st.session_state:
            st.session_state.enhanced_results = []
        if 'current_view' not in st.session_state:
            st.session_state.current_view = "Intelligence Engine"
        if 'demo_mode' not in st.session_state:
            st.session_state.demo_mode = False
        if 'show_personalization' not in st.session_state:
            st.session_state.show_personalization = False
    
    def render_enhanced_sidebar(self):
        """Enhanced sidebar with personalization controls"""
        st.sidebar.title("🧠 Prosora Enhanced Control Center")
        
        # Main view selector
        st.sidebar.subheader("📊 Main View")
        view_options = [
            "Intelligence Engine",
            "Personalization Center", 
            "Performance Analytics",
            "Learning Dashboard",
            "Multi-User Setup"
        ]
        
        st.session_state.current_view = st.sidebar.radio(
            "Select View:",
            view_options,
            index=view_options.index(st.session_state.current_view)
        )
        
        # Quick personalization toggle
        st.sidebar.subheader("🎛️ Quick Controls")
        st.session_state.show_personalization = st.sidebar.checkbox(
            "Show Personalization Panel", 
            value=st.session_state.show_personalization
        )
        
        # Demo mode
        st.session_state.demo_mode = st.sidebar.checkbox(
            "Demo Mode", 
            value=st.session_state.demo_mode
        )
        
        # Quick preset selector
        if st.session_state.current_view == "Intelligence Engine":
            st.sidebar.subheader("⚡ Quick Presets")
            preset_options = ["Custom", "Thought Leader", "Viral Content", "Research Mode", "Quick Insights"]
            selected_preset = st.sidebar.selectbox("Apply Preset:", preset_options)
            
            if selected_preset != "Custom" and st.sidebar.button("Apply"):
                self.apply_quick_preset(selected_preset)
                st.success(f"Applied {selected_preset} preset!")
                st.rerun()
        
        # System status
        st.sidebar.subheader("📈 System Status")
        self.render_system_status()
        
        # Profile summary
        if hasattr(st.session_state, 'user_profile'):
            st.sidebar.subheader("👤 Active Profile")
            profile = st.session_state.user_profile
            st.sidebar.write(f"**Style:** {profile.voice_style}")
            st.sidebar.write(f"**Complexity:** {profile.complexity_level}")
            st.sidebar.write(f"**Risk:** {profile.risk_tolerance}")
    
    def render_system_status(self):
        """Render system status indicators"""
        # Engine status
        engine_status = "🟢 Active" if hasattr(self, 'engine') else "🔴 Inactive"
        st.sidebar.write(f"**Engine:** {engine_status}")
        
        # Learning status
        if hasattr(self, 'engine') and hasattr(self.engine, 'learning_engine'):
            insights_count = len(self.engine.learning_engine.get_learning_insights(7))
            st.sidebar.write(f"**Learning Insights:** {insights_count}")
        
        # Results count
        results_count = len(st.session_state.enhanced_results)
        st.sidebar.write(f"**Generated Results:** {results_count}")
        
        # Performance metrics
        if st.session_state.enhanced_results:
            latest_result = st.session_state.enhanced_results[-1]
            if 'metrics' in latest_result:
                metrics = latest_result['metrics']
                avg_quality = np.mean([
                    getattr(metrics, 'query_clarity', 0),
                    getattr(metrics, 'content_authenticity', 0),
                    getattr(metrics, 'engagement_potential', 0)
                ])
                st.sidebar.metric("Avg Quality", f"{avg_quality:.2f}")
    
    def apply_quick_preset(self, preset_name: str):
        """Apply quick preset configurations"""
        presets = {
            "Thought Leader": {
                "voice_style": "Thought Leader",
                "complexity_level": "Expert",
                "contrarian_factor": 0.8,
                "evidence_requirement": "Heavy",
                "risk_tolerance": "Bold"
            },
            "Viral Content": {
                "voice_style": "Engaging",
                "content_preference": "Story-Driven",
                "contrarian_factor": 0.4,
                "complexity_level": "Moderate"
            },
            "Research Mode": {
                "voice_style": "Academic",
                "complexity_level": "Expert",
                "evidence_requirement": "Academic",
                "output_length": "Long"
            },
            "Quick Insights": {
                "voice_style": "Professional",
                "output_length": "Short",
                "complexity_level": "Simple",
                "freshness_weight": 0.9
            }
        }
        
        if preset_name in presets:
            settings = presets[preset_name]
            for key, value in settings.items():
                if hasattr(st.session_state.user_profile, key):
                    setattr(st.session_state.user_profile, key, value)
    
    def render_intelligence_engine_view(self):
        """Main intelligence engine interface with enhanced controls"""
        st.title("🧠 Enhanced Prosora Intelligence Engine")
        
        # Personalization panel (collapsible)
        if st.session_state.show_personalization:
            with st.expander("🎛️ Personalization Controls", expanded=True):
                self.control_center.render_smart_presets()
                
                col1, col2 = st.columns(2)
                with col1:
                    self.control_center.render_voice_style_controls()
                with col2:
                    self.control_center.render_generation_controls()
        
        # Main query interface
        st.subheader("💭 Intelligence Query")
        
        # Enhanced query input with context
        col1, col2 = st.columns([3, 1])
        
        with col1:
            query_text = st.text_area(
                "Enter your query:",
                placeholder="e.g., 'AI regulation impact on fintech startups'",
                height=100,
                help="Ask about trends, analysis, or insights in any domain"
            )
        
        with col2:
            st.write("**Query Enhancement:**")
            enhance_with_context = st.checkbox("Add Context", value=True)
            include_contrarian = st.checkbox("Contrarian View", value=True)
            real_time_sources = st.checkbox("Real-time Sources", value=True)
            
            # Query complexity indicator
            if query_text:
                complexity = self.estimate_query_complexity(query_text)
                st.metric("Query Complexity", complexity)
        
        # Advanced options (collapsible)
        with st.expander("⚙️ Advanced Generation Options"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                enable_learning = st.checkbox("Enable Learning Loop", value=True)
                force_variant = st.selectbox(
                    "Force Content Variant:",
                    ["Auto-select", "analytical", "engaging", "contrarian", "data_driven"]
                )
            
            with col2:
                learning_boost = st.slider("Learning Boost", 0.0, 0.5, 0.1, 0.05)
                performance_tracking = st.checkbox("Track Performance", value=True)
            
            with col3:
                output_format = st.selectbox(
                    "Output Format:",
                    ["Complete Analysis", "Key Insights Only", "Content Variants", "Research Report"]
                )
        
        # Generate button with enhanced processing
        if st.button("🚀 Generate Enhanced Intelligence", type="primary"):
            if query_text.strip():
                self.process_enhanced_query(
                    query_text, 
                    enhance_with_context,
                    include_contrarian,
                    real_time_sources,
                    enable_learning,
                    force_variant,
                    learning_boost,
                    performance_tracking,
                    output_format
                )
            else:
                st.warning("Please enter a query to analyze.")
        
        # Results display
        self.render_enhanced_results()
    
    def estimate_query_complexity(self, query: str) -> str:
        """Estimate query complexity based on content"""
        word_count = len(query.split())
        
        # Check for complex indicators
        complex_indicators = ['analysis', 'impact', 'correlation', 'framework', 'strategy']
        has_complex_terms = any(term in query.lower() for term in complex_indicators)
        
        if word_count > 15 or has_complex_terms:
            return "High"
        elif word_count > 8:
            return "Medium"
        else:
            return "Low"
    
    def process_enhanced_query(self, query: str, enhance_context: bool, 
                             include_contrarian: bool, real_time: bool,
                             enable_learning: bool, force_variant: str,
                             learning_boost: float, track_performance: bool,
                             output_format: str):
        """Process query with enhanced personalization"""
        
        with st.spinner("🧠 Processing with Enhanced Intelligence..."):
            start_time = time.time()
            
            try:
                # Apply user profile settings to engine
                self.apply_profile_to_engine()
                
                # Process query through Phase 5 system
                if st.session_state.demo_mode:
                    result = self.generate_demo_result(query)
                else:
                    result = self.engine.process_complete_intelligence(
                        query,
                        enable_learning=enable_learning,
                        simulate_performance=track_performance
                    )
                
                # Enhance result with personalization metadata
                enhanced_result = self.enhance_result_with_personalization(
                    result, query, output_format, time.time() - start_time
                )
                
                # Store result
                st.session_state.enhanced_results.append(enhanced_result)
                
                st.success(f"✅ Enhanced intelligence generated in {time.time() - start_time:.2f}s")
                
            except Exception as e:
                st.error(f"Error processing query: {str(e)}")
                if st.session_state.demo_mode:
                    st.info("Demo mode: Generating sample result...")
                    result = self.generate_demo_result(query)
                    st.session_state.enhanced_results.append(result)
    
    def apply_profile_to_engine(self):
        """Apply user profile settings to the intelligence engine"""
        profile = st.session_state.user_profile
        
        # This would integrate with the actual engine configuration
        # For now, we'll store the profile for use in result enhancement
        if hasattr(self.engine, 'set_personalization_config'):
            config = {
                'voice_style': profile.voice_style,
                'complexity_level': profile.complexity_level,
                'contrarian_factor': profile.contrarian_factor,
                'evidence_requirement': profile.evidence_requirement,
                'source_priorities': profile.source_priorities
            }
            self.engine.set_personalization_config(config)
    
    def enhance_result_with_personalization(self, result: Dict, query: str, 
                                          output_format: str, processing_time: float) -> Dict:
        """Enhance result with personalization metadata"""
        profile = st.session_state.user_profile
        
        enhanced_result = {
            'query': query,
            'result': result,
            'personalization': {
                'voice_style': profile.voice_style,
                'complexity_level': profile.complexity_level,
                'contrarian_factor': profile.contrarian_factor,
                'output_format': output_format
            },
            'metadata': {
                'timestamp': datetime.now(),
                'processing_time': processing_time,
                'profile_version': profile.last_updated,
                'demo_mode': st.session_state.demo_mode
            }
        }
        
        return enhanced_result
    
    def generate_demo_result(self, query: str) -> Dict:
        """Generate demo result for testing"""
        return {
            'query': query,
            'insights': [
                {
                    'title': f"Enhanced Analysis: {query}",
                    'content': f"This is a demo analysis of '{query}' with personalized insights based on your profile settings.",
                    'tier': 1,
                    'credibility': 0.85,
                    'domains': ['technology', 'business'],
                    'frameworks': ['strategic_analysis', 'trend_analysis']
                }
            ],
            'content': {
                'linkedin_posts': [{'content': f"Demo LinkedIn post about {query}"}],
                'twitter_threads': [{'content': f"Demo Twitter thread about {query}"}]
            },
            'metrics': {
                'query_clarity': 0.9,
                'content_authenticity': 0.85,
                'engagement_potential': 0.8
            }
        }
    
    def render_enhanced_results(self):
        """Render enhanced results with personalization insights"""
        if not st.session_state.enhanced_results:
            st.info("💡 Generate your first enhanced intelligence query above!")
            return
        
        st.subheader("📊 Enhanced Intelligence Results")
        
        # Results selector
        if len(st.session_state.enhanced_results) > 1:
            result_index = st.selectbox(
                "Select Result:",
                range(len(st.session_state.enhanced_results)),
                index=len(st.session_state.enhanced_results) - 1,
                format_func=lambda x: f"Query {x+1}: {st.session_state.enhanced_results[x]['query'][:50]}..."
            )
        else:
            result_index = 0
        
        result = st.session_state.enhanced_results[result_index]
        
        # Display result with enhanced formatting
        self.display_enhanced_result(result)
    
    def display_enhanced_result(self, result: Dict):
        """Display a single enhanced result"""
        # Header with personalization info
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.write(f"**Query:** {result['query']}")
        
        with col2:
            if 'personalization' in result:
                st.write(f"**Style:** {result['personalization']['voice_style']}")
        
        with col3:
            if 'metadata' in result:
                st.write(f"**Time:** {result['metadata']['processing_time']:.2f}s")
        
        # Main content tabs
        tab1, tab2, tab3, tab4 = st.tabs(["📝 Content", "📊 Analytics", "🎛️ Personalization", "🔍 Sources"])
        
        with tab1:
            self.render_content_tab(result)
        
        with tab2:
            self.render_analytics_tab(result)
        
        with tab3:
            self.render_personalization_tab(result)
        
        with tab4:
            self.render_sources_tab(result)
    
    def render_content_tab(self, result: Dict):
        """Render content results"""
        if 'result' in result and 'insights' in result['result']:
            for insight in result['result']['insights']:
                with st.expander(f"💡 {insight['title']}", expanded=True):
                    st.write(insight['content'])
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Tier", insight['tier'])
                    with col2:
                        st.metric("Credibility", f"{insight['credibility']:.2f}")
                    with col3:
                        st.metric("Domains", len(insight.get('domains', [])))
    
    def render_analytics_tab(self, result: Dict):
        """Render analytics and metrics"""
        if 'result' in result and 'metrics' in result['result']:
            metrics = result['result']['metrics']
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Query Clarity", f"{getattr(metrics, 'query_clarity', 0):.2f}")
            with col2:
                st.metric("Content Authenticity", f"{getattr(metrics, 'content_authenticity', 0):.2f}")
            with col3:
                st.metric("Engagement Potential", f"{getattr(metrics, 'engagement_potential', 0):.2f}")
    
    def render_personalization_tab(self, result: Dict):
        """Render personalization details"""
        if 'personalization' in result:
            pers = result['personalization']
            
            st.write("**Applied Personalization:**")
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"- Voice Style: {pers['voice_style']}")
                st.write(f"- Complexity: {pers['complexity_level']}")
            
            with col2:
                st.write(f"- Contrarian Factor: {pers['contrarian_factor']:.1f}")
                st.write(f"- Output Format: {pers['output_format']}")
    
    def render_sources_tab(self, result: Dict):
        """Render source information"""
        st.write("**Source Analysis:**")
        st.info("Source tracking and analysis will be displayed here.")
    
    def render_personalization_center_view(self):
        """Render the full personalization center"""
        self.control_center.render_complete_control_center()
    
    def render_performance_analytics_view(self):
        """Render performance analytics dashboard"""
        st.title("📊 Performance Analytics Dashboard")
        st.info("Advanced performance analytics coming soon!")
    
    def render_learning_dashboard_view(self):
        """Render learning dashboard"""
        st.title("🧠 Learning Dashboard")
        st.info("Learning insights and adaptation dashboard coming soon!")
    
    def render_multi_user_setup_view(self):
        """Render multi-user setup interface"""
        st.title("👥 Multi-User Setup")
        st.info("Multi-user collaboration features coming soon!")
    
    def run(self):
        """Main application runner"""
        # Render sidebar
        self.render_enhanced_sidebar()
        
        # Render main content based on selected view
        if st.session_state.current_view == "Intelligence Engine":
            self.render_intelligence_engine_view()
        elif st.session_state.current_view == "Personalization Center":
            self.render_personalization_center_view()
        elif st.session_state.current_view == "Performance Analytics":
            self.render_performance_analytics_view()
        elif st.session_state.current_view == "Learning Dashboard":
            self.render_learning_dashboard_view()
        elif st.session_state.current_view == "Multi-User Setup":
            self.render_multi_user_setup_view()

# Main execution
if __name__ == "__main__":
    dashboard = ProsoraEnhancedDashboard()
    dashboard.run()