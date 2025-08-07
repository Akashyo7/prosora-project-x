#!/usr/bin/env python3
"""
Enhanced Streamlit Interface for Testing Prosora Intelligence
Phase 1: Smart Query Analysis & Metrics Foundation
"""

import streamlit as st
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from enhanced_unified_intelligence import EnhancedUnifiedProsoraIntelligence
from real_source_fetcher import RealSourceFetcher

# Page config
st.set_page_config(
    page_title="Enhanced Prosora Intelligence",
    page_icon="🧠",
    layout="wide"
)

class EnhancedProsoraInterface:
    def __init__(self):
        if 'engine' not in st.session_state:
            st.session_state.engine = EnhancedUnifiedProsoraIntelligence()
        self.engine = st.session_state.engine
        
        if 'query_results' not in st.session_state:
            st.session_state.query_results = []
    
    def render_header(self):
        """Enhanced header with system status"""
        st.title("🧠 Enhanced Prosora Intelligence Engine")
        st.caption("Phase 1: Smart Query Analysis & Comprehensive Metrics")
        
        # System metrics overview
        col1, col2, col3, col4, col5 = st.columns(5)
        
        system_metrics = self.engine.get_system_metrics(7)
        
        with col1:
            st.metric("AI Status", "✅ Online" if self.engine.ai_available else "⚠️ Offline")
        with col2:
            st.metric("Total Queries", system_metrics.get('total_queries', 0))
        with col3:
            st.metric("Avg Quality", f"{system_metrics.get('avg_source_quality', 0):.2f}")
        with col4:
            st.metric("Avg Latency", f"{system_metrics.get('avg_latency', 0):.2f}s")
        with col5:
            st.metric("AI Tokens Used", system_metrics.get('total_tokens', 0))
    
    def render_query_interface(self):
        """Enhanced query interface"""
        st.header("🔍 Enhanced Intelligence Query")
        
        # Query input with advanced options
        col1, col2 = st.columns([3, 1])
        
        with col1:
            query_text = st.text_input(
                "Enter your intelligence query:",
                placeholder="e.g., AI regulation impact on fintech startups",
                help="The AI will analyze intent, domains, and complexity automatically"
            )
        
        with col2:
            st.write("")
            st.write("")
            analyze_button = st.button("🚀 Analyze with AI", type="primary")
        
        # Advanced options
        with st.expander("🔧 Advanced Options", expanded=False):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                force_intent = st.selectbox(
                    "Force Intent (optional):",
                    ["Auto-detect", "linkedin_post", "twitter_thread", "blog_outline", "analysis", "comprehensive"]
                )
            
            with col2:
                force_complexity = st.selectbox(
                    "Force Complexity (optional):",
                    ["Auto-detect", "simple", "cross_domain", "contrarian"]
                )
            
            with col3:
                enable_metrics = st.checkbox("Detailed Metrics", value=True)
        
        # Example queries with complexity indicators
        st.write("**Example queries by complexity:**")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write("**🟢 Simple:**")
            if st.button("AI in healthcare"):
                query_text = "AI applications in healthcare"
                analyze_button = True
        
        with col2:
            st.write("**🟡 Cross-domain:**")
            if st.button("AI regulation × fintech"):
                query_text = "AI regulation impact on fintech startups"
                analyze_button = True
        
        with col3:
            st.write("**🔴 Contrarian:**")
            if st.button("Contrarian crypto view"):
                query_text = "Contrarian analysis of crypto regulation benefits"
                analyze_button = True
        
        # Process query
        if analyze_button and query_text:
            with st.spinner("🧠 Processing with enhanced AI analysis..."):
                try:
                    response, metrics = self.engine.process_query_with_metrics(query_text)
                    
                    # Store results
                    result_data = {
                        'timestamp': datetime.now(),
                        'query': query_text,
                        'response': response,
                        'metrics': metrics
                    }
                    st.session_state.query_results.append(result_data)
                    
                    st.success("✅ Enhanced analysis complete!")
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Analysis failed: {e}")
    
    def render_results(self):
        """Render enhanced results with metrics"""
        if not st.session_state.query_results:
            st.info("👆 Enter a query above to see enhanced intelligence results")
            return
        
        latest_result = st.session_state.query_results[-1]
        response = latest_result['response']
        metrics = latest_result['metrics']
        
        st.header("📊 Enhanced Intelligence Results")
        
        # Query Analysis Results
        st.subheader("🔍 AI Query Analysis")
        
        if 'query_analysis' in response:
            analysis = response['query_analysis']
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Intent", analysis['intent'])
                st.metric("Confidence", f"{analysis['intent_confidence']:.2f}")
            
            with col2:
                st.metric("Domains Found", len(analysis['domains']))
                st.write("**Domains:**")
                for domain in analysis['domains']:
                    weight = analysis['domain_weights'].get(domain, 0)
                    st.write(f"• {domain.title()}: {weight:.2f}")
            
            with col3:
                st.metric("Complexity", analysis['complexity'])
                st.metric("Evidence Level", analysis['evidence_level'])
            
            with col4:
                st.metric("Keywords", len(analysis['semantic_keywords']))
                st.write("**Context Signals:**")
                for signal, value in analysis['context_signals'].items():
                    st.write(f"• {signal.title()}: {value:.2f}")
        
        # Performance Metrics Dashboard
        st.subheader("⚡ Performance Metrics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Query Clarity", f"{metrics.query_clarity:.2f}")
            st.metric("Domain Coverage", metrics.domain_coverage)
        
        with col2:
            st.metric("Source Quality", f"{metrics.source_quality_score:.2f}")
            st.metric("Evidence Density", f"{metrics.evidence_density:.2f}")
        
        with col3:
            st.metric("Content Authenticity", f"{metrics.content_authenticity:.2f}")
            st.metric("Uniqueness Score", f"{metrics.uniqueness_score:.2f}")
        
        with col4:
            st.metric("Total Latency", f"{metrics.total_latency:.2f}s")
            st.metric("AI Tokens", metrics.ai_tokens_used)
        
        # Metrics Visualization
        col1, col2 = st.columns(2)
        
        with col1:
            # Quality metrics radar chart
            quality_metrics = {
                'Query Clarity': metrics.query_clarity,
                'Source Quality': metrics.source_quality_score,
                'Content Authenticity': metrics.content_authenticity,
                'Evidence Strength': metrics.evidence_strength,
                'Engagement Potential': metrics.engagement_potential,
                'Uniqueness': metrics.uniqueness_score
            }
            
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=list(quality_metrics.values()),
                theta=list(quality_metrics.keys()),
                fill='toself',
                name='Quality Metrics',
                line_color='rgb(0, 123, 255)'
            ))
            
            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
                showlegend=True,
                title="Quality Metrics Profile"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Processing time breakdown
            time_breakdown = {
                'Source Fetch': metrics.source_fetch_time,
                'AI Analysis': max(0, metrics.total_latency - metrics.source_fetch_time - 0.1),
                'Content Generation': 0.1  # Mock
            }
            
            fig = px.pie(
                values=list(time_breakdown.values()),
                names=list(time_breakdown.keys()),
                title="Processing Time Breakdown"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Generated Content
        if 'content' in response:
            st.subheader("📝 Generated Content")
            
            content = response['content']
            
            # Content tabs
            tabs = st.tabs(["LinkedIn Posts", "Insights Summary", "Performance Summary"])
            
            with tabs[0]:
                if content.get('linkedin_posts'):
                    for i, post in enumerate(content['linkedin_posts']):
                        with st.expander(f"LinkedIn Post {i+1} - {post['tier']}"):
                            st.text_area("Content", post['content'], height=200, key=f"post_{i}")
                            
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Credibility", f"{post['credibility_score']:.2f}")
                            with col2:
                                st.metric("Evidence Count", post['evidence_count'])
                            with col3:
                                st.metric("Est. Engagement", post['estimated_engagement'])
                else:
                    st.info("No LinkedIn posts generated for this query")
            
            with tabs[1]:
                insights = content.get('insights_summary', {})
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Insights", insights.get('total_insights', 0))
                with col2:
                    st.metric("Avg Credibility", f"{insights.get('average_credibility', 0):.2f}")
                with col3:
                    st.metric("Cross-Domain", insights.get('cross_domain_insights', 0))
                
                st.write("**Domains Covered:**")
                for domain in insights.get('domains_covered', []):
                    st.write(f"• {domain.title()}")
            
            with tabs[2]:
                if 'performance_summary' in response:
                    perf = response['performance_summary']
                    
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Total Time", perf['total_time'])
                    with col2:
                        st.metric("Quality Score", perf['quality_score'])
                    with col3:
                        st.metric("Authenticity", perf['authenticity'])
                    with col4:
                        st.metric("Uniqueness", perf['uniqueness'])
    
    def render_metrics_history(self):
        """Render metrics history and trends"""
        if len(st.session_state.query_results) < 2:
            return
        
        st.header("📈 Metrics History & Trends")
        
        # Prepare data for visualization
        history_data = []
        for result in st.session_state.query_results[-10:]:  # Last 10 queries
            metrics = result['metrics']
            history_data.append({
                'timestamp': result['timestamp'],
                'query': result['query'][:30] + "...",
                'quality': metrics.source_quality_score,
                'authenticity': metrics.content_authenticity,
                'latency': metrics.total_latency,
                'uniqueness': metrics.uniqueness_score
            })
        
        df = pd.DataFrame(history_data)
        
        # Metrics trends
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.line(df, x='timestamp', y=['quality', 'authenticity', 'uniqueness'],
                         title="Quality Metrics Trends")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.bar(df, x='query', y='latency',
                        title="Processing Time by Query")
            fig.update_xaxis(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
        
        # System performance summary
        st.subheader("🎯 System Performance Summary")
        
        avg_quality = df['quality'].mean()
        avg_latency = df['latency'].mean()
        avg_uniqueness = df['uniqueness'].mean()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Avg Quality Score", f"{avg_quality:.2f}")
        with col2:
            st.metric("Avg Processing Time", f"{avg_latency:.2f}s")
        with col3:
            st.metric("Avg Uniqueness", f"{avg_uniqueness:.2f}")
    
    def run(self):
        """Run the enhanced interface"""
        self.render_header()
        
        st.divider()
        
        self.render_query_interface()
        
        st.divider()
        
        self.render_results()
        
        if len(st.session_state.query_results) >= 2:
            st.divider()
            self.render_metrics_history()

def main():
    """Main function"""
    interface = EnhancedProsoraInterface()
    interface.run()

if __name__ == "__main__":
    main()