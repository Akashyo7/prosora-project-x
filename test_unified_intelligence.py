#!/usr/bin/env python3
"""
Streamlit Interface for Testing Unified Prosora Intelligence
"""

import streamlit as st
import json
from datetime import datetime
from unified_prosora_intelligence import UnifiedProsoraIntelligence
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Page config
st.set_page_config(
    page_title="Unified Prosora Intelligence Test",
    page_icon="🧠",
    layout="wide"
)

class UnifiedProsoraTestInterface:
    def __init__(self):
        self.engine = UnifiedProsoraIntelligence()
        self.setup_session_state()
    
    def setup_session_state(self):
        """Initialize session state"""
        if 'results' not in st.session_state:
            st.session_state.results = None
        if 'query_history' not in st.session_state:
            st.session_state.query_history = []
    
    def render_header(self):
        """Render header"""
        st.title("🧠 Unified Prosora Intelligence Engine")
        st.caption("Test the complete intelligence pipeline with your curated sources")
        
        # System status
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("AI Status", "✅ Online" if self.engine.ai_available else "⚠️ Offline")
        with col2:
            st.metric("Sources Config", "✅ Loaded")
        with col3:
            st.metric("Expertise Domains", len(self.engine.expertise_domains))
        with col4:
            st.metric("Query History", len(st.session_state.query_history))
    
    def render_query_interface(self):
        """Render query input interface"""
        st.header("🔍 Intelligence Query")
        
        # Query input
        col1, col2 = st.columns([3, 1])
        
        with col1:
            query_text = st.text_input(
                "Enter your intelligence query:",
                placeholder="e.g., AI regulation in fintech, Cross-domain analysis of blockchain governance",
                help="Ask about any topic across tech, politics, product, or finance domains"
            )
        
        with col2:
            st.write("") # Spacing
            st.write("") # Spacing
            process_button = st.button("🚀 Process Query", type="primary")
        
        # Example queries
        st.write("**Example queries:**")
        example_queries = [
            "AI regulation impact on fintech startups",
            "Cross-domain analysis of blockchain governance",
            "Product strategy for political tech platforms",
            "Contrarian view on crypto regulation"
        ]
        
        cols = st.columns(len(example_queries))
        for i, example in enumerate(example_queries):
            with cols[i]:
                if st.button(f"📝 {example}", key=f"example_{i}"):
                    query_text = example
                    process_button = True
        
        # Process query
        if process_button and query_text:
            with st.spinner("🧠 Processing with Prosora Intelligence..."):
                try:
                    results = self.engine.process_query(query_text)
                    st.session_state.results = results
                    st.session_state.query_history.append({
                        'query': query_text,
                        'timestamp': datetime.now().isoformat(),
                        'results_summary': {
                            'linkedin_posts': len(results.linkedin_posts),
                            'twitter_threads': len(results.twitter_threads),
                            'blog_outlines': len(results.blog_outlines),
                            'credibility_score': results.generation_metadata['credibility_score']
                        }
                    })
                    st.success("✅ Intelligence processing complete!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Processing failed: {e}")
    
    def render_results(self):
        """Render processing results"""
        if not st.session_state.results:
            st.info("👆 Enter a query above to see intelligence results")
            return
        
        results = st.session_state.results
        
        st.header("📊 Intelligence Results")
        
        # Results overview
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("LinkedIn Posts", len(results.linkedin_posts))
        with col2:
            st.metric("Twitter Threads", len(results.twitter_threads))
        with col3:
            st.metric("Blog Outlines", len(results.blog_outlines))
        with col4:
            st.metric("Evidence Sources", results.evidence_report['total_sources'])
        
        # Credibility and evidence analysis
        st.subheader("🎯 Evidence Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Credibility score
            credibility = results.generation_metadata['credibility_score']
            fig = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = credibility * 100,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Credibility Score"},
                delta = {'reference': 70},
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 50], 'color': "lightgray"},
                        {'range': [50, 80], 'color': "gray"},
                        {'range': [80, 100], 'color': "lightgreen"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            ))
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Source tier distribution
            evidence = results.evidence_report
            tier_data = {
                'Tier': ['Premium', 'Standard', 'Experimental'],
                'Count': [
                    evidence['premium_sources'],
                    evidence['standard_sources'],
                    evidence['experimental_sources']
                ]
            }
            
            fig = px.pie(
                values=tier_data['Count'],
                names=tier_data['Tier'],
                title="Source Tier Distribution",
                color_discrete_map={
                    'Premium': '#1f77b4',
                    'Standard': '#ff7f0e',
                    'Experimental': '#2ca02c'
                }
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Insights summary
        st.subheader("💡 Insights Summary")
        insights = results.insights_summary
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Insights", insights['total_insights'])
        with col2:
            st.metric("Domains Covered", len(insights['domains_covered']))
        with col3:
            st.metric("Frameworks Applied", len(insights['frameworks_applied']))
        
        # Domain and framework breakdown
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Domains Analyzed:**")
            for domain in insights['domains_covered']:
                st.write(f"• {domain.title()}")
        
        with col2:
            st.write("**Frameworks Applied:**")
            for framework in insights['frameworks_applied'][:5]:
                st.write(f"• {framework}")
        
        # Generated content tabs
        st.subheader("📝 Generated Content")
        
        content_tabs = st.tabs(["LinkedIn Posts", "Twitter Threads", "Blog Outlines", "Evidence Report"])
        
        with content_tabs[0]:  # LinkedIn Posts
            if results.linkedin_posts:
                for i, post in enumerate(results.linkedin_posts):
                    with st.expander(f"LinkedIn Post {i+1} - {post['tier']}"):
                        st.text_area("Content", post['content'], height=200, key=f"linkedin_{i}")
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Credibility", f"{post['credibility_score']:.2f}")
                        with col2:
                            st.metric("Evidence Count", post['evidence_count'])
                        with col3:
                            st.metric("Domains", len(post['domains']))
                        
                        # Supporting evidence
                        st.write("**Supporting Evidence:**")
                        for evidence in post['supporting_evidence']:
                            st.write(f"• {evidence['source']} (Credibility: {evidence['credibility']:.2f})")
                        
                        # Frameworks
                        st.write("**Frameworks:**")
                        for framework in post['frameworks']:
                            st.write(f"• {framework}")
            else:
                st.info("No LinkedIn posts generated for this query")
        
        with content_tabs[1]:  # Twitter Threads
            if results.twitter_threads:
                for i, thread in enumerate(results.twitter_threads):
                    with st.expander(f"Twitter Thread {i+1} - {thread['tier']}"):
                        st.write("**Thread:**")
                        for j, tweet in enumerate(thread['tweets']):
                            st.write(f"{j+1}. {tweet}")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Credibility", f"{thread['credibility_score']:.2f}")
                        with col2:
                            st.metric("Estimated Reach", thread['estimated_reach'])
                        
                        st.write("**Evidence Sources:**")
                        for source in thread['evidence_sources']:
                            st.write(f"• {source}")
            else:
                st.info("No Twitter threads generated for this query")
        
        with content_tabs[2]:  # Blog Outlines
            if results.blog_outlines:
                for i, blog in enumerate(results.blog_outlines):
                    with st.expander(f"Blog Outline {i+1} - {blog['tier']}"):
                        st.text_area("Outline", blog['outline'], height=400, key=f"blog_{i}")
                        
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("Word Count", blog['word_count'])
                        with col2:
                            st.metric("Read Time", blog['read_time'])
                        with col3:
                            st.metric("Evidence Sources", blog['evidence_sources'])
                        with col4:
                            st.metric("Credibility", f"{blog['credibility_score']:.2f}")
            else:
                st.info("No blog outlines generated for this query")
        
        with content_tabs[3]:  # Evidence Report
            st.write("**Evidence Summary:**")
            evidence = results.evidence_report
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Sources", evidence['total_sources'])
            with col2:
                st.metric("Average Credibility", f"{evidence['average_credibility']:.2f}")
            with col3:
                st.metric("Premium Sources", evidence['premium_sources'])
            
            # Source details
            st.write("**Source Details:**")
            source_df = pd.DataFrame(evidence['source_details'])
            if not source_df.empty:
                st.dataframe(source_df, use_container_width=True)
    
    def render_query_history(self):
        """Render query history"""
        if st.session_state.query_history:
            st.header("📚 Query History")
            
            for i, query_data in enumerate(reversed(st.session_state.query_history[-5:])):
                with st.expander(f"Query {len(st.session_state.query_history)-i}: {query_data['query'][:50]}..."):
                    st.write(f"**Query:** {query_data['query']}")
                    st.write(f"**Timestamp:** {query_data['timestamp']}")
                    
                    summary = query_data['results_summary']
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("LinkedIn", summary['linkedin_posts'])
                    with col2:
                        st.metric("Twitter", summary['twitter_threads'])
                    with col3:
                        st.metric("Blog", summary['blog_outlines'])
                    with col4:
                        st.metric("Credibility", f"{summary['credibility_score']:.2f}")
    
    def run(self):
        """Run the Streamlit interface"""
        self.render_header()
        
        st.divider()
        
        self.render_query_interface()
        
        st.divider()
        
        self.render_results()
        
        if st.session_state.query_history:
            st.divider()
            self.render_query_history()

def main():
    """Main function"""
    interface = UnifiedProsoraTestInterface()
    interface.run()

if __name__ == "__main__":
    main()