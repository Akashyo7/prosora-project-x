#!/usr/bin/env python3
"""
Enhanced Content Generator with Automatic Evidence Integration
Generates content with built-in Google evidence research
"""

import json
import google.generativeai as genai
from typing import Dict, List
from datetime import datetime
from config import Config
from google_evidence_search import GoogleEvidenceSearch
import time

class EnhancedContentGenerator:
    def __init__(self):
        self.config = Config()
        genai.configure(api_key=self.config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Initialize evidence search
        self.evidence_search = GoogleEvidenceSearch()
    
    def generate_evidence_backed_content(self, insights: Dict) -> Dict:
        """Generate content with automatic evidence integration"""
        
        print("✍️ Generating evidence-backed content...")
        
        generated_content = {
            "linkedin_posts": self._create_evidence_backed_linkedin_posts(insights),
            "twitter_threads": self._create_evidence_backed_twitter_threads(insights),
            "blog_outlines": self._create_evidence_backed_blog_outlines(insights),
            "generated_at": datetime.now().isoformat()
        }
        
        return generated_content
    
    def _create_evidence_backed_linkedin_posts(self, insights: Dict) -> List[Dict]:
        """Create LinkedIn posts with automatic evidence research"""
        
        posts = []
        
        # Get premium insights for LinkedIn posts
        premium_insights = insights.get('premium_insights', [])
        cross_domain = insights.get('cross_domain_connections', [])
        
        # Combine insights for processing
        all_insights = premium_insights + cross_domain
        
        for insight in all_insights[:2]:  # Process top 2 insights
            print(f"   📝 Creating LinkedIn post for: {insight.get('title', 'Untitled')[:50]}...")
            
            # Step 1: Enhance insight with evidence
            enhanced_insight = self._enhance_with_evidence(insight)
            
            # Step 2: Generate content with evidence woven in
            linkedin_post = self._generate_linkedin_with_evidence(enhanced_insight)
            
            if linkedin_post:
                posts.append(linkedin_post)
                time.sleep(1)  # Rate limiting
        
        return posts
    
    def _create_evidence_backed_twitter_threads(self, insights: Dict) -> List[Dict]:
        """Create Twitter threads with automatic evidence research"""
        
        threads = []
        
        cross_domain = insights.get('cross_domain_connections', [])
        
        for connection in cross_domain[:1]:  # Process 1 connection for Twitter
            print(f"   🧵 Creating Twitter thread for: {connection.get('title', 'Untitled')[:50]}...")
            
            # Enhance with evidence
            enhanced_connection = self._enhance_with_evidence(connection)
            
            # Generate thread with evidence
            twitter_thread = self._generate_twitter_thread_with_evidence(enhanced_connection)
            
            if twitter_thread:
                threads.append(twitter_thread)
                time.sleep(1)
        
        return threads
    
    def _create_evidence_backed_blog_outlines(self, insights: Dict) -> List[Dict]:
        """Create blog outlines with automatic evidence research"""
        
        outlines = []
        
        frameworks = insights.get('prosora_frameworks', [])
        
        for framework in frameworks[:1]:  # Process 1 framework for blog
            print(f"   📖 Creating blog outline for: {framework.get('title', 'Untitled')[:50]}...")
            
            # Enhance with evidence
            enhanced_framework = self._enhance_with_evidence(framework)
            
            # Generate outline with evidence
            blog_outline = self._generate_blog_outline_with_evidence(enhanced_framework)
            
            if blog_outline:
                outlines.append(blog_outline)
        
        return outlines
    
    def _enhance_with_evidence(self, insight: Dict) -> Dict:
        """Enhance insight with Google evidence search"""
        
        try:
            # Search for supporting evidence
            enhanced_insight = self.evidence_search.enhance_insight_with_evidence(insight)
            print(f"      🔍 Found {enhanced_insight['evidence_count']} supporting sources")
            return enhanced_insight
        except Exception as e:
            print(f"      ⚠️ Evidence search failed: {e}")
            # Return original insight if evidence search fails
            return insight
    
    def _generate_linkedin_with_evidence(self, enhanced_insight: Dict) -> Dict:
        """Generate LinkedIn post with evidence seamlessly integrated"""
        
        # Extract evidence for context
        evidence_context = self._format_evidence_for_prompt(enhanced_insight.get('supporting_evidence', []))
        
        prompt = f"""
        You are Akash - IIT Bombay engineer, political consultant, product ops lead, FinTech MBA student.
        
        Write a LinkedIn post based on this insight with supporting evidence naturally woven in:
        
        **Main Insight:**
        {enhanced_insight.get('title', '')}: {enhanced_insight.get('content', '')}
        
        **Supporting Evidence to Reference:**
        {evidence_context}
        
        **Writing Style:**
        - Professional thought leadership tone
        - 250-300 words
        - Start with a compelling hook
        - Naturally reference evidence without being academic
        - Include your personal perspective from IIT/consulting/MBA background
        - End with an engaging question
        - Use phrases like "Recent research shows..." or "According to industry analysis..."
        
        **Format:**
        Write as if you're sharing your expert analysis backed by credible sources, not just opinion.
        Make evidence feel natural, not forced.
        """
        
        try:
            response = self.model.generate_content(prompt)
            
            return {
                "type": "evidence_backed_post",
                "content": response.text,
                "source_insight": enhanced_insight,
                "evidence_count": enhanced_insight.get('evidence_count', 0),
                "evidence_credibility": enhanced_insight.get('evidence_credibility', 0),
                "platform": "linkedin",
                "generated_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"      ❌ Error generating LinkedIn post: {e}")
            return {}
    
    def _generate_twitter_thread_with_evidence(self, enhanced_connection: Dict) -> Dict:
        """Generate Twitter thread with evidence integrated"""
        
        evidence_context = self._format_evidence_for_prompt(enhanced_connection.get('supporting_evidence', []))
        
        prompt = f"""
        Create a Twitter thread (6-7 tweets) based on this cross-domain insight with evidence:
        
        **Insight:**
        {enhanced_connection.get('title', '')}: {enhanced_connection.get('content', '')}
        
        **Supporting Evidence:**
        {evidence_context}
        
        **Thread Structure:**
        1/7 Hook with surprising insight + emoji
        2/7 Your credibility (IIT + consulting + product + MBA)
        3/7 Main insight with evidence reference ("Recent studies show...")
        4/7 Cross-domain analysis with data point
        5/7 Personal experience/example
        6/7 Broader implications with evidence
        7/7 Engaging question + relevant hashtags
        
        **Style:**
        - Each tweet max 280 characters
        - Naturally weave in evidence without being academic
        - Use phrases like "Data shows..." or "Research indicates..."
        - Make evidence feel conversational
        
        Format as: "1/7 [tweet content]"
        """
        
        try:
            response = self.model.generate_content(prompt)
            tweets = self._parse_twitter_thread(response.text)
            
            return {
                "type": "evidence_backed_thread",
                "tweets": tweets,
                "source_insight": enhanced_connection,
                "evidence_count": enhanced_connection.get('evidence_count', 0),
                "platform": "twitter",
                "generated_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"      ❌ Error generating Twitter thread: {e}")
            return {}
    
    def _generate_blog_outline_with_evidence(self, enhanced_framework: Dict) -> Dict:
        """Generate blog outline with evidence integrated"""
        
        evidence_context = self._format_evidence_for_prompt(enhanced_framework.get('supporting_evidence', []))
        
        prompt = f"""
        Create a detailed blog outline based on this framework with evidence integration:
        
        **Framework:**
        {enhanced_framework.get('title', '')}: {enhanced_framework.get('content', '')}
        
        **Supporting Evidence:**
        {evidence_context}
        
        **Blog Structure:**
        1. Introduction with hook and evidence-backed thesis
        2. Framework explanation with research support
        3. Real-world applications with case studies
        4. Evidence-backed benefits and outcomes
        5. Implementation guide with data points
        6. Conclusion with call-to-action
        
        **Evidence Integration:**
        - Weave evidence naturally throughout sections
        - Use academic sources for credibility
        - Include news sources for current relevance
        - Reference trend data for market validation
        
        Target: 1500-2000 words with evidence-backed authority
        """
        
        try:
            response = self.model.generate_content(prompt)
            
            return {
                "title": enhanced_framework.get('title', ''),
                "outline": response.text,
                "type": "evidence_backed_framework",
                "evidence_count": enhanced_framework.get('evidence_count', 0),
                "estimated_words": "1500-2000",
                "generated_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"      ❌ Error generating blog outline: {e}")
            return {}
    
    def _format_evidence_for_prompt(self, evidence_list: List[Dict]) -> str:
        """Format evidence for AI prompt context"""
        
        if not evidence_list:
            return "No specific evidence available - use general knowledge."
        
        formatted_evidence = []
        
        for evidence in evidence_list[:3]:  # Use top 3 pieces of evidence
            formatted_evidence.append(
                f"• {evidence.get('title', 'Unknown')} ({evidence.get('source', 'Unknown source')}): "
                f"{evidence.get('snippet', 'No description available')}"
            )
        
        return "\n".join(formatted_evidence)
    
    def _parse_twitter_thread(self, thread_text: str) -> List[str]:
        """Parse Twitter thread from AI response"""
        
        tweets = []
        lines = thread_text.split('\n')
        
        for line in lines:
            line = line.strip()
            # Look for numbered tweets like "1/7", "2/7", etc.
            if '/' in line and any(line.startswith(f'{i}/') for i in range(1, 10)):
                # Extract tweet content after numbering
                parts = line.split(' ', 1)
                if len(parts) > 1:
                    tweet = parts[1].strip()
                    if tweet and len(tweet) <= 280:
                        tweets.append(tweet)
        
        return tweets

# Integration function
def integrate_enhanced_content_generation():
    """Test the enhanced content generation with evidence"""
    
    generator = EnhancedContentGenerator()
    
    # Sample insights for testing
    sample_insights = {
        'premium_insights': [
            {
                'title': 'AI Regulation Creates FinTech Opportunities',
                'content': 'The intersection of AI regulation and financial technology creates both challenges and opportunities for startups.',
                'type': 'premium_insight'
            }
        ],
        'cross_domain_connections': [
            {
                'title': 'Political Campaign Strategies for Product Launches',
                'content': 'Product launches can learn from political campaign strategies in audience targeting and messaging.',
                'type': 'cross_domain'
            }
        ],
        'prosora_frameworks': [
            {
                'title': 'The Political Product Manager Framework',
                'content': 'A methodology for applying political campaign strategies to product management.',
                'type': 'framework'
            }
        ]
    }
    
    # Generate evidence-backed content
    content = generator.generate_evidence_backed_content(sample_insights)
    
    print("\n🎉 Enhanced Content Generation Complete!")
    print(f"📝 LinkedIn posts: {len(content['linkedin_posts'])}")
    print(f"🧵 Twitter threads: {len(content['twitter_threads'])}")
    print(f"📖 Blog outlines: {len(content['blog_outlines'])}")
    
    # Show sample LinkedIn post
    if content['linkedin_posts']:
        post = content['linkedin_posts'][0]
        print(f"\n📝 Sample LinkedIn Post (Evidence Count: {post.get('evidence_count', 0)}):")
        print("-" * 50)
        print(post.get('content', '')[:300] + "...")
        print("-" * 50)
    
    return content

if __name__ == "__main__":
    integrate_enhanced_content_generation()