#!/usr/bin/env python3
"""
Prosora Intelligence Engine - Production Version
Ready to run with your curated sources and real data
"""

import json
import yaml
import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from typing import List, Dict
import google.generativeai as genai
from config import Config
import time

class ProsoraProduction:
    def __init__(self):
        self.config = Config()
        genai.configure(api_key=self.config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-flash')  # Use Flash to avoid rate limits
        
        # Load your curated sources
        with open('prosora_sources.yaml', 'r') as f:
            self.sources = yaml.safe_load(f)
    
    def fetch_real_content(self) -> List[Dict]:
        """Fetch content from your actual curated sources"""
        
        print("📡 Fetching content from your curated sources...")
        all_content = []
        
        # Fetch from premium sources
        premium_sources = self.sources['premium_sources']
        for source in premium_sources:
            if source['type'] == 'blog' and 'url' in source:
                content = self._fetch_blog_content(source)
                all_content.extend(content)
                time.sleep(1)  # Rate limiting
        
        # Fetch from standard sources  
        standard_sources = self.sources['standard_sources']
        for source in standard_sources:
            if source['type'] == 'blog' and 'url' in source:
                content = self._fetch_blog_content(source)
                all_content.extend(content)
                time.sleep(1)  # Rate limiting
        
        print(f"✅ Fetched {len(all_content)} content pieces from {len(premium_sources + standard_sources)} sources")
        
        return all_content
    
    def _fetch_blog_content(self, source: Dict) -> List[Dict]:
        """Fetch content from a blog/RSS source"""
        
        content = []
        
        try:
            print(f"   Fetching from {source['name']}...")
            feed = feedparser.parse(source['url'])
            
            for entry in feed.entries[:2]:  # Limit to 2 articles per source
                # Extract article content
                article_text = self._extract_article_text(entry.link)
                
                content.append({
                    "type": "curated_blog",
                    "title": entry.title,
                    "summary": entry.summary if hasattr(entry, 'summary') else "",
                    "content": article_text,
                    "url": entry.link,
                    "source": source['name'],
                    "credibility_score": source['credibility'],
                    "expertise_domains": source['domains'],
                    "personal_relevance": source['relevance'],
                    "content_quality": self._determine_quality(source['credibility']),
                    "published": entry.published if hasattr(entry, 'published') else "",
                    "timestamp": datetime.now().isoformat()
                })
                
        except Exception as e:
            print(f"   ⚠️ Error fetching from {source['name']}: {e}")
            
        return content
    
    def _extract_article_text(self, url: str) -> str:
        """Extract clean text from article URL"""
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "footer", "header"]):
                script.decompose()
            
            # Get main content
            main_content = soup.find('main') or soup.find('article') or soup.find('div', class_='content')
            if main_content:
                text = main_content.get_text()
            else:
                text = soup.get_text()
            
            # Clean up text
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            clean_text = ' '.join(chunk for chunk in chunks if chunk)
            
            return clean_text[:3000]  # Limit to 3000 characters
            
        except Exception as e:
            print(f"   ⚠️ Error extracting text from {url}: {e}")
            return ""
    
    def _determine_quality(self, credibility: float) -> str:
        """Determine content quality based on credibility"""
        if credibility >= 0.8:
            return "premium"
        elif credibility >= 0.6:
            return "standard"
        else:
            return "experimental"
    
    def analyze_content_intelligently(self, content: List[Dict]) -> Dict:
        """Analyze content with intelligent insights"""
        
        print("🧠 Analyzing content with AI...")
        
        # Separate by quality tiers
        premium_content = [c for c in content if c.get('content_quality') == 'premium']
        standard_content = [c for c in content if c.get('content_quality') == 'standard']
        
        insights = {
            "premium_insights": self._analyze_premium_tier(premium_content),
            "supporting_insights": self._analyze_standard_tier(standard_content),
            "cross_domain_connections": self._find_cross_domain_patterns(content),
            "prosora_frameworks": self._generate_prosora_frameworks(content),
            "content_opportunities": self._identify_content_opportunities(content),
            "prosora_index": self._calculate_prosora_index(content)
        }
        
        return insights
    
    def _analyze_premium_tier(self, premium_content: List[Dict]) -> List[Dict]:
        """Analyze premium content for high-value insights"""
        
        if not premium_content:
            return []
        
        # Combine premium content
        premium_text = " ".join([
            f"{item.get('title', '')} {item.get('content', '')[:1000]}" 
            for item in premium_content
        ])
        
        prompt = f"""
        Analyze this PREMIUM content from high-credibility sources like a16z, Stratechery, First Round Review.
        
        You are Akash - IIT Bombay engineer, political consultant, product ops lead, FinTech MBA student.
        
        Extract 2 PREMIUM insights that only someone with your cross-domain background would identify:
        
        Content: {premium_text[:2000]}
        
        Format each as:
        **Premium Insight [X]: [Title]**
        - **Pattern**: [What sophisticated pattern do you see?]
        - **Cross-Domain**: [How does this connect tech/politics/product/finance?]
        - **Your Take**: [Your unique perspective]
        - **Content Angle**: [How to turn this into viral content]
        """
        
        try:
            response = self.model.generate_content(prompt)
            return self._parse_insights(response.text, "premium")
        except Exception as e:
            print(f"   ⚠️ Error in premium analysis: {e}")
            return []
    
    def _analyze_standard_tier(self, standard_content: List[Dict]) -> List[Dict]:
        """Analyze standard content for supporting insights"""
        
        if not standard_content:
            return []
        
        standard_text = " ".join([
            f"{item.get('title', '')} {item.get('content', '')[:800]}" 
            for item in standard_content
        ])
        
        prompt = f"""
        Analyze this STANDARD content to find supporting evidence and additional context.
        
        Content: {standard_text[:1500]}
        
        Find 1 SUPPORTING insight that validates or extends premium insights:
        
        **Supporting Insight: [Title]**
        - **Evidence**: [What data/examples support premium insights?]
        - **Context**: [Additional business context]
        - **Application**: [How can this be applied practically?]
        """
        
        try:
            response = self.model.generate_content(prompt)
            return self._parse_insights(response.text, "supporting")
        except Exception as e:
            print(f"   ⚠️ Error in standard analysis: {e}")
            return []
    
    def _find_cross_domain_patterns(self, content: List[Dict]) -> List[Dict]:
        """Find patterns across your expertise domains"""
        
        # Group content by domains
        domain_content = {}
        for item in content:
            for domain in item.get('expertise_domains', []):
                if domain not in domain_content:
                    domain_content[domain] = []
                domain_content[domain].append(item.get('title', '') + " " + item.get('content', '')[:500])
        
        prompt = f"""
        Find cross-domain connections across your expertise areas:
        
        Tech content: {len(domain_content.get('tech', []))} pieces
        Politics content: {len(domain_content.get('politics', []))} pieces  
        Product content: {len(domain_content.get('product', []))} pieces
        Finance content: {len(domain_content.get('finance', []))} pieces
        
        Sample content: {str(domain_content)[:1000]}
        
        Identify 1 CROSS-DOMAIN connection:
        
        **Cross-Domain Pattern: [Title]**
        - **Domains Connected**: [Which domains intersect?]
        - **Unique Insight**: [What connection do you see that others would miss?]
        - **Why You**: [Why does your background let you see this?]
        - **Content Hook**: [Viral social media angle]
        """
        
        try:
            response = self.model.generate_content(prompt)
            return self._parse_insights(response.text, "cross_domain")
        except Exception as e:
            print(f"   ⚠️ Error in cross-domain analysis: {e}")
            return []
    
    def _generate_prosora_frameworks(self, content: List[Dict]) -> List[Dict]:
        """Generate your signature Prosora frameworks"""
        
        high_relevance_content = sorted(content, key=lambda x: x.get('personal_relevance', 0), reverse=True)[:3]
        
        content_text = " ".join([
            f"{item.get('title', '')} {item.get('content', '')[:800]}" 
            for item in high_relevance_content
        ])
        
        prompt = f"""
        Create 1 signature "Prosora Framework" based on this content.
        
        Your signature frameworks:
        - "The Political Product Manager"
        - "FinTech Democracy" 
        - "The IIT-MBA Bridge"
        
        Content: {content_text[:1500]}
        
        Create a NEW framework:
        
        **The [Name] Framework: [Subtitle]**
        - **Core Concept**: [What's the main idea?]
        - **Your Unique Angle**: [Why only you could create this?]
        - **3 Key Principles**: [Actionable principles]
        - **Real Application**: [How people can use this]
        - **Content Series**: [How to turn this into multiple posts]
        """
        
        try:
            response = self.model.generate_content(prompt)
            return self._parse_insights(response.text, "framework")
        except Exception as e:
            print(f"   ⚠️ Error generating frameworks: {e}")
            return []
    
    def _identify_content_opportunities(self, content: List[Dict]) -> List[str]:
        """Identify immediate content opportunities"""
        
        opportunities = []
        
        # High-credibility content opportunities
        premium_count = len([c for c in content if c.get('content_quality') == 'premium'])
        if premium_count >= 2:
            opportunities.append("Create LinkedIn post from premium insights")
        
        # Cross-domain opportunities
        domains_covered = set()
        for item in content:
            domains_covered.update(item.get('expertise_domains', []))
        
        if len(domains_covered) >= 3:
            opportunities.append("Create Twitter thread on cross-domain connections")
        
        # Framework opportunities
        if any('framework' in item.get('title', '').lower() for item in content):
            opportunities.append("Develop new Prosora Framework blog post")
        
        return opportunities
    
    def _calculate_prosora_index(self, content: List[Dict]) -> Dict:
        """Calculate your personalized Prosora Index"""
        
        if not content:
            return {}
        
        # Calculate weighted scores
        total_weight = 0
        domain_scores = {'tech': 0, 'politics': 0, 'product': 0, 'finance': 0}
        
        for item in content:
            weight = item.get('credibility_score', 0.5) * item.get('personal_relevance', 0.5)
            total_weight += weight
            
            for domain in item.get('expertise_domains', []):
                if domain in domain_scores:
                    domain_scores[domain] += weight
        
        # Normalize to 0-100 scale
        if total_weight > 0:
            for domain in domain_scores:
                domain_scores[domain] = min(100, (domain_scores[domain] / total_weight) * 100)
        
        # Calculate composite score
        domain_weights = {'tech': 0.3, 'politics': 0.2, 'product': 0.25, 'finance': 0.25}
        composite_score = sum(domain_scores[d] * domain_weights[d] for d in domain_scores)
        
        return {
            'tech_innovation': domain_scores['tech'],
            'political_stability': domain_scores['politics'],
            'market_opportunity': domain_scores['product'],
            'financial_insight': domain_scores['finance'],
            'composite_prosora_score': composite_score,
            'content_quality_score': (total_weight / len(content)) * 100 if content else 0
        }
    
    def _parse_insights(self, text: str, insight_type: str) -> List[Dict]:
        """Parse insights from AI response"""
        
        insights = []
        
        # Simple parsing - can be enhanced
        if "**" in text:
            sections = text.split("**")
            for i in range(1, len(sections), 2):
                if i + 1 < len(sections):
                    title = sections[i].strip()
                    content = sections[i + 1].strip()
                    
                    insights.append({
                        "type": insight_type,
                        "title": title,
                        "content": content,
                        "generated_at": datetime.now().isoformat()
                    })
        
        return insights
    
    def generate_content(self, insights: Dict) -> Dict:
        """Generate ready-to-post content"""
        
        print("✍️ Generating content for social media...")
        
        generated_content = {
            "linkedin_posts": self._create_linkedin_posts(insights),
            "twitter_threads": self._create_twitter_threads(insights),
            "blog_ideas": self._create_blog_ideas(insights),
            "generated_at": datetime.now().isoformat()
        }
        
        return generated_content
    
    def _create_linkedin_posts(self, insights: Dict) -> List[Dict]:
        """Create LinkedIn posts from insights"""
        
        posts = []
        
        # Create post from premium insights
        premium_insights = insights.get('premium_insights', [])
        if premium_insights:
            insight = premium_insights[0]
            
            prompt = f"""
            Create a LinkedIn post based on this premium insight:
            
            {insight.get('title', '')}: {insight.get('content', '')}
            
            Style: Professional thought leadership
            Length: 200-300 words
            Include: Personal perspective from your IIT/consulting/MBA background
            End with: Engaging question
            
            Make it authentic to your voice and expertise.
            """
            
            try:
                response = self.model.generate_content(prompt)
                posts.append({
                    "type": "premium_insight",
                    "content": response.text,
                    "source_insight": insight,
                    "platform": "linkedin"
                })
            except Exception as e:
                print(f"   ⚠️ Error creating LinkedIn post: {e}")
        
        return posts
    
    def _create_twitter_threads(self, insights: Dict) -> List[Dict]:
        """Create Twitter threads from insights"""
        
        threads = []
        
        # Create thread from cross-domain connections
        cross_domain = insights.get('cross_domain_connections', [])
        if cross_domain:
            connection = cross_domain[0]
            
            prompt = f"""
            Create a Twitter thread (6 tweets) about:
            {connection.get('title', '')}: {connection.get('content', '')}
            
            Format as:
            1/6 [Hook with emoji]
            2/6 [Your background/credibility]
            3/6 [Main insight]
            4/6 [Cross-domain connection]
            5/6 [Practical application]
            6/6 [Question for engagement]
            
            Each tweet max 280 characters.
            """
            
            try:
                response = self.model.generate_content(prompt)
                tweets = self._parse_twitter_thread(response.text)
                
                threads.append({
                    "type": "cross_domain_thread",
                    "tweets": tweets,
                    "source_insight": connection,
                    "platform": "twitter"
                })
            except Exception as e:
                print(f"   ⚠️ Error creating Twitter thread: {e}")
        
        return threads
    
    def _create_blog_ideas(self, insights: Dict) -> List[Dict]:
        """Create blog post ideas from frameworks"""
        
        blog_ideas = []
        
        frameworks = insights.get('prosora_frameworks', [])
        for framework in frameworks:
            blog_ideas.append({
                "title": framework.get('title', ''),
                "concept": framework.get('content', ''),
                "type": "prosora_framework",
                "estimated_words": "1500-2000"
            })
        
        return blog_ideas
    
    def _parse_twitter_thread(self, text: str) -> List[str]:
        """Parse Twitter thread from AI response"""
        
        tweets = []
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            if '/' in line and any(line.startswith(f'{i}/') for i in range(1, 10)):
                # Extract tweet content after numbering
                parts = line.split(' ', 1)
                if len(parts) > 1:
                    tweet = parts[1].strip()
                    if len(tweet) <= 280:
                        tweets.append(tweet)
        
        return tweets
    
    def run_production_pipeline(self) -> Dict:
        """Run the complete production pipeline"""
        
        print("🚀 Starting Prosora Intelligence Engine - Production Run")
        print("=" * 60)
        
        # Step 1: Fetch real content
        print("\n📡 STEP 1: Content Aggregation")
        content = self.fetch_real_content()
        
        if not content:
            print("❌ No content fetched. Check your source URLs.")
            return {}
        
        # Step 2: Intelligent analysis
        print(f"\n🧠 STEP 2: Intelligent Analysis")
        insights = self.analyze_content_intelligently(content)
        
        # Step 3: Content generation
        print(f"\n✍️ STEP 3: Content Generation")
        generated_content = self.generate_content(insights)
        
        # Step 4: Create production report
        print(f"\n📊 STEP 4: Production Report")
        
        report = {
            "production_run": datetime.now().isoformat(),
            "content_stats": {
                "total_pieces": len(content),
                "premium_pieces": len([c for c in content if c.get('content_quality') == 'premium']),
                "sources_accessed": len(set(c.get('source', '') for c in content))
            },
            "insights_generated": {
                "premium_insights": len(insights.get('premium_insights', [])),
                "cross_domain_connections": len(insights.get('cross_domain_connections', [])),
                "prosora_frameworks": len(insights.get('prosora_frameworks', []))
            },
            "content_ready": {
                "linkedin_posts": len(generated_content.get('linkedin_posts', [])),
                "twitter_threads": len(generated_content.get('twitter_threads', [])),
                "blog_ideas": len(generated_content.get('blog_ideas', []))
            },
            "prosora_index": insights.get('prosora_index', {}),
            "content_opportunities": insights.get('content_opportunities', [])
        }
        
        # Save everything
        with open("data/production_content.json", "w") as f:
            json.dump(content, f, indent=2)
        
        with open("data/production_insights.json", "w") as f:
            json.dump(insights, f, indent=2)
        
        with open("data/production_generated.json", "w") as f:
            json.dump(generated_content, f, indent=2)
        
        with open("data/production_report.json", "w") as f:
            json.dump(report, f, indent=2)
        
        # Print summary
        self._print_production_summary(report)
        
        return report
    
    def _print_production_summary(self, report: Dict):
        """Print production run summary"""
        
        print(f"\n🎉 PRODUCTION RUN COMPLETE")
        print("=" * 60)
        
        stats = report['content_stats']
        insights = report['insights_generated']
        content = report['content_ready']
        prosora = report['prosora_index']
        
        print(f"📊 Content Processed:")
        print(f"   Total pieces: {stats['total_pieces']}")
        print(f"   Premium pieces: {stats['premium_pieces']}")
        print(f"   Sources accessed: {stats['sources_accessed']}")
        
        print(f"\n🧠 Insights Generated:")
        print(f"   Premium insights: {insights['premium_insights']}")
        print(f"   Cross-domain connections: {insights['cross_domain_connections']}")
        print(f"   Prosora frameworks: {insights['prosora_frameworks']}")
        
        print(f"\n📝 Content Ready:")
        print(f"   LinkedIn posts: {content['linkedin_posts']}")
        print(f"   Twitter threads: {content['twitter_threads']}")
        print(f"   Blog ideas: {content['blog_ideas']}")
        
        print(f"\n🎯 Prosora Index:")
        print(f"   Tech Innovation: {prosora.get('tech_innovation', 0):.1f}/100")
        print(f"   Political Stability: {prosora.get('political_stability', 0):.1f}/100")
        print(f"   Market Opportunity: {prosora.get('market_opportunity', 0):.1f}/100")
        print(f"   Financial Insight: {prosora.get('financial_insight', 0):.1f}/100")
        print(f"   Composite Score: {prosora.get('composite_prosora_score', 0):.1f}/100")
        
        print(f"\n⚡ Content Opportunities:")
        for opp in report.get('content_opportunities', [])[:3]:
            print(f"   • {opp}")
        
        print(f"\n💾 Files saved:")
        print(f"   • data/production_content.json")
        print(f"   • data/production_insights.json") 
        print(f"   • data/production_generated.json")
        print(f"   • data/production_report.json")

if __name__ == "__main__":
    engine = ProsoraProduction()
    report = engine.run_production_pipeline()