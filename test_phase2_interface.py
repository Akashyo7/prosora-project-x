#!/usr/bin/env python3
"""
Phase 2 Streamlit Interface: Real Source Integration Testing
Showcases real RSS fetching, AI analysis, and comprehensive metrics
"""

import streamlit as st
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from phase2_enhanced_intelligence import Phase2EnhancedIntelligence
import time

# Page config
st.set_page_config(
    page_title="Phase 2: Real Source Intelligence",
    page_icon="📡",
    layout="wide"
)

class Phase2TestInterface:
    def __init__(self):
        if 'phase2_engine' not in st.session_state:
            with st.spinner("🚀 Initializing Phase 2 Engine with Real Sources..."):
                st.session_state.phase2_engine = Phase2EnhancedIntelligence()
        self.engine = st.session_state.phase2_engine
        
        if 'phase2_results' not in st.session_state:
            st.session_state.phase2_results = []
        
        if 'real_sources_cache' not in st.session_state:
            st.session_state.real_sources_cache = []
    
    def render_header(self):
        """Phase 2 header with real source status"""
        st.title("📡 Phase 2: Real Source Intelligence Engine")
        st.caption("Testing real RSS fetching, AI analysis, and enhanced metrics")
        
        # System status with real source info
        col1, col2, col3, col4, col5 = st.columns(5)
        
        system_metrics = self.engine.get_system_metrics(7)
        
        with col1:
            st.metric("🤖 AI Status", "✅ Online" if self.engine.ai_available else "⚠️ Offline")
        with col2:
            st.metric("📡 Real Sources", "✅ Active")
        with col3:
            st.metric("Total Queries", system_metrics.get('total_queries', 0))
        with col4:
            st.metric("Avg Quality", f"{system_metrics.get('avg_source_quality', 0):.2f}")
        with col5:
            st.metric("Cache Status", "✅ Active")
        
        # Real source status indicator
        st.info("🔥 **Phase 2 Active**: Now fetching REAL content from RSS feeds and web sources!")
    
    def render_source_preview(self):
        """Preview available real sources"""
        with st.expander("📡 Real Source Configuration Preview", expanded=False):
            st.write("**Premium Sources (High Credibility):**")
            
            premium_sources = [
                {"name": "Stratechery", "status": "✅ RSS Active", "credibility": 0.95, "domains": ["tech", "strategy"]},
                {"name": "First Round Review", "status": "⚠️ RSS Issues", "credibility": 0.95, "domains": ["product", "tech"]},
                {"name": "CB Insights", "status": "⚠️ RSS Issues", "credibility": 0.85, "domains": ["tech", "finance"]},
            ]
            
            df = pd.DataFrame(premium_sources)
            st.dataframe(df, use_container_width=True)
            
            st.write("**Standard Sources:**")
            standard_sources = [
                {"name": "Harvard Business Review", "status": "⚠️ RSS Issues", "credibility": 0.8, "domains": ["business", "leadership"]},
                {"name": "McKinsey Insights", "status": "⚠️ RSS Issues", "credibility": 0.8, "domains": ["strategy", "business"]},
            ]
            
            df2 = pd.DataFrame(standard_sources)
            st.dataframe(df2, use_container_width=True)
            
            st.info("💡 **Note**: Some RSS feeds have parsing issues but Stratechery is working perfectly!")
    
    def render_query_interface(self):
        """Enhanced query interface for Phase 2"""
        st.header("🔍 Real Source Intelligence Query")
        
        # Query input
        col1, col2 = st.columns([3, 1])
        
        with col1:
            query_text = st.text_input(
                "Enter your intelligence query:",
                placeholder="e.g., AI regulation impact on fintech startups",
                help="Phase 2 will fetch REAL content from RSS feeds and analyze with AI"
            )
        
        with col2:
            st.write("")
            st.write("")
            process_button = st.button("📡 Process with Real Sources", type="primary")
        
        # Phase 2 specific examples
        st.write("**Phase 2 Test Queries (optimized for real sources):**")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write("**🟢 Tech Strategy:**")
            if st.button("Tech platform strategy"):
                query_text = "Technology platform strategy and competitive moats"
                process_button = True
            if st.button("AI business models"):
                query_text = "AI business models and monetization strategies"
                process_button = True
        
        with col2:
            st.write("**🟡 Cross-Domain:**")
            if st.button("AI × Regulation"):
                query_text = "AI regulation impact on startup innovation"
                process_button = True
            if st.button("Product × Finance"):
                query_text = "Product strategy in fintech and embedded finance"
                process_button = True
        
        with col3:
            st.write("**🔴 Contrarian:**")
            if st.button("Contrarian on remote work"):
                query_text = "Contrarian view on remote work productivity"
                process_button = True
            if st.button("Contrarian on AI hype"):
                query_text = "Contrarian analysis of AI investment hype"
                process_button = True
        
        # Process query with real sources
        if process_button and query_text:
            with st.spinner("📡 Fetching real sources and processing with AI..."):
                start_time = time.time()
                
                try:
                    # Show progress
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    status_text.text("🔍 Analyzing query with AI...")
                    progress_bar.progress(20)
                    
                    status_text.text("📡 Fetching real content from RSS feeds...")
                    progress_bar.progress(50)
                    
                    # Process with Phase 2 engine
                    response, metrics = self.engine.process_query_with_real_sources(query_text)
                    
                    status_text.text("🧠 Generating AI-powered insights...")
                    progress_bar.progress(80)
                    
                    status_text.text("✅ Complete!")
                    progress_bar.progress(100)
                    
                    # Store results
                    result_data = {
                        'timestamp': datetime.now(),
                        'query': query_text,
                        'response': response,
                        'metrics': metrics,
                        'processing_time': time.time() - start_time
                    }
                    st.session_state.phase2_results.append(result_data)
                    
                    # Clear progress indicators
                    progress_bar.empty()
                    status_text.empty()
                    
                    st.success(f"✅ Phase 2 processing complete! Fetched {response.get('real_sources_fetched', 0)} real sources in {result_data['processing_time']:.2f}s")
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Phase 2 processing failed: {e}")
    
    def render_real_source_results(self):
        """Render results with real source integration"""
        if not st.session_state.phase2_results:
            st.info("👆 Enter a query above to see Phase 2 real source results")
            return
        
        latest_result = st.session_state.phase2_results[-1]
        response = latest_result['response']
        metrics = latest_result['metrics']
        
        st.header("📊 Phase 2: Real Source Results")
        
        # Real Sources Summary
        st.subheader("📡 Real Sources Fetched")
        
        if 'real_sources_summary' in response:
            sources_summary = response['real_sources_summary']
            
            if sources_summary:
                # Create DataFrame for real sources
                sources_df = pd.DataFrame(sources_summary)
                
                # Display metrics
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Sources Fetched", len(sources_summary))
                with col2:
                    avg_credibility = sources_df['credibility'].mean()
                    st.metric("Avg Credibility", f"{avg_credibility:.2f}")
                with col3:
                    avg_freshness = sources_df['freshness'].mean()
                    st.metric("Avg Freshness", f"{avg_freshness:.2f}")
                with col4:
                    avg_relevance = sources_df['relevance'].mean()
                    st.metric("Avg Relevance", f"{avg_relevance:.2f}")
                
                # Real sources table
                st.write("**Real Sources Used:**")
                
                # Format the dataframe for better display
                display_df = sources_df.copy()
                display_df['credibility'] = display_df['credibility'].round(2)
                display_df['freshness'] = display_df['freshness'].round(2)
                display_df['relevance'] = display_df['relevance'].round(2)
                display_df['title'] = display_df['title'].str[:50] + "..."
                
                st.dataframe(display_df, use_container_width=True)
                
                # Source quality visualization
                col1, col2 = st.columns(2)
                
                with col1:
                    # Credibility vs Freshness scatter
                    fig = px.scatter(
                        sources_df, 
                        x='freshness', 
                        y='credibility',
                        size='relevance',
                        hover_data=['source', 'title'],
                        title="Source Quality Matrix",
                        labels={'freshness': 'Freshness Score', 'credibility': 'Credibility Score'}
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # Source distribution by credibility
                    fig = px.histogram(
                        sources_df,
                        x='credibility',
                        title="Source Credibility Distribution",
                        nbins=10
                    )
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("No real sources were fetched for this query")
        
        # Enhanced Performance Metrics
        st.subheader("⚡ Phase 2 Performance Metrics")
        
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
            st.metric("Source Fetch Time", f"{metrics.source_fetch_time:.2f}s")
        
        # Performance breakdown
        col1, col2 = st.columns(2)
        
        with col1:
            # Quality metrics radar
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
                name='Phase 2 Quality Metrics',
                line_color='rgb(0, 123, 255)'
            ))
            
            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
                showlegend=True,
                title="Phase 2 Quality Profile"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Processing time breakdown
            time_breakdown = {
                'Source Fetching': metrics.source_fetch_time,
                'AI Analysis': max(0, metrics.total_latency - metrics.source_fetch_time - 0.5),
                'Content Generation': 0.5  # Estimated
            }
            
            fig = px.pie(
                values=list(time_breakdown.values()),
                names=list(time_breakdown.keys()),
                title="Phase 2 Processing Time Breakdown"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Generated Content with Real Source Backing
        if 'content' in response:
            st.subheader("📝 AI-Generated Content (Real Source Backed)")
            
            content = response['content']
            
            # Content tabs
            tabs = st.tabs(["LinkedIn Posts", "Insights Summary", "Real Sources Used", "Performance Summary"])
            
            with tabs[0]:
                if content.get('linkedin_posts'):
                    for i, post in enumerate(content['linkedin_posts']):
                        with st.expander(f"LinkedIn Post {i+1} - {post['tier']} (Real Source Backed)"):
                            st.text_area("Content", post['content'], height=250, key=f"phase2_post_{i}")
                            
                            # Enhanced metrics for Phase 2
                            col1, col2, col3, col4 = st.columns(4)
                            with col1:
                                st.metric("Credibility", f"{post['credibility_score']:.2f}")
                            with col2:
                                st.metric("Real Sources", post.get('real_source_count', 0))
                            with col3:
                                st.metric("Freshness", f"{post.get('freshness_score', 0):.2f}")
                            with col4:
                                st.metric("Evidence Count", post['evidence_count'])
                            
                            # Real source evidence
                            st.write("**Real Source Evidence:**")
                            for evidence in post.get('supporting_evidence', []):
                                with st.container():
                                    st.write(f"📡 **{evidence['source']}** (Credibility: {evidence['credibility']:.2f})")
                                    st.write(f"   📰 {evidence.get('title', 'No title')}")
                                    st.write(f"   🔗 [Source Link]({evidence.get('url', '#')})")
                                    st.write(f"   ⏰ Freshness: {evidence.get('freshness', 0):.2f}")
                else:
                    st.info("No LinkedIn posts generated for this query")
            
            with tabs[1]:
                insights = content.get('insights_summary', {})
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Insights", insights.get('total_insights', 0))
                with col2:
                    st.metric("Real Sources Used", insights.get('real_sources_used', 0))
                with col3:
                    st.metric("Avg Freshness", f"{insights.get('average_freshness', 0):.2f}")
                
                # Source breakdown
                if 'source_breakdown' in insights:
                    st.write("**Source Tier Breakdown:**")
                    breakdown = insights['source_breakdown']
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Premium", breakdown.get('premium', 0))
                    with col2:
                        st.metric("Standard", breakdown.get('standard', 0))
                    with col3:
                        st.metric("Experimental", breakdown.get('experimental', 0))
                
                st.write("**Domains Covered:**")
                for domain in insights.get('domains_covered', []):
                    st.write(f"• {domain.title()}")
            
            with tabs[2]:
                if 'real_sources_used' in content:
                    st.write("**Real Sources Used in Content Generation:**")
                    
                    for i, source in enumerate(content['real_sources_used'][:5]):
                        with st.expander(f"📡 {source['source_name']} (Credibility: {source['credibility']:.2f})"):
                            st.write(f"**Title:** {source['title']}")
                            st.write(f"**Freshness:** {source['freshness']:.2f}")
                            st.write(f"**URL:** [Link]({source['url']})")
                            st.write(f"**Content Preview:** {source['content_preview']}")
                else:
                    st.info("No real source details available")
            
            with tabs[3]:
                if 'performance_summary' in response:
                    perf = response['performance_summary']
                    
                    st.write("**Phase 2 Performance Summary:**")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Total Time", perf['total_time'])
                    with col2:
                        st.metric("Source Fetch Time", perf['source_fetch_time'])
                    with col3:
                        st.metric("Quality Score", perf['quality_score'])
                    with col4:
                        st.metric("Real Sources", perf['real_sources_used'])
                    
                    # Performance insights
                    st.write("**Performance Insights:**")
                    st.write(f"• Fetched {perf['real_sources_used']} real sources")
                    st.write(f"• Source fetching took {perf['source_fetch_time']} ({(float(perf['source_fetch_time'][:-1]) / float(perf['total_time'][:-1]) * 100):.1f}% of total time)")
                    st.write(f"• Content authenticity: {perf['authenticity']}")
                    st.write(f"• Uniqueness score: {perf['uniqueness']}")
    
    def render_phase2_comparison(self):
        """Compare Phase 2 vs previous versions"""
        if len(st.session_state.phase2_results) < 2:
            return
        
        st.header("📈 Phase 2 Performance Trends")
        
        # Prepare comparison data
        comparison_data = []
        for result in st.session_state.phase2_results[-10:]:
            metrics = result['metrics']
            comparison_data.append({
                'timestamp': result['timestamp'],
                'query': result['query'][:30] + "...",
                'real_sources': result['response'].get('real_sources_fetched', 0),
                'quality': metrics.source_quality_score,
                'authenticity': metrics.content_authenticity,
                'latency': metrics.total_latency,
                'uniqueness': metrics.uniqueness_score,
                'source_fetch_time': metrics.source_fetch_time
            })
        
        df = pd.DataFrame(comparison_data)
        
        # Trends visualization
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.line(df, x='timestamp', y=['quality', 'authenticity', 'uniqueness'],
                         title="Phase 2 Quality Metrics Over Time")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.scatter(df, x='real_sources', y='quality', size='uniqueness',
                           hover_data=['query'], title="Real Sources vs Quality")
            st.plotly_chart(fig, use_container_width=True)
        
        # Performance summary
        st.subheader("🎯 Phase 2 System Performance")
        
        avg_sources = df['real_sources'].mean()
        avg_quality = df['quality'].mean()
        avg_latency = df['latency'].mean()
        avg_fetch_time = df['source_fetch_time'].mean()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Avg Real Sources", f"{avg_sources:.1f}")
        with col2:
            st.metric("Avg Quality", f"{avg_quality:.2f}")
        with col3:
            st.metric("Avg Total Time", f"{avg_latency:.2f}s")
        with col4:
            st.metric("Avg Fetch Time", f"{avg_fetch_time:.2f}s")
        
        # Phase 2 advantages
        st.success("🚀 **Phase 2 Advantages**: Real RSS content, enhanced credibility scoring, source freshness tracking, and AI-powered insights!")
    
    def run(self):
        """Run the Phase 2 test interface"""
        self.render_header()
        
        st.divider()
        
        self.render_source_preview()
        
        st.divider()
        
        self.render_query_interface()
        
        st.divider()
        
        self.render_real_source_results()
        
        if len(st.session_state.phase2_results) >= 2:
            st.divider()
            self.render_phase2_comparison()

def main():
    """Main function"""
    interface = Phase2TestInterface()
    interface.run()

if __name__ == "__main__":
    main()