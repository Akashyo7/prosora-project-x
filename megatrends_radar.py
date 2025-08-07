#!/usr/bin/env python3
"""
Megatrends Radar Chart
Dual-layer radar chart showing expertise vs global megatrends
"""

import yaml
import plotly.graph_objects as go
import pandas as pd
from typing import Dict, List

class MegatrendsRadar:
    def __init__(self):
        # Load megatrends configuration
        with open('prosora_sources.yaml', 'r') as f:
            config = yaml.safe_load(f)
        
        self.megatrends = config.get('megatrends', [])
        self.megatrend_categories = config.get('megatrend_categories', [])
    
    def create_dual_layer_radar(self, prosora_data: Dict) -> go.Figure:
        """Create dual-layer radar chart: expertise vs megatrends"""
        
        # Prepare data for both layers
        categories = ['Tech Innovation', 'Political Stability', 'Market Opportunity', 'Financial Insight']
        
        # Layer 1: Your current expertise
        expertise_values = [
            prosora_data.get('tech_innovation', 0),
            prosora_data.get('political_stability', 0),
            prosora_data.get('market_opportunity', 0),
            prosora_data.get('financial_insight', 0)
        ]
        
        # Layer 2: Megatrend alignment scores
        megatrend_values = self._calculate_megatrend_alignment()
        
        # Create the dual-layer radar chart
        fig = go.Figure()
        
        # Add expertise layer (your current scores)
        fig.add_trace(go.Scatterpolar(
            r=expertise_values,
            theta=categories,
            fill='toself',
            name='Your Expertise',
            line_color='rgb(0, 123, 255)',
            fillcolor='rgba(0, 123, 255, 0.3)',
            hovertemplate='<b>%{theta}</b><br>Your Score: %{r:.1f}/100<extra></extra>'
        ))
        
        # Add megatrend layer (future opportunity alignment)
        fig.add_trace(go.Scatterpolar(
            r=megatrend_values,
            theta=categories,
            fill='toself',
            name='Megatrend Alignment',
            line_color='rgb(255, 99, 71)',
            fillcolor='rgba(255, 99, 71, 0.2)',
            hovertemplate='<b>%{theta}</b><br>Megatrend Score: %{r:.1f}/100<extra></extra>'
        ))
        
        # Update layout
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    tickfont=dict(size=10),
                    gridcolor='lightgray'
                ),
                angularaxis=dict(
                    tickfont=dict(size=12)
                )
            ),
            showlegend=True,
            title={
                'text': "Expertise vs Megatrends Alignment",
                'x': 0.5,
                'font': {'size': 16}
            },
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            height=400
        )
        
        return fig
    
    def _calculate_megatrend_alignment(self) -> List[float]:
        """Calculate alignment scores for each domain based on megatrends"""
        
        # Group megatrends by domain
        domain_alignment = {
            'tech': [],
            'politics': [],
            'product': [],
            'finance': []
        }
        
        for trend in self.megatrends:
            category = trend.get('category', '')
            alignment = trend.get('your_alignment', 0)
            relevance = trend.get('relevance_score', 0)
            
            # Weight alignment by relevance
            weighted_alignment = (alignment * relevance) / 100
            
            if category in domain_alignment:
                domain_alignment[category].append(weighted_alignment)
        
        # Calculate average alignment for each domain
        megatrend_scores = []
        
        # Tech Innovation
        tech_scores = domain_alignment['tech']
        tech_avg = sum(tech_scores) / len(tech_scores) if tech_scores else 0
        megatrend_scores.append(tech_avg)
        
        # Political Stability
        politics_scores = domain_alignment['politics']
        politics_avg = sum(politics_scores) / len(politics_scores) if politics_scores else 0
        megatrend_scores.append(politics_avg)
        
        # Market Opportunity (product)
        product_scores = domain_alignment['product']
        product_avg = sum(product_scores) / len(product_scores) if product_scores else 0
        megatrend_scores.append(product_avg)
        
        # Financial Insight
        finance_scores = domain_alignment['finance']
        finance_avg = sum(finance_scores) / len(finance_scores) if finance_scores else 0
        megatrend_scores.append(finance_avg)
        
        return megatrend_scores
    
    def get_megatrend_insights(self) -> Dict:
        """Get insights about megatrend alignment"""
        
        alignment_scores = self._calculate_megatrend_alignment()
        categories = ['Tech Innovation', 'Political Stability', 'Market Opportunity', 'Financial Insight']
        
        # Find strongest and weakest alignments
        max_idx = alignment_scores.index(max(alignment_scores))
        min_idx = alignment_scores.index(min(alignment_scores))
        
        strongest_domain = categories[max_idx]
        weakest_domain = categories[min_idx]
        
        # Get top megatrends by relevance
        top_trends = sorted(self.megatrends, key=lambda x: x.get('relevance_score', 0), reverse=True)[:3]
        
        # Calculate opportunity gaps
        opportunity_gaps = []
        for i, (category, score) in enumerate(zip(categories, alignment_scores)):
            if score < 70:  # Below 70 is considered a gap
                opportunity_gaps.append({
                    'domain': category,
                    'current_alignment': score,
                    'improvement_potential': 100 - score
                })
        
        return {
            'strongest_alignment': {
                'domain': strongest_domain,
                'score': alignment_scores[max_idx]
            },
            'weakest_alignment': {
                'domain': weakest_domain,
                'score': alignment_scores[min_idx]
            },
            'top_megatrends': [
                {
                    'name': trend['name'],
                    'relevance': trend['relevance_score'],
                    'your_alignment': trend['your_alignment'],
                    'category': trend['category']
                }
                for trend in top_trends
            ],
            'opportunity_gaps': opportunity_gaps,
            'overall_alignment': sum(alignment_scores) / len(alignment_scores)
        }
    
    def create_megatrend_breakdown_chart(self) -> go.Figure:
        """Create detailed breakdown of individual megatrends"""
        
        # Prepare data
        trend_names = [trend['name'] for trend in self.megatrends]
        relevance_scores = [trend['relevance_score'] for trend in self.megatrends]
        alignment_scores = [trend['your_alignment'] for trend in self.megatrends]
        categories = [trend['category'] for trend in self.megatrends]
        
        # Create scatter plot
        fig = go.Figure()
        
        # Color map for categories
        color_map = {
            'tech': 'rgb(0, 123, 255)',
            'politics': 'rgb(255, 99, 71)',
            'product': 'rgb(50, 205, 50)',
            'finance': 'rgb(255, 165, 0)'
        }
        
        for category in set(categories):
            category_trends = [i for i, cat in enumerate(categories) if cat == category]
            
            fig.add_trace(go.Scatter(
                x=[relevance_scores[i] for i in category_trends],
                y=[alignment_scores[i] for i in category_trends],
                mode='markers+text',
                name=category.title(),
                text=[trend_names[i] for i in category_trends],
                textposition="top center",
                marker=dict(
                    size=12,
                    color=color_map.get(category, 'gray'),
                    opacity=0.7
                ),
                hovertemplate='<b>%{text}</b><br>Relevance: %{x}<br>Your Alignment: %{y}<extra></extra>'
            ))
        
        # Update layout
        fig.update_layout(
            title="Megatrends: Relevance vs Your Alignment",
            xaxis_title="Global Relevance Score",
            yaxis_title="Your Alignment Score",
            showlegend=True,
            height=500,
            xaxis=dict(range=[0, 100]),
            yaxis=dict(range=[0, 100])
        )
        
        # Add quadrant lines
        fig.add_hline(y=50, line_dash="dash", line_color="gray", opacity=0.5)
        fig.add_vline(x=50, line_dash="dash", line_color="gray", opacity=0.5)
        
        # Add quadrant labels
        fig.add_annotation(x=75, y=75, text="High Impact<br>High Alignment", showarrow=False, opacity=0.7)
        fig.add_annotation(x=25, y=75, text="Low Impact<br>High Alignment", showarrow=False, opacity=0.7)
        fig.add_annotation(x=75, y=25, text="High Impact<br>Low Alignment", showarrow=False, opacity=0.7)
        fig.add_annotation(x=25, y=25, text="Low Impact<br>Low Alignment", showarrow=False, opacity=0.7)
        
        return fig

# Demo function
def demo_megatrends_radar():
    """Demo the megatrends radar functionality"""
    
    radar = MegatrendsRadar()
    
    # Sample prosora data
    sample_prosora_data = {
        'tech_innovation': 85,
        'political_stability': 65,
        'market_opportunity': 78,
        'financial_insight': 72
    }
    
    # Create dual-layer radar chart
    fig = radar.create_dual_layer_radar(sample_prosora_data)
    
    # Get insights
    insights = radar.get_megatrend_insights()
    
    print("🎯 Megatrends Analysis:")
    print(f"Strongest Alignment: {insights['strongest_alignment']['domain']} ({insights['strongest_alignment']['score']:.1f})")
    print(f"Weakest Alignment: {insights['weakest_alignment']['domain']} ({insights['weakest_alignment']['score']:.1f})")
    print(f"Overall Alignment: {insights['overall_alignment']:.1f}/100")
    
    print(f"\n🚀 Top Megatrends:")
    for trend in insights['top_megatrends']:
        print(f"• {trend['name']} - Relevance: {trend['relevance']}, Your Alignment: {trend['your_alignment']}")
    
    print(f"\n💡 Opportunity Gaps:")
    for gap in insights['opportunity_gaps']:
        print(f"• {gap['domain']}: {gap['improvement_potential']:.1f} points improvement potential")
    
    return fig, insights

if __name__ == "__main__":
    fig, insights = demo_megatrends_radar()
    print("\n📊 Megatrends radar chart created successfully!")