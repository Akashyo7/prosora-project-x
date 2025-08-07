#!/usr/bin/env python3
"""
Prosora Intelligence Engine - Main Orchestrator
Your AI-powered personal branding and content intelligence system
"""

import json
import os
from datetime import datetime
from content_aggregator import ContentAggregator
from ai_analyzer import AIAnalyzer
from content_generator import ContentGenerator

class ProsoraEngine:
    def __init__(self):
        self.aggregator = ContentAggregator()
        self.analyzer = AIAnalyzer()
        self.generator = ContentGenerator()
        
        # Ensure data directory exists
        os.makedirs("data", exist_ok=True)
        
    def run_full_pipeline(self):
        """Run the complete Prosora Intelligence pipeline"""
        print("🚀 Starting Prosora Intelligence Engine...")
        print("=" * 50)
        
        try:
            # Step 1: Aggregate content from all sources
            print("\n📥 STEP 1: Content Aggregation")
            raw_content = self.aggregator.aggregate_all_content()
            
            # Step 2: AI analysis for insights
            print("\n🧠 STEP 2: AI Analysis & Insights")
            insights = self.analyzer.analyze_content_for_insights(raw_content)
            
            # Step 3: Generate branded content
            print("\n✍️ STEP 3: Content Generation")
            generated_content = self.generator.generate_prosora_content(insights)
            
            # Step 4: Create summary report
            print("\n📊 STEP 4: Summary Report")
            summary = self._create_summary_report(raw_content, insights, generated_content)
            
            print("\n🎉 Prosora Intelligence Engine Complete!")
            print("=" * 50)
            
            return summary
            
        except Exception as e:
            print(f"❌ Error in Prosora Engine: {e}")
            return None
    
    def _create_summary_report(self, raw_content, insights, generated_content):
        """Create a summary report of the pipeline run"""
        
        summary = {
            "run_timestamp": datetime.now().isoformat(),
            "content_stats": {
                "newsletters_processed": len(raw_content.get("newsletters", [])),
                "youtube_transcripts": len(raw_content.get("youtube", [])),
                "trend_items": len(raw_content.get("trends", [])),
            },
            "insights_generated": {
                "cross_domain_connections": len(insights.get("cross_domain_connections", [])),
                "contrarian_opportunities": len(insights.get("contrarian_opportunities", [])),
                "trending_intersections": len(insights.get("trending_intersections", [])),
            },
            "content_generated": {
                "linkedin_posts": len(generated_content.get("linkedin_posts", [])),
                "twitter_threads": len(generated_content.get("twitter_threads", [])),
                "blog_outlines": len(generated_content.get("blog_outlines", [])),
                "prosora_predictions": len(generated_content.get("prosora_predictions", [])),
            },
            "prosora_index": insights.get("prosora_index_signals", {}),
            "top_insights": [
                conn.get("title", "") for conn in insights.get("cross_domain_connections", [])[:3]
            ],
            "ready_to_post": {
                "linkedin": len([p for p in generated_content.get("linkedin_posts", []) if len(p.get("content", "")) > 100]),
                "twitter": len(generated_content.get("twitter_threads", [])),
                "blog": len(generated_content.get("blog_outlines", []))
            }
        }
        
        # Save summary
        with open("data/prosora_summary.json", "w") as f:
            json.dump(summary, f, indent=2)
            
        # Print summary
        print(f"📈 Content Processed: {summary['content_stats']['newsletters_processed']} newsletters, {summary['content_stats']['youtube_transcripts']} videos, {summary['content_stats']['trend_items']} trends")
        print(f"💡 Insights Generated: {summary['insights_generated']['cross_domain_connections']} connections, {summary['insights_generated']['contrarian_opportunities']} contrarian takes")
        print(f"📝 Content Ready: {summary['ready_to_post']['linkedin']} LinkedIn posts, {summary['ready_to_post']['twitter']} Twitter threads, {summary['ready_to_post']['blog']} blog outlines")
        
        print(f"\n🎯 Current Prosora Index:")
        for metric, score in summary['prosora_index'].items():
            print(f"   {metric.replace('_', ' ').title()}: {score:.1f}/100")
            
        print(f"\n🔥 Top Insights:")
        for i, insight in enumerate(summary['top_insights'], 1):
            print(f"   {i}. {insight}")
            
        return summary
    
    def quick_content_generation(self, topic: str = None):
        """Quick content generation for a specific topic"""
        print(f"⚡ Quick content generation for: {topic or 'trending topics'}")
        
        if topic:
            # Generate content for specific topic
            insights = {
                "cross_domain_connections": [{
                    "title": f"Cross-domain perspective on {topic}",
                    "insight": f"Analyzing {topic} through tech, politics, product, and fintech lens",
                    "hook": f"Why {topic} is more complex than it appears"
                }],
                "contrarian_opportunities": [],
                "prosora_index_signals": {"tech_innovation": 50, "political_stability": 50, "market_opportunity": 50, "social_impact": 50}
            }
        else:
            # Load latest insights if available
            try:
                with open("data/content_analysis.json", "r") as f:
                    insights = json.load(f)
            except FileNotFoundError:
                print("No previous insights found. Run full pipeline first.")
                return None
                
        generated_content = self.generator.generate_prosora_content(insights)
        print("✅ Quick content generated!")
        
        return generated_content

def main():
    """Main entry point"""
    engine = ProsoraEngine()
    
    print("🎯 Prosora Intelligence Engine")
    print("Choose an option:")
    print("1. Run full pipeline (aggregation + analysis + generation)")
    print("2. Quick content generation")
    print("3. View latest summary")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == "1":
        engine.run_full_pipeline()
    elif choice == "2":
        topic = input("Enter specific topic (or press Enter for trending): ").strip()
        engine.quick_content_generation(topic if topic else None)
    elif choice == "3":
        try:
            with open("data/prosora_summary.json", "r") as f:
                summary = json.load(f)
                print(json.dumps(summary, indent=2))
        except FileNotFoundError:
            print("No summary found. Run the pipeline first.")
    else:
        print("Invalid choice. Running full pipeline...")
        engine.run_full_pipeline()

if __name__ == "__main__":
    main()