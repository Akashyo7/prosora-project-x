#!/usr/bin/env python3
"""
Prosora Complete Intelligence Dashboard
Comprehensive Streamlit interface showcasing all 5 phases working together
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

# Import all phases
from phase5_self_improving_intelligence import Phase5SelfImprovingIntelligence
from learning_loop_engine import LearningEngine

# Page config
st.set_page_config(
    page_title="Prosora Complete Intelligence Dashboard",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

class ProsoraCompleteDashboard:
    def __init__(self):
        # Initialize the complete Phase 5 system
        if 'prosora_engine' not in st.session_state:
            with st.spinner("🚀 Initializing Complete Prosora Intelligence Engine..."):
                st.session_state.prosora_engine = Phase5SelfImprovingIntelligence()
        self.engine = st.session_state.prosora_engine
        
        # Initialize session state
        if 'complete_results' not in st.session_state:
            st.session_state.complete_results = []
        if 'current_phase' not in st.session_state:
            st.session_state.current_phase = "Complete System"
        if 'demo_mode' not in st.session_state:
            st.session_state.demo_mode = False
    
    def safe_get_metric(self, metrics, key, default=0):
        """Safely get metric value from either dataclass or dict"""
        try:
            if hasattr(metrics, key):
                return getattr(metrics, key)
            elif isinstance(metrics, dict):
                return metrics.get(key, default)
            else:
                return default
        except:
            return default
    
    def render_header(self):
        """Render the main header with system overview"""
        st.title("🧠 Prosora Complete Intelligence Dashboard")
        st.caption("All 5 Phases Working Together - The Ultimate Content Intelligence Engine")
        
        # System status overview
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        
        with col1:
            st.metric("🤖 AI Status", "✅ Online" if self.engine.ai_available else "⚠️ Offline")
        with col2:
            st.metric("📡 Real Sources", "✅ Active")
        with col3:
            st.metric("🎯 Personalization", "✅ Active")
        with col4:
            st.metric("🔄 Optimization", "✅ Active")
        with col5:
            st.metric("🧠 Learning Loop", "✅ Active")
        with col6:
            st.metric("Total Queries", len(st.session_state.complete_results))
        
        # Phase progression indicator
        st.subheader("🚀 Complete Intelligence Pipeline")
        
        phases = [
            ("Phase 1", "Smart Query Analysis", "✅"),
            ("Phase 2", "Real Source Integration", "✅"),
            ("Phase 3", "Voice Personalization", "✅"),
            ("Phase 4", "Content Optimization", "✅"),
            ("Phase 5", "Self-Improving Learning", "✅")
        ]
        
        cols = st.columns(5)
        for i, (phase, description, status) in enumerate(phases):
            with cols[i]:
                st.info(f"**{phase}**\n{description}\n{status}")
    
    def render_sidebar(self):
        """Render enhanced sidebar with all controls"""
        st.sidebar.title("🧠 Prosora Control Center")
        
        # Phase selector
        st.sidebar.subheader("📊 View Mode")
        view_mode = st.sidebar.radio(
            "Select View:",
            ["Complete System", "Phase Comparison", "Learning Analytics", "Performance Tracking"]
        )
        st.session_state.current_phase = view_mode
        
        # Demo mode toggle
        st.sidebar.subheader("🎮 Demo Controls")
        st.session_state.demo_mode = st.sidebar.checkbox("Demo Mode", value=st.session_state.demo_mode)
        
        if st.session_state.demo_mode:
            st.sidebar.info("🎮 Demo mode: Simulates performance data for testing")
        
        # Quick actions
        st.sidebar.subheader("⚡ Quick Actions")
        if st.sidebar.button("🔄 Run System Test"):
            self.run_system_test()
        
        if st.sidebar.button("📊 Generate Sample Data"):
            self.generate_sample_data()
        
        if st.sidebar.button("🧹 Clear Results"):
            st.session_state.complete_results = []
            st.rerun()
        
        # System metrics
        st.sidebar.subheader("📈 System Metrics")
        if st.session_state.complete_results:
            latest_result = st.session_state.complete_results[-1]
            metrics = latest_result.get('metrics', {})
            
            st.sidebar.metric("Last Query Clarity", f"{self.safe_get_metric(metrics, 'query_clarity'):.2f}")
            st.sidebar.metric("Content Authenticity", f"{self.safe_get_metric(metrics, 'content_authenticity'):.2f}")
            st.sidebar.metric("Engagement Potential", f"{self.safe_get_metric(metrics, 'engagement_potential'):.2f}")
        
        # Learning insights
        st.sidebar.subheader("🧠 Learning Status")
        learning_insights = self.engine.learning_engine.get_learning_insights(7)
        st.sidebar.write(f"Active Insights: {len(learning_insights)}")
        
        if learning_insights:
            latest_insight = learning_insights[0]
            st.sidebar.write(f"**Latest:** {latest_insight['type']}")
            st.sidebar.write(f"Impact: {latest_insight['impact_score']:.2f}")
    
    def render_query_interface(self):
        """Enhanced query interface for complete system"""
        st.header("🔍 Complete Intelligence Query Interface")
        
        # Query input with advanced options
        col1, col2 = st.columns([3, 1])
        
        with col1:
            query_text = st.text_input(
                "Enter your intelligence query:",
                placeholder="e.g., AI regulation impact on fintech product strategy",
                help="The complete system will process through all 5 phases automatically"
            )
        
        with col2:
            st.write("")
            st.write("")
            process_button = st.button("🚀 Process with Complete System", type="primary")
        
        # Advanced options
        with st.expander("🔧 Advanced System Options", expanded=False):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                enable_learning = st.checkbox("Enable Learning Loop", value=True)
                simulate_performance = st.checkbox("Simulate Performance", value=st.session_state.demo_mode)
            
            with col2:
                force_variant = st.selectbox(
                    "Force Recommended Variant:",
                    ["Auto-select", "analytical", "engaging", "contrarian", "data_driven"]
                )
            
            with col3:
                learning_boost = st.slider("Learning Boost Factor", 0.0, 0.5, 0.1, 0.05)
        
        # Example queries by complexity
        st.write("**🎯 Example Queries by Intelligence Level:**")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write("**🟢 Cross-Domain Analysis:**")
            if st.button("Tech × Policy Strategy"):
                query_text = "Technology platform strategy in regulated environments"
                process_button = True
            if st.button("Product × Finance Innovation"):
                query_text = "Product innovation strategies in fintech and embedded finance"
                process_button = True
        
        with col2:
            st.write("**🟡 Framework-Driven:**")
            if st.button("IIT-MBA Leadership"):
                query_text = "Engineering leadership principles in product management scaling"
                process_button = True
            if st.button("Political Product Strategy"):
                query_text = "Building products in politically sensitive and regulated markets"
                process_button = True
        
        with col3:
            st.write("**🔴 Contrarian Intelligence:**")
            if st.button("Contrarian AI Analysis"):
                query_text = "Contrarian analysis of AI productivity claims and investment hype"
                process_button = True
            if st.button("Contrarian Remote Work"):
                query_text = "Contrarian perspective on remote work effectiveness in high-growth startups"
                process_button = True
        
        # Process with complete system
        if process_button and query_text:
            self.process_complete_query(query_text, enable_learning, simulate_performance)
    
    def process_complete_query(self, query_text: str, enable_learning: bool, simulate_performance: bool):
        """Process query through complete system with progress tracking"""
        
        with st.spinner("🧠 Processing through complete intelligence pipeline..."):
            # Create progress tracking
            progress_container = st.container()
            
            with progress_container:
                progress_bar = st.progress(0)
                status_text = st.empty()
                phase_status = st.empty()
                
                # Phase 1: Query Analysis
                status_text.text("Phase 1: 🔍 Smart Query Analysis with AI...")
                phase_status.info("Analyzing intent, domains, complexity, and personal frameworks")
                progress_bar.progress(20)
                time.sleep(0.5)
                
                # Phase 2: Real Source Fetching
                status_text.text("Phase 2: 📡 Real Source Integration...")
                phase_status.info("Fetching from RSS feeds, analyzing credibility and freshness")
                progress_bar.progress(40)
                time.sleep(0.5)
                
                # Phase 3: Personalization
                status_text.text("Phase 3: 🎯 Voice Personalization & Frameworks...")
                phase_status.info("Applying your personal voice, expertise, and frameworks")
                progress_bar.progress(60)
                time.sleep(0.5)
                
                # Phase 4: Optimization
                status_text.text("Phase 4: 🔄 Content Optimization & A/B Testing...")
                phase_status.info("Generating variants, predicting engagement, optimizing")
                progress_bar.progress(80)
                time.sleep(0.5)
                
                # Phase 5: Learning Enhancement
                status_text.text("Phase 5: 🧠 Self-Improving Learning Loop...")
                phase_status.info("Applying learned patterns, enhancing predictions")
                progress_bar.progress(90)
                time.sleep(0.5)
                
                try:
                    # Process with Phase 5 system
                    start_time = time.time()
                    response, metrics = self.engine.process_query_with_self_improvement(query_text)
                    processing_time = time.time() - start_time
                    
                    # Simulate performance feedback if enabled
                    performance_feedback = None
                    if simulate_performance and 'error' not in response:
                        content_id = response.get('self_improving_content', {}).get('performance_tracking_id', 'test')
                        predicted = response.get('learning_summary', {}).get('max_learning_enhanced_engagement', 0.5)
                        performance_feedback = self.engine.simulate_performance_feedback(
                            content_id, 'analytical', predicted
                        )
                    
                    # Store complete results
                    result_data = {
                        'timestamp': datetime.now(),
                        'query': query_text,
                        'response': response,
                        'metrics': metrics,
                        'processing_time': processing_time,
                        'performance_feedback': performance_feedback,
                        'phases_completed': 5
                    }
                    st.session_state.complete_results.append(result_data)
                    
                    # Complete
                    status_text.text("✅ Complete Intelligence Processing Finished!")
                    phase_status.success(f"All 5 phases completed in {processing_time:.2f}s")
                    progress_bar.progress(100)
                    
                    # Clear progress after delay
                    time.sleep(1)
                    progress_bar.empty()
                    status_text.empty()
                    phase_status.empty()
                    
                    # Show success summary
                    if 'error' not in response:
                        learning_summary = response.get('learning_summary', {})
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            st.success(f"**Patterns Applied:** {learning_summary.get('patterns_applied', 0)}")
                        with col2:
                            st.success(f"**Learning Boost:** +{learning_summary.get('learning_boost', 0):.3f}")
                        with col3:
                            st.success(f"**Max Engagement:** {learning_summary.get('max_learning_enhanced_engagement', 0):.2f}")
                        with col4:
                            st.success(f"**Processing Time:** {processing_time:.2f}s")
                        
                        if performance_feedback:
                            st.info(f"🎯 **Simulated Performance:** {performance_feedback['actual_engagement']:.2f} engagement (Accuracy: {1-performance_feedback['prediction_accuracy']:.2f})")
                    
                    st.rerun()
                    
                except Exception as e:
                    status_text.text("❌ Processing failed")
                    phase_status.error(f"Error: {e}")
                    progress_bar.empty()
                    st.error(f"Complete system processing failed: {e}")
    
    def render_complete_results(self):
        """Render comprehensive results from all phases"""
        if not st.session_state.complete_results:
            st.info("👆 Enter a query above to see complete intelligence results from all 5 phases")
            return
        
        latest_result = st.session_state.complete_results[-1]
        response = latest_result['response']
        metrics = latest_result['metrics']
        
        if st.session_state.current_phase == "Complete System":
            self.render_complete_system_view(latest_result)
        elif st.session_state.current_phase == "Phase Comparison":
            self.render_phase_comparison_view()
        elif st.session_state.current_phase == "Learning Analytics":
            self.render_learning_analytics_view()
        elif st.session_state.current_phase == "Performance Tracking":
            self.render_performance_tracking_view()
    
    def render_complete_system_view(self, latest_result):
        """Render complete system results view"""
        response = latest_result['response']
        metrics = latest_result['metrics']
        
        st.header("🧠 Complete Intelligence Results")
        
        # Phase-by-phase breakdown
        st.subheader("📊 Phase-by-Phase Analysis")
        
        phase_tabs = st.tabs([
            "Phase 1: Query Analysis", 
            "Phase 2: Real Sources", 
            "Phase 3: Personalization", 
            "Phase 4: Optimization", 
            "Phase 5: Learning"
        ])
        
        with phase_tabs[0]:  # Phase 1
            if 'personalized_query_analysis' in response:
                analysis = response['personalized_query_analysis']
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Intent Detected", analysis['intent'])
                    st.metric("Confidence", f"{analysis['intent_confidence']:.2f}")
                
                with col2:
                    st.metric("Domains Found", len(analysis['domains']))
                    st.metric("Complexity", analysis['complexity'])
                
                with col3:
                    st.metric("Frameworks", len(analysis.get('personal_frameworks', [])))
                    st.metric("Voice Style", analysis.get('voice_style', 'N/A'))
                
                # Domain weights visualization
                if analysis.get('domain_weights'):
                    domain_df = pd.DataFrame([
                        {'Domain': domain, 'Weight': weight} 
                        for domain, weight in analysis['domain_weights'].items()
                    ])
                    
                    fig = px.bar(domain_df, x='Domain', y='Weight', 
                               title="Domain Relevance Analysis")
                    st.plotly_chart(fig, use_container_width=True)
                
                # Personal frameworks
                if analysis.get('personal_frameworks'):
                    st.write("**🎯 Personal Frameworks Applied:**")
                    for framework in analysis['personal_frameworks']:
                        st.write(f"• {framework}")
        
        with phase_tabs[1]:  # Phase 2
            st.metric("Real Sources Fetched", response.get('real_sources_fetched', 0))
            
            if 'real_sources_summary' in response and response['real_sources_summary']:
                sources_df = pd.DataFrame(response['real_sources_summary'])
                
                col1, col2 = st.columns(2)
                
                with col1:
                    fig = px.scatter(sources_df, x='freshness', y='credibility', 
                                   size='credibility', hover_data=['source'],
                                   title="Source Quality Matrix")
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    st.write("**📡 Real Sources Used:**")
                    for _, source in sources_df.iterrows():
                        st.write(f"• **{source['source']}** (Credibility: {source['credibility']:.2f})")
                        st.write(f"  📰 {source['title'][:60]}...")
                        st.write(f"  🔗 [Link]({source['url']})")
        
        with phase_tabs[2]:  # Phase 3
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Content Authenticity", f"{self.safe_get_metric(metrics, 'content_authenticity'):.2f}")
            with col2:
                st.metric("Voice Personalization", "✅ Active")
            with col3:
                st.metric("Cross-Domain Rate", f"{self.safe_get_metric(metrics, 'cross_domain_rate'):.2f}")
            
            # Voice personalization details
            if 'voice_personalization' in response:
                voice_data = response['voice_personalization']
                st.write("**🗣️ Voice Personalization Applied:**")
                st.write(f"• Style: {voice_data.get('voice_style', 'N/A')}")
                st.write(f"• Frameworks: {len(voice_data.get('frameworks_applied', []))}")
                st.write(f"• Authenticity: {voice_data.get('authenticity_score', 0):.2f}")
        
        with phase_tabs[3]:  # Phase 4
            if 'self_improving_content' in response:
                content = response['self_improving_content']
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Variants Generated", len(content.get('variants', {})))
                with col2:
                    st.metric("Recommended Variant", content.get('recommended_variant', 'N/A'))
                with col3:
                    st.metric("Max Engagement Pred", f"{max(content.get('engagement_predictions', {0: 0}).values()):.2f}")
                with col4:
                    st.metric("A/B Test Ready", "✅ Yes")
                
                # Engagement predictions comparison
                if content.get('engagement_predictions') and content.get('learning_enhanced_predictions'):
                    pred_df = pd.DataFrame([
                        {'Variant': variant, 'Base Prediction': base_pred, 
                         'Learning Enhanced': content['learning_enhanced_predictions'].get(variant, base_pred)}
                        for variant, base_pred in content['engagement_predictions'].items()
                    ])
                    
                    fig = px.bar(pred_df, x='Variant', y=['Base Prediction', 'Learning Enhanced'],
                               title="Engagement Predictions: Base vs Learning Enhanced",
                               barmode='group')
                    st.plotly_chart(fig, use_container_width=True)
        
        with phase_tabs[4]:  # Phase 5
            if 'learning_summary' in response:
                learning = response['learning_summary']
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Patterns Applied", learning.get('patterns_applied', 0))
                with col2:
                    st.metric("Learning Boost", f"+{learning.get('learning_boost', 0):.3f}")
                with col3:
                    st.metric("Recommendations Used", learning.get('recommendations_used', 0))
                with col4:
                    st.metric("Improvement", f"+{learning.get('improvement_over_base', 0):.3f}")
                
                # Learning enhancement visualization
                if learning.get('learning_boost', 0) > 0:
                    st.success(f"🧠 **Learning Enhancement Active:** +{learning['learning_boost']:.3f} engagement boost applied")
                
                # Performance feedback if available
                if latest_result.get('performance_feedback'):
                    feedback = latest_result['performance_feedback']
                    st.write("**🎯 Simulated Performance Feedback:**")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Actual Engagement", f"{feedback['actual_engagement']:.2f}")
                    with col2:
                        st.metric("Prediction Accuracy", f"{1-feedback['prediction_accuracy']:.2f}")
                    with col3:
                        st.metric("Performance Tier", feedback['performance_tier'].title())
        
        # Generated Content Showcase
        st.subheader("📝 Generated Content (All Variants)")
        
        if 'self_improving_content' in response:
            content = response['self_improving_content']
            
            if content.get('variants'):
                for variant_name, variant_content in content['variants'].items():
                    with st.expander(f"📄 {variant_name.title()} Variant - Engagement: {content.get('learning_enhanced_predictions', {}).get(variant_name, 0):.2f}"):
                        st.text_area("Content", variant_content, height=200, key=f"complete_{variant_name}")
                        
                        # Variant metrics
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Base Prediction", f"{content.get('engagement_predictions', {}).get(variant_name, 0):.2f}")
                        with col2:
                            st.metric("Learning Enhanced", f"{content.get('learning_enhanced_predictions', {}).get(variant_name, 0):.2f}")
                        with col3:
                            boost = content.get('learning_enhanced_predictions', {}).get(variant_name, 0) - content.get('engagement_predictions', {}).get(variant_name, 0)
                            st.metric("Learning Boost", f"+{boost:.3f}")
    
    def render_phase_comparison_view(self):
        """Render phase comparison analytics"""
        st.header("📊 Phase Comparison Analytics")
        
        if len(st.session_state.complete_results) < 2:
            st.info("Need at least 2 queries to show phase comparison")
            return
        
        # Prepare comparison data
        comparison_data = []
        for result in st.session_state.complete_results[-10:]:
            metrics = result['metrics']
            response = result['response']
            
            learning_summary = response.get('learning_summary', {})
            
            comparison_data.append({
                'timestamp': result['timestamp'],
                'query': result['query'][:30] + "...",
                'phase1_clarity': self.safe_get_metric(metrics, 'query_clarity'),
                'phase2_source_quality': self.safe_get_metric(metrics, 'source_quality_score'),
                'phase3_authenticity': self.safe_get_metric(metrics, 'content_authenticity'),
                'phase4_engagement': self.safe_get_metric(metrics, 'engagement_potential'),
                'phase5_learning_boost': learning_summary.get('learning_boost', 0),
                'total_latency': self.safe_get_metric(metrics, 'total_latency')
            })
        
        df = pd.DataFrame(comparison_data)
        
        # Phase performance trends
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.line(df, x='timestamp', 
                         y=['phase1_clarity', 'phase2_source_quality', 'phase3_authenticity', 'phase4_engagement'],
                         title="Phase Quality Metrics Over Time")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.scatter(df, x='phase5_learning_boost', y='phase4_engagement',
                           size='phase3_authenticity', hover_data=['query'],
                           title="Learning Boost vs Engagement Potential")
            st.plotly_chart(fig, use_container_width=True)
        
        # Phase performance summary
        st.subheader("📈 Phase Performance Summary")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Avg Query Clarity", f"{df['phase1_clarity'].mean():.2f}")
        with col2:
            st.metric("Avg Source Quality", f"{df['phase2_source_quality'].mean():.2f}")
        with col3:
            st.metric("Avg Authenticity", f"{df['phase3_authenticity'].mean():.2f}")
        with col4:
            st.metric("Avg Engagement", f"{df['phase4_engagement'].mean():.2f}")
        with col5:
            st.metric("Avg Learning Boost", f"{df['phase5_learning_boost'].mean():.3f}")
    
    def render_learning_analytics_view(self):
        """Render learning analytics dashboard"""
        st.header("🧠 Learning Analytics Dashboard")
        
        # Get learning insights
        learning_insights = self.engine.learning_engine.get_learning_insights(30)
        
        if not learning_insights:
            st.info("No learning insights available yet. Process more queries to generate insights.")
            return
        
        # Learning insights overview
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Insights", len(learning_insights))
        with col2:
            avg_impact = np.mean([insight['impact_score'] for insight in learning_insights])
            st.metric("Avg Impact Score", f"{avg_impact:.2f}")
        with col3:
            avg_evidence = np.mean([insight['evidence_strength'] for insight in learning_insights])
            st.metric("Avg Evidence Strength", f"{avg_evidence:.2f}")
        
        # Insights breakdown
        st.subheader("💡 Learning Insights")
        
        for i, insight in enumerate(learning_insights[:5]):
            with st.expander(f"Insight {i+1}: {insight['type'].title()}"):
                st.write(f"**Description:** {insight['description']}")
                st.write(f"**Recommendation:** {insight['recommendation']}")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Impact Score", f"{insight['impact_score']:.2f}")
                with col2:
                    st.metric("Evidence Strength", f"{insight['evidence_strength']:.2f}")
        
        # Learning trends
        if st.session_state.complete_results:
            learning_data = []
            for result in st.session_state.complete_results:
                learning_summary = result['response'].get('learning_summary', {})
                learning_data.append({
                    'timestamp': result['timestamp'],
                    'learning_boost': learning_summary.get('learning_boost', 0),
                    'patterns_applied': learning_summary.get('patterns_applied', 0),
                    'improvement': learning_summary.get('improvement_over_base', 0)
                })
            
            if learning_data:
                learning_df = pd.DataFrame(learning_data)
                
                fig = px.line(learning_df, x='timestamp', y=['learning_boost', 'improvement'],
                             title="Learning Enhancement Over Time")
                st.plotly_chart(fig, use_container_width=True)
    
    def render_performance_tracking_view(self):
        """Render performance tracking dashboard"""
        st.header("🎯 Performance Tracking Dashboard")
        
        # Filter results with performance feedback
        performance_results = [r for r in st.session_state.complete_results if r.get('performance_feedback')]
        
        if not performance_results:
            st.info("No performance data available. Enable 'Simulate Performance' to see tracking.")
            return
        
        # Performance metrics
        performance_data = []
        for result in performance_results:
            feedback = result['performance_feedback']
            learning_summary = result['response'].get('learning_summary', {})
            
            performance_data.append({
                'timestamp': result['timestamp'],
                'query': result['query'][:30] + "...",
                'predicted_engagement': learning_summary.get('max_learning_enhanced_engagement', 0),
                'actual_engagement': feedback['actual_engagement'],
                'prediction_accuracy': 1 - feedback['prediction_accuracy'],
                'performance_tier': feedback['performance_tier']
            })
        
        perf_df = pd.DataFrame(performance_data)
        
        # Performance overview
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Avg Actual Engagement", f"{perf_df['actual_engagement'].mean():.2f}")
        with col2:
            st.metric("Avg Prediction Accuracy", f"{perf_df['prediction_accuracy'].mean():.2f}")
        with col3:
            high_performers = len(perf_df[perf_df['performance_tier'] == 'high'])
            st.metric("High Performers", high_performers)
        with col4:
            st.metric("Total Tracked", len(perf_df))
        
        # Performance visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.scatter(perf_df, x='predicted_engagement', y='actual_engagement',
                           color='performance_tier', hover_data=['query'],
                           title="Predicted vs Actual Engagement")
            # Add perfect prediction line
            fig.add_shape(type="line", x0=0, y0=0, x1=1, y1=1, 
                         line=dict(color="red", dash="dash"))
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.line(perf_df, x='timestamp', y=['predicted_engagement', 'actual_engagement'],
                         title="Engagement Trends Over Time")
            st.plotly_chart(fig, use_container_width=True)
        
        # Performance tier distribution
        tier_counts = perf_df['performance_tier'].value_counts()
        fig = px.pie(values=tier_counts.values, names=tier_counts.index,
                    title="Performance Tier Distribution")
        st.plotly_chart(fig, use_container_width=True)
    
    def run_system_test(self):
        """Run comprehensive system test"""
        test_queries = [
            "AI regulation impact on fintech product strategy",
            "Cross-domain analysis of political tech platforms",
            "Contrarian view on startup funding trends"
        ]
        
        with st.spinner("🧪 Running comprehensive system test..."):
            for query in test_queries:
                try:
                    response, metrics = self.engine.process_query_with_self_improvement(query)
                    
                    # Simulate performance
                    if 'self_improving_content' in response:
                        content_id = response['self_improving_content'].get('performance_tracking_id', 'test')
                        predicted = response.get('learning_summary', {}).get('max_learning_enhanced_engagement', 0.5)
                        performance_feedback = self.engine.simulate_performance_feedback(content_id, 'test', predicted)
                    else:
                        performance_feedback = None
                    
                    # Store result
                    result_data = {
                        'timestamp': datetime.now(),
                        'query': query,
                        'response': response,
                        'metrics': metrics,
                        'processing_time': 2.5,  # Mock
                        'performance_feedback': performance_feedback,
                        'phases_completed': 5
                    }
                    st.session_state.complete_results.append(result_data)
                    
                except Exception as e:
                    st.error(f"Test failed for query '{query}': {e}")
        
        st.success("✅ System test completed!")
        st.rerun()
    
    def generate_sample_data(self):
        """Generate sample data for demonstration"""
        sample_queries = [
            "Product strategy in regulated fintech markets",
            "Engineering leadership in cross-functional teams",
            "Political analysis of tech platform governance",
            "Contrarian view on AI productivity claims",
            "Cross-domain innovation in financial services"
        ]
        
        with st.spinner("📊 Generating sample data..."):
            for query in sample_queries:
                # Mock response data
                mock_response = {
                    'personalized_query_analysis': {
                        'intent': 'comprehensive',
                        'intent_confidence': np.random.uniform(0.7, 0.95),
                        'domains': ['tech', 'finance', 'politics'][:np.random.randint(2, 4)],
                        'complexity': np.random.choice(['cross_domain', 'contrarian']),
                        'personal_frameworks': ['IIT-MBA Framework', 'Cross-Domain Analysis']
                    },
                    'real_sources_fetched': np.random.randint(3, 8),
                    'self_improving_content': {
                        'variants': {'analytical': 'mock', 'engaging': 'mock', 'contrarian': 'mock'},
                        'engagement_predictions': {
                            'analytical': np.random.uniform(0.6, 0.8),
                            'engaging': np.random.uniform(0.65, 0.85),
                            'contrarian': np.random.uniform(0.7, 0.9)
                        },
                        'learning_enhanced_predictions': {
                            'analytical': np.random.uniform(0.65, 0.85),
                            'engaging': np.random.uniform(0.7, 0.9),
                            'contrarian': np.random.uniform(0.75, 0.95)
                        },
                        'performance_tracking_id': f'sample_{len(st.session_state.complete_results)}'
                    },
                    'learning_summary': {
                        'patterns_applied': np.random.randint(0, 4),
                        'learning_boost': np.random.uniform(0, 0.15),
                        'max_learning_enhanced_engagement': np.random.uniform(0.7, 0.95),
                        'improvement_over_base': np.random.uniform(0, 0.1)
                    }
                }
                
                # Mock metrics - create a simple object with attributes
                class MockMetrics:
                    def __init__(self):
                        self.query_clarity = np.random.uniform(0.7, 0.95)
                        self.source_quality_score = np.random.uniform(0.8, 0.95)
                        self.content_authenticity = np.random.uniform(0.85, 1.0)
                        self.engagement_potential = np.random.uniform(0.7, 0.9)
                        self.total_latency = np.random.uniform(2, 8)
                        self.domain_coverage = np.random.randint(2, 4)
                        self.cross_domain_rate = np.random.uniform(0.5, 1.0)
                
                mock_metrics = MockMetrics()
                
                # Mock performance feedback
                predicted = mock_response['learning_summary']['max_learning_enhanced_engagement']
                actual = predicted + np.random.uniform(-0.15, 0.2)
                actual = max(0, min(actual, 1))
                
                performance_feedback = {
                    'actual_engagement': actual,
                    'prediction_accuracy': abs(actual - predicted),
                    'performance_tier': 'high' if actual > 0.7 else 'medium' if actual > 0.4 else 'low'
                }
                
                # Store sample result
                result_data = {
                    'timestamp': datetime.now() - timedelta(days=np.random.randint(0, 7)),
                    'query': query,
                    'response': mock_response,
                    'metrics': mock_metrics,
                    'processing_time': mock_metrics['total_latency'],
                    'performance_feedback': performance_feedback,
                    'phases_completed': 5
                }
                st.session_state.complete_results.append(result_data)
        
        st.success("✅ Sample data generated!")
        st.rerun()
    
    def run(self):
        """Run the complete dashboard"""
        self.render_header()
        
        # Render sidebar
        self.render_sidebar()
        
        st.divider()
        
        # Main content area
        self.render_query_interface()
        
        st.divider()
        
        self.render_complete_results()

def main():
    """Main function"""
    dashboard = ProsoraCompleteDashboard()
    dashboard.run()

if __name__ == "__main__":
    main()