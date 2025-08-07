#!/usr/bin/env python3
"""
Phase 3 Streamlit Interface: Personalized Intelligence Testing
Showcases voice personalization, personal frameworks, and AI-powered content generation
"""

import streamlit as st
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from phase3_personalized_intelligence import Phase3PersonalizedIntelligence
import time

# Page config
st.set_page_config(
    page_title="Phase 3: Personalized Intelligence",
    page_icon="🎯",
    layout="wide"
)

class Phase3TestInterface:
    def __init__(self):
        if 'phase3_engine' not in st.session_state:
            with st.spinner("🎯 Initializing Phase 3 Personalized Intelligence Engine..."):
                st.session_state.phase3_engine = Phase3PersonalizedIntelligence()
        self.engine = st.session_state.phase3_engine
        
        if 'phase3_results' not in st.session_state:
            st.session_state.phase3_results = []
    
    def render_header(self):
        """Phase 3 header with personalization status"""
        st.title("🎯 Phase 3: Personalized Intelligence Engine")
        st.caption("AI-powered voice personalization with Akash's frameworks and expertise")
        
        # System status with personalization info
        col1, col2, col3, col4, col5 = st.columns(5)
        
        system_metrics = self.engine.get_system_metrics(7)
        
        with col1:
            st.metric("🤖 AI Status", "✅ Online" if self.engine.ai_available else "⚠️ Offline")
        with col2:
            st.metric("🎯 Personalization", "✅ Active")
        with col3:
            st.metric("📡 Real Sources", "✅ Active")
        with col4:
            st.metric("Total Queries", system_metrics.get('total_queries', 0))
        with col5:
            st.metric("Avg Authenticity", f"{system_metrics.get('avg_authenticity', 0):.2f}")
        
        # Phase 3 features highlight
        st.success("🔥 **Phase 3 Active**: Personalized content with YOUR voice, frameworks, and cross-domain expertise!")
    
    def render_personalization_preview(self):
        """Preview Akash's personalization profile"""
        with st.expander("🎯 Akash's Personalization Profile", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Background & Expertise:**")
                st.write("• IIT Bombay engineer with technical depth")
                st.write("• Political consultant with policy expertise")
                st.write("• Product ops lead with scaling experience")
                st.write("• FinTech MBA student with financial knowledge")
                
                st.write("**Thinking Style:**")
                st.write("• Analytical and data-driven")
                st.write("• Cross-domain synthesis")
                st.write("• Contrarian when appropriate")
                st.write("• Framework-oriented approach")
            
            with col2:
                st.write("**Personal Frameworks:**")
                frameworks = {
                    "IIT-MBA Technical Leadership": "Engineering + Business Strategy",
                    "Political Product Management": "Product in Regulated Environments", 
                    "Fintech Regulatory Navigation": "Financial Products + Compliance",
                    "Cross-Domain Innovation": "Finding Intersections"
                }
                
                for framework, description in frameworks.items():
                    st.write(f"• **{framework}**: {description}")
                
                st.write("**Voice Elements:**")
                st.write("• Professional but engaging")
                st.write("• Framework introductions")
                st.write("• Cross-domain connections")
                st.write("• Contrarian insights")
    
    def render_query_interface(self):
        """Enhanced query interface for Phase 3"""
        st.header("🎯 Personalized Intelligence Query")
        
        # Query input
        col1, col2 = st.columns([3, 1])
        
        with col1:
            query_text = st.text_input(
                "Enter your intelligence query:",
                placeholder="e.g., AI regulation impact on fintech product strategy",
                help="Phase 3 will personalize content with YOUR voice and frameworks"
            )
        
        with col2:
            st.write("")
            st.write("")
            process_button = st.button("🎯 Generate Personalized Content", type="primary")
        
        # Personalization options
        with st.expander("🔧 Personalization Options", expanded=False):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                voice_style = st.selectbox(
                    "Voice Style:",
                    ["Auto-detect", "analytical_cross_domain", "professional", "contrarian_analytical"]
                )
            
            with col2:
                force_frameworks = st.multiselect(
                    "Force Specific Frameworks:",
                    ["IIT-MBA Technical Leadership", "Political Product Management", 
                     "Fintech Regulatory Navigation", "Cross-Domain Innovation"]
                )
            
            with col3:
                contrarian_level = st.slider("Contrarian Level", 0.0, 1.0, 0.5, 0.1)
        
        # Phase 3 specific examples
        st.write("**Phase 3 Personalized Test Queries:**")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write("**🟢 Cross-Domain Analysis:**")
            if st.button("Tech × Policy Strategy"):
                query_text = "Technology platform strategy in regulated environments"
                process_button = True
            if st.button("Product × Finance Innovation"):
                query_text = "Product innovation in fintech and embedded finance"
                process_button = True
        
        with col2:
            st.write("**🟡 Framework-Driven:**")
            if st.button("IIT-MBA Perspective"):
                query_text = "Engineering leadership in product management"
                process_button = True
            if st.button("Political Product View"):
                query_text = "Building products in politically sensitive markets"
                process_button = True
        
        with col3:
            st.write("**🔴 Contrarian Analysis:**")
            if st.button("Contrarian on AI Hype"):
                query_text = "Contrarian analysis of AI investment and productivity claims"
                process_button = True
            if st.button("Contrarian on Remote Work"):
                query_text = "Contrarian view on remote work effectiveness in startups"
                process_button = True
        
        # Process query with personalization
        if process_button and query_text:
            with st.spinner("🎯 Generating personalized content with your voice and frameworks..."):
                start_time = time.time()
                
                try:
                    # Show progress
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    status_text.text("🔍 Analyzing query with personalization...")
                    progress_bar.progress(20)
                    
                    status_text.text("📡 Fetching real sources...")
                    progress_bar.progress(40)
                    
                    status_text.text("🎯 Applying personal frameworks...")
                    progress_bar.progress(60)
                    
                    status_text.text("✍️ Generating content in your voice...")
                    progress_bar.progress(80)
                    
                    # Process with Phase 3 engine
                    response, metrics = self.engine.process_query_with_personalization(query_text)
                    
                    status_text.text("✅ Personalization complete!")
                    progress_bar.progress(100)
                    
                    # Store results
                    result_data = {
                        'timestamp': datetime.now(),
                        'query': query_text,
                        'response': response,
                        'metrics': metrics,
                        'processing_time': time.time() - start_time
                    }
                    st.session_state.phase3_results.append(result_data)
                    
                    # Clear progress indicators
                    progress_bar.empty()
                    status_text.empty()
                    
                    frameworks_count = len(response.get('personalized_query_analysis', {}).get('personal_frameworks', []))
                    st.success(f"✅ Phase 3 complete! Applied {frameworks_count} personal frameworks with {metrics.content_authenticity:.2f} authenticity in {result_data['processing_time']:.2f}s")
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Phase 3 processing failed: {e}")
    
    def render_personalized_results(self):
        """Render results with personalization details"""
        if not st.session_state.phase3_results:
            st.info("👆 Enter a query above to see Phase 3 personalized results")
            return
        
        latest_result = st.session_state.phase3_results[-1]
        response = latest_result['response']
        metrics = latest_result['metrics']
        
        st.header("🎯 Phase 3: Personalized Results")
        
        # Personalization Analysis
        if 'personalized_query_analysis' in response:
            st.subheader("🔍 Personalized Query Analysis")
            
            analysis = response['personalized_query_analysis']
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Intent", analysis['intent'])
                st.metric("Confidence", f"{analysis['intent_confidence']:.2f}")
            
            with col2:
                st.metric("Domains", len(analysis['domains']))
                st.write("**Domains:**")
                for domain in analysis['domains']:
                    weight = analysis['domain_weights'].get(domain, 0)
                    st.write(f"• {domain}: {weight:.2f}")
            
            with col3:
                st.metric("Complexity", analysis['complexity'])
                st.metric("Voice Style", analysis['voice_style'])
            
            with col4:
                st.metric("Frameworks", len(analysis['personal_frameworks']))
                st.metric("Contrarian Potential", f"{analysis['contrarian_potential']:.2f}")
            
            # Personal Frameworks Applied
            if analysis['personal_frameworks']:
                st.write("**🎯 Personal Frameworks Applied:**")
                for framework in analysis['personal_frameworks']:
                    st.write(f"• {framework}")
        
        # Voice Personalization Summary
        if 'voice_personalization' in response:
            st.subheader("🎯 Voice Personalization Summary")
            
            voice_data = response['voice_personalization']
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Frameworks Applied", len(voice_data['frameworks_applied']))
            with col2:
                st.metric("Voice Style", voice_data['voice_style'])
            with col3:
                st.metric("Contrarian Potential", f"{voice_data['contrarian_potential']:.2f}")
            with col4:
                st.metric("Authenticity Score", f"{voice_data['authenticity_score']:.2f}")
        
        # Enhanced Performance Metrics
        st.subheader("⚡ Phase 3 Performance Metrics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Query Clarity", f"{metrics.query_clarity:.2f}")
            st.metric("Domain Coverage", metrics.domain_coverage)
        
        with col2:
            st.metric("Content Authenticity", f"{metrics.content_authenticity:.2f}")
            st.metric("Uniqueness Score", f"{metrics.uniqueness_score:.2f}")
        
        with col3:
            st.metric("Engagement Potential", f"{metrics.engagement_potential:.2f}")
            st.metric("Evidence Strength", f"{metrics.evidence_strength:.2f}")
        
        with col4:
            st.metric("Total Latency", f"{metrics.total_latency:.2f}s")
            st.metric("Cross-Domain Rate", f"{metrics.cross_domain_rate:.2f}")
        
        # Personalization Quality Visualization
        col1, col2 = st.columns(2)
        
        with col1:
            # Personalization metrics radar
            personalization_metrics = {
                'Content Authenticity': metrics.content_authenticity,
                'Uniqueness Score': metrics.uniqueness_score,
                'Engagement Potential': metrics.engagement_potential,
                'Query Clarity': metrics.query_clarity,
                'Evidence Strength': metrics.evidence_strength,
                'Cross-Domain Rate': metrics.cross_domain_rate
            }
            
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=list(personalization_metrics.values()),
                theta=list(personalization_metrics.keys()),
                fill='toself',
                name='Phase 3 Personalization',
                line_color='rgb(255, 0, 128)'
            ))
            
            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
                showlegend=True,
                title="Phase 3 Personalization Quality"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Framework application breakdown
            if 'personalized_query_analysis' in response:
                frameworks = response['personalized_query_analysis']['personal_frameworks']
                if frameworks:
                    framework_data = pd.DataFrame({
                        'Framework': frameworks,
                        'Applied': [1] * len(frameworks)
                    })
                    
                    fig = px.bar(
                        framework_data,
                        x='Applied',
                        y='Framework',
                        orientation='h',
                        title="Personal Frameworks Applied"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No personal frameworks applied")
        
        # Personalized Content Generation
        if 'personalized_content' in response:
            st.subheader("✍️ Personalized Content (Your Voice)")
            
            content = response['personalized_content']
            
            # Content tabs
            tabs = st.tabs(["LinkedIn Posts", "Personalization Summary", "Voice Analysis", "Performance"])
            
            with tabs[0]:
                if content.get('linkedin_posts'):
                    for i, post in enumerate(content['linkedin_posts']):
                        with st.expander(f"LinkedIn Post {i+1} - {post['tier']} (Personalized)"):
                            st.text_area("Personalized Content", post['content'], height=300, key=f"phase3_post_{i}")
                            
                            # Enhanced personalization metrics
                            col1, col2, col3, col4 = st.columns(4)
                            with col1:
                                st.metric("Authenticity", f"{post.get('authenticity_score', 0):.2f}")
                            with col2:
                                st.metric("Frameworks Used", len(post.get('personal_frameworks', [])))
                            with col3:
                                st.metric("Voice Elements", len(post.get('voice_elements', [])))
                            with col4:
                                st.metric("Credibility", f"{post['credibility_score']:.2f}")
                            
                            # Personal frameworks used
                            if post.get('personal_frameworks'):
                                st.write("**🎯 Personal Frameworks Used:**")
                                for framework in post['personal_frameworks']:
                                    st.write(f"• {framework}")
                            
                            # Voice elements
                            if post.get('voice_elements'):
                                st.write("**🗣️ Voice Elements:**")
                                for element in post['voice_elements']:
                                    st.write(f"• {element.replace('_', ' ').title()}")
                            
                            # Evidence backing
                            if post.get('supporting_evidence'):
                                st.write("**📡 Evidence Sources:**")
                                for evidence in post['supporting_evidence']:
                                    st.write(f"• {evidence['source']} (Credibility: {evidence['credibility']:.2f})")
                else:
                    st.info("No personalized LinkedIn posts generated")
            
            with tabs[1]:
                personalization = content.get('personalization_summary', {})
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Frameworks Applied", len(personalization.get('frameworks_applied', [])))
                with col2:
                    st.metric("Voice Style", personalization.get('voice_style', 'N/A'))
                with col3:
                    st.metric("Contrarian Elements", personalization.get('contrarian_elements', 0))
                
                # Authenticity indicators
                st.write("**✅ Authenticity Indicators:**")
                for indicator in personalization.get('authenticity_indicators', []):
                    st.write(f"• {indicator.replace('_', ' ').title()}")
                
                # Cross-domain connections
                if personalization.get('cross_domain_connections', 0) > 0:
                    st.write(f"**🔗 Cross-Domain Connections:** {personalization['cross_domain_connections']}")
            
            with tabs[2]:
                st.write("**🗣️ Voice Analysis:**")
                
                if 'personalized_query_analysis' in response:
                    analysis = response['personalized_query_analysis']
                    
                    st.write(f"**Voice Style:** {analysis['voice_style']}")
                    st.write(f"**Contrarian Potential:** {analysis['contrarian_potential']:.2f}")
                    
                    # Domain expertise mapping
                    st.write("**Domain Expertise Applied:**")
                    for domain, weight in analysis['domain_weights'].items():
                        expertise_map = {
                            'tech': 'IIT Bombay Engineering Background',
                            'politics': 'Political Consulting Experience',
                            'product': 'Product Ops Leadership',
                            'finance': 'FinTech MBA Knowledge'
                        }
                        expertise = expertise_map.get(domain, f'{domain.title()} Expertise')
                        st.write(f"• {expertise}: {weight:.2f}")
            
            with tabs[3]:
                if 'performance_summary' in response:
                    perf = response['performance_summary']
                    
                    st.write("**🎯 Phase 3 Performance Summary:**")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Total Time", perf['total_time'])
                    with col2:
                        st.metric("Personalization Quality", perf['personalization_quality'])
                    with col3:
                        st.metric("Uniqueness", perf['uniqueness'])
                    with col4:
                        st.metric("Frameworks Used", perf['frameworks_used'])
                    
                    # Phase 3 insights
                    st.write("**🎯 Phase 3 Advantages:**")
                    st.write(f"• Applied {perf['frameworks_used']} personal frameworks")
                    st.write(f"• Achieved {perf['personalization_quality']} authenticity score")
                    st.write(f"• Generated {perf['uniqueness']} uniqueness score")
                    st.write("• Content sounds like YOUR voice and expertise")
    
    def render_phase3_evolution(self):
        """Show Phase 3 evolution and improvements"""
        if len(st.session_state.phase3_results) < 2:
            return
        
        st.header("📈 Phase 3 Personalization Evolution")
        
        # Prepare evolution data
        evolution_data = []
        for result in st.session_state.phase3_results[-10:]:
            metrics = result['metrics']
            frameworks_count = len(result['response'].get('personalized_query_analysis', {}).get('personal_frameworks', []))
            
            evolution_data.append({
                'timestamp': result['timestamp'],
                'query': result['query'][:30] + "...",
                'authenticity': metrics.content_authenticity,
                'uniqueness': metrics.uniqueness_score,
                'engagement': metrics.engagement_potential,
                'frameworks_used': frameworks_count,
                'latency': metrics.total_latency
            })
        
        df = pd.DataFrame(evolution_data)
        
        # Evolution visualization
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.line(df, x='timestamp', y=['authenticity', 'uniqueness', 'engagement'],
                         title="Phase 3 Personalization Quality Over Time")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.scatter(df, x='frameworks_used', y='authenticity', size='uniqueness',
                           hover_data=['query'], title="Frameworks vs Authenticity")
            st.plotly_chart(fig, use_container_width=True)
        
        # Phase 3 performance summary
        st.subheader("🎯 Phase 3 System Performance")
        
        avg_authenticity = df['authenticity'].mean()
        avg_uniqueness = df['uniqueness'].mean()
        avg_frameworks = df['frameworks_used'].mean()
        avg_latency = df['latency'].mean()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Avg Authenticity", f"{avg_authenticity:.2f}")
        with col2:
            st.metric("Avg Uniqueness", f"{avg_uniqueness:.2f}")
        with col3:
            st.metric("Avg Frameworks", f"{avg_frameworks:.1f}")
        with col4:
            st.metric("Avg Processing Time", f"{avg_latency:.2f}s")
        
        # Phase 3 breakthrough
        st.success("🚀 **Phase 3 Breakthrough**: Content that truly sounds like YOU with your frameworks, voice, and cross-domain expertise!")
    
    def run(self):
        """Run the Phase 3 test interface"""
        self.render_header()
        
        st.divider()
        
        self.render_personalization_preview()
        
        st.divider()
        
        self.render_query_interface()
        
        st.divider()
        
        self.render_personalized_results()
        
        if len(st.session_state.phase3_results) >= 2:
            st.divider()
            self.render_phase3_evolution()

def main():
    """Main function"""
    interface = Phase3TestInterface()
    interface.run()

if __name__ == "__main__":
    main()