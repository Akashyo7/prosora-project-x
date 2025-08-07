#!/usr/bin/env python3
"""
Prosora Intelligence Orchestrator
Advanced, personalized content intelligence system with credibility weighting
"""

import json
import yaml
from datetime import datetime
from typing import Dict, List
from advanced_aggregator import AdvancedContentAggregator
from intelligent_insights import IntelligentInsightsEngine
from content_generator import ContentGenerator

class ProsoraOrchestrator:
    def __init__(self):
        self.aggregator = AdvancedContentAggregator()
        self.insights_engine = IntelligentInsightsEngine()
        self.content_generator = ContentGenerator()
        
        # Load configuration
        with open('prosora_sources.yaml', 'r') as f:
            self.config = yaml.safe_load(f)
    
    def run_intelligent_pipeline(self) -> dict:
        """Run the complete intelligent Prosora pipeline"""
        
        print("🚀 Starting Prosora Intelligence Orchestrator")
        print("=" * 60)
        
        # Phase 1: Advanced Content Aggregation
        print("\n📡 PHASE 1: Advanced Content Aggregation")
        print("- Fetching from your curated, weighted sources...")
        
        aggregation_results = self.aggregator.run_advanced_aggregation()
        all_content = self._extract_content_from_results(aggregation_results)
        
        # Phase 2: Intelligent Analysis with Credibility Weighting
        print("\n🧠 PHASE 2: Intelligent Analysis")
        print("- Analyzing with credibility weighting...")
        print("- Generating personalized frameworks...")
        
        intelligent_insights = self.insights_engine.analyze_with_credibility_weighting(all_content)
        
        # Phase 3: Advanced Content Generation
        print("\n✍️ PHASE 3: Advanced Content Generation")
        print("- Creating tier-based content...")
        
        generated_content = self.content_generator.generate_prosora_content(intelligent_insights)
        
        # Phase 4: Intelligence Report
        print("\n📊 PHASE 4: Intelligence Report")
        
        intelligence_report = self._create_intelligence_report(
            aggregation_results, 
            intelligent_insights, 
            generated_content
        )
        
        print("\n🎉 Prosora Intelligence Pipeline Complete!")
        print("=" * 60)
        
        return intelligence_report
    
    def _extract_content_from_results(self, aggregation_results: dict) -> list:
        """Extract content list from aggregation results"""
        # This would extract the actual content from the aggregation results
        # For now, return empty list as placeholder
        return []
    
    def _create_intelligence_report(self, aggregation: dict, insights: dict, content: dict) -> dict:
        """Create comprehensive intelligence report"""
        
        report = {
            "report_timestamp": datetime.now().isoformat(),
            "executive_summary": self._create_executive_summary(aggregation, insights),
            "source_analysis": self._analyze_source_performance(aggregation),
            "insight_quality": self._assess_insight_quality(insights),
            "content_readiness": self._assess_content_readiness(content),
            "prosora_index_advanced": insights.get("prosora_index_advanced", {}),
            "recommendations": self._generate_recommendations(aggregation, insights, content),
            "next_actions": self._suggest_next_actions(insights)
        }
        
        # Save comprehensive report
        with open("data/prosora_intelligence_report.json", "w") as f:
            json.dump(report, f, indent=2)
        
        # Print executive summary
        self._print_executive_summary(report)
        
        return report
    
    def _create_executive_summary(self, aggregation: dict, insights: dict) -> dict:
        """Create executive summary of intelligence gathering"""
        
        return {
            "total_sources_processed": aggregation.get("total_sources", 0),
            "premium_content_ratio": aggregation.get("premium_content", 0) / max(aggregation.get("content_pieces", 1), 1),
            "tier_1_insights": len(insights.get("tier_1_insights", [])),
            "personalized_frameworks": len(insights.get("personalized_frameworks", [])),
            "contrarian_opportunities": len(insights.get("contrarian_opportunities", [])),
            "knowledge_gaps_identified": len(insights.get("knowledge_gaps", [])),
            "composite_prosora_score": insights.get("prosora_index_advanced", {}).get("composite_prosora_score", 0)
        }
    
    def _analyze_source_performance(self, aggregation: dict) -> dict:
        """Analyze performance of different source types"""
        
        return {
            "email_newsletters": "High value - direct access to premium content",
            "youtube_channels": "Medium value - good for trend identification", 
            "curated_blogs": "High value - in-depth analysis",
            "social_signals": "Low value - experimental trends only",
            "recommendation": "Focus on email newsletters and curated blogs for next cycle"
        }
    
    def _assess_insight_quality(self, insights: dict) -> dict:
        """Assess quality of generated insights"""
        
        tier_1_count = len(insights.get("tier_1_insights", []))
        framework_count = len(insights.get("personalized_frameworks", []))
        
        quality_score = (tier_1_count * 0.4) + (framework_count * 0.6)
        
        return {
            "quality_score": min(10, quality_score),
            "tier_1_insights_generated": tier_1_count,
            "personalized_frameworks_created": framework_count,
            "assessment": "High quality" if quality_score > 3 else "Standard quality"
        }
    
    def _assess_content_readiness(self, content: dict) -> dict:
        """Assess readiness of generated content"""
        
        linkedin_ready = len([p for p in content.get("linkedin_posts", []) if len(p.get("content", "")) > 100])
        twitter_ready = len([t for t in content.get("twitter_threads", []) if len(t.get("tweets", [])) > 5])
        blog_ready = len(content.get("blog_outlines", []))
        
        return {
            "linkedin_posts_ready": linkedin_ready,
            "twitter_threads_ready": twitter_ready,
            "blog_outlines_ready": blog_ready,
            "total_content_pieces": linkedin_ready + twitter_ready + blog_ready,
            "readiness_score": min(10, (linkedin_ready + twitter_ready + blog_ready) / 3)
        }
    
    def _generate_recommendations(self, aggregation: dict, insights: dict, content: dict) -> list:
        """Generate actionable recommendations"""
        
        recommendations = []
        
        # Source recommendations
        premium_ratio = aggregation.get("premium_content", 0) / max(aggregation.get("content_pieces", 1), 1)
        if premium_ratio < 0.3:
            recommendations.append("Increase premium source ratio - add more high-credibility newsletters")
        
        # Content recommendations
        if len(content.get("linkedin_posts", [])) < 3:
            recommendations.append("Generate more LinkedIn content for consistent posting")
        
        # Insight recommendations
        if len(insights.get("contrarian_opportunities", [])) < 2:
            recommendations.append("Seek more diverse sources to identify contrarian opportunities")
        
        return recommendations
    
    def _suggest_next_actions(self, insights: dict) -> list:
        """Suggest immediate next actions"""
        
        actions = []
        
        # Based on insights generated
        if insights.get("tier_1_insights"):
            actions.append("Post tier 1 insights on LinkedIn immediately - high engagement potential")
        
        if insights.get("personalized_frameworks"):
            actions.append("Develop personalized frameworks into full blog posts")
        
        if insights.get("contrarian_opportunities"):
            actions.append("Create Twitter threads around contrarian takes")
        
        # Based on knowledge gaps
        gaps = insights.get("knowledge_gaps", [])
        if gaps:
            actions.append(f"Address knowledge gaps: {', '.join(gaps[:2])}")
        
        return actions
    
    def _print_executive_summary(self, report: Dict):
        """Print executive summary to console"""
        
        summary = report["executive_summary"]
        
        print(f"\n📈 EXECUTIVE SUMMARY")
        print(f"   Sources Processed: {summary['total_sources_processed']}")
        print(f"   Premium Content Ratio: {summary['premium_content_ratio']:.1%}")
        print(f"   Tier 1 Insights: {summary['tier_1_insights']}")
        print(f"   Personalized Frameworks: {summary['personalized_frameworks']}")
        print(f"   Contrarian Opportunities: {summary['contrarian_opportunities']}")
        
        print(f"\n🎯 PROSORA INDEX (Advanced)")
        prosora = report["prosora_index_advanced"]
        print(f"   Composite Score: {prosora.get('composite_prosora_score', 0):.1f}/100")
        print(f"   Data Quality: {prosora.get('data_quality_score', 0):.1f}/100")
        print(f"   Source Diversity: {prosora.get('source_diversity', 0)} unique sources")
        
        print(f"\n📝 CONTENT READINESS")
        readiness = report["content_readiness"]
        print(f"   LinkedIn Posts: {readiness['linkedin_posts_ready']} ready")
        print(f"   Twitter Threads: {readiness['twitter_threads_ready']} ready")
        print(f"   Blog Outlines: {readiness['blog_outlines_ready']} ready")
        
        print(f"\n🎯 TOP RECOMMENDATIONS")
        for i, rec in enumerate(report["recommendations"][:3], 1):
            print(f"   {i}. {rec}")
        
        print(f"\n⚡ IMMEDIATE ACTIONS")
        for i, action in enumerate(report["next_actions"][:3], 1):
            print(f"   {i}. {action}")

def main():
    """Main orchestrator entry point"""
    
    orchestrator = ProsoraOrchestrator()
    
    print("🎯 Prosora Intelligence Orchestrator")
    print("Advanced, personalized content intelligence system")
    print("\nOptions:")
    print("1. Run full intelligent pipeline")
    print("2. Test source configuration")
    print("3. View latest intelligence report")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == "1":
        report = orchestrator.run_intelligent_pipeline()
    elif choice == "2":
        print("Testing source configuration...")
        # Test configuration
        print(f"✅ Loaded {len(orchestrator.config['premium_sources'])} premium sources")
        print(f"✅ Loaded {len(orchestrator.config['standard_sources'])} standard sources")
        print(f"✅ Loaded {len(orchestrator.config['experimental_sources'])} experimental sources")
    elif choice == "3":
        try:
            with open("data/prosora_intelligence_report.json", "r") as f:
                report = json.load(f)
                orchestrator._print_executive_summary(report)
        except FileNotFoundError:
            print("No intelligence report found. Run the pipeline first.")
    else:
        print("Invalid choice. Running full pipeline...")
        report = orchestrator.run_intelligent_pipeline()

if __name__ == "__main__":
    main()