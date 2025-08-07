import json
import google.generativeai as genai
from typing import Dict, List
from datetime import datetime
from config import Config

class ContentGenerator:
    def __init__(self):
        self.config = Config()
        genai.configure(api_key=self.config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
    def generate_prosora_content(self, insights: Dict) -> Dict:
        """Generate content based on AI insights"""
        print("✍️ Generating Prosora-branded content...")
        
        generated_content = {
            "linkedin_posts": self._generate_linkedin_posts(insights),
            "twitter_threads": self._generate_twitter_threads(insights),
            "blog_outlines": self._generate_blog_outlines(insights),
            "prosora_predictions": self._generate_prosora_predictions(insights),
            "generated_at": datetime.now().isoformat()
        }
        
        # Save generated content
        with open("data/generated_content.json", "w") as f:
            json.dump(generated_content, f, indent=2)
            
        return generated_content
    
    def _generate_linkedin_posts(self, insights: Dict) -> List[Dict]:
        """Generate LinkedIn thought leadership posts"""
        posts = []
        
        # Generate from cross-domain connections
        for connection in insights.get("cross_domain_connections", [])[:2]:
            prompt = f"""
            Write a LinkedIn post for Akash (IIT Bombay engineer, political consultant, product ops lead, FinTech MBA student) based on this insight:
            
            Connection: {connection.get('title', '')}
            Insight: {connection.get('insight', '')}
            Hook: {connection.get('hook', '')}
            
            Style: Professional thought leadership, personal experience, actionable insights
            Length: 200-300 words
            Include: Personal anecdote, data point, call-to-action
            Tone: Confident but approachable, showing cross-domain expertise
            
            Start with a hook, share the insight, add personal context, end with engagement question.
            """
            
            try:
                response = self.model.generate_content(prompt)
                
                posts.append({
                    "type": "cross_domain_insight",
                    "content": response.text,
                    "source_insight": connection,
                    "platform": "linkedin"
                })
                
            except Exception as e:
                print(f"Error generating LinkedIn post: {e}")
        
        # Generate from contrarian takes
        for take in insights.get("contrarian_opportunities", [])[:1]:
            prompt = f"""
            Write a LinkedIn post presenting this contrarian take professionally:
            
            Take: {take.get('statement', '')}
            Evidence: {take.get('evidence', '')}
            
            Style: Thought-provoking but professional, backed by data
            Include personal perspective from your diverse background
            End with discussion question: {take.get('discussion_starter', '')}
            """
            
            try:
                response = self.model.generate_content(prompt)
                
                posts.append({
                    "type": "contrarian_take",
                    "content": response.text,
                    "source_insight": take,
                    "platform": "linkedin"
                })
                
            except Exception as e:
                print(f"Error generating contrarian LinkedIn post: {e}")
                
        return posts
    
    def _generate_twitter_threads(self, insights: Dict) -> List[Dict]:
        """Generate Twitter thread content"""
        threads = []
        
        for connection in insights.get("cross_domain_connections", [])[:1]:
            prompt = f"""
            Create a viral Twitter thread (6-8 tweets) about:
            {connection.get('insight', '')}
            
            Thread Strategy:
            - Hook: Start with surprising/contrarian statement
            - Story: Personal anecdote from IIT/consulting/MBA background
            - Framework: Your unique cross-domain methodology
            - Proof: Add credibility with specific examples
            - CTA: End with engagement question
            
            Format EXACTLY as:
            1/8 [Hook tweet with emoji]
            2/8 [Story/context]
            3/8 [Framework insight]
            4/8 [Cross-domain analysis]
            5/8 [Specific example]
            6/8 [Personal experience]
            7/8 [Broader implications]
            8/8 [Question for engagement]
            
            Each tweet max 280 characters. Use emojis strategically but sparingly.
            Reference your IIT/political consulting/product ops/FinTech MBA background naturally.
            """
            
            try:
                response = self.model.generate_content(prompt)
                
                thread_content = response.text
                tweets = self._parse_thread(thread_content)
                
                threads.append({
                    "type": "insight_thread",
                    "tweets": tweets,
                    "source_insight": connection,
                    "platform": "twitter"
                })
                
            except Exception as e:
                print(f"Error generating Twitter thread: {e}")
                
        return threads
    
    def _generate_blog_outlines(self, insights: Dict) -> List[Dict]:
        """Generate blog post outlines"""
        outlines = []
        
        # Generate "The Prosora Framework" series
        frameworks = [
            "The Political Product Manager: Campaign Strategies for Product Launches",
            "FinTech Democracy: How Financial Inclusion Mirrors Political Representation",
            "The IIT-MBA Bridge: Technical Concepts for Business Leaders"
        ]
        
        for framework in frameworks:
            prompt = f"""
            Create a detailed blog post outline for: "{framework}"
            
            Author background: IIT engineer + political consultant + product ops + FinTech MBA
            
            Include:
            - Compelling introduction with personal anecdote
            - 3-4 main sections with subpoints
            - Real examples from each domain
            - Actionable framework/methodology
            - Conclusion with call-to-action
            
            Target: 1500-2000 words, thought leadership piece
            """
            
            try:
                response = self.model.generate_content(prompt)
                
                outlines.append({
                    "title": framework,
                    "outline": response.text,
                    "type": "prosora_framework",
                    "estimated_words": "1500-2000"
                })
                
            except Exception as e:
                print(f"Error generating blog outline: {e}")
                
        return outlines
    
    def _generate_prosora_predictions(self, insights: Dict) -> List[Dict]:
        """Generate weekly Prosora predictions"""
        predictions = []
        
        prosora_signals = insights.get("prosora_index_signals", {})
        trending_intersections = insights.get("trending_intersections", [])
        
        prompt = f"""
        Based on current signals:
        - Tech Innovation: {prosora_signals.get('tech_innovation', 0)}/100
        - Political Stability: {prosora_signals.get('political_stability', 0)}/100  
        - Market Opportunity: {prosora_signals.get('market_opportunity', 0)}/100
        - Social Impact: {prosora_signals.get('social_impact', 0)}/100
        
        Trending intersections: {', '.join(trending_intersections[:3])}
        
        Generate 3 predictions for the next week combining these domains.
        Format each as:
        - Prediction: [specific, measurable prediction]
        - Confidence: [High/Medium/Low]
        - Rationale: [why this will happen]
        - Watch for: [specific indicators]
        """
        
        try:
            response = self.model.generate_content(prompt)
            
            predictions_text = response.text
            predictions = self._parse_predictions(predictions_text)
            
        except Exception as e:
            print(f"Error generating predictions: {e}")
            
        return predictions
    
    def _parse_thread(self, thread_text: str) -> List[str]:
        """Parse thread text into individual tweets"""
        tweets = []
        lines = thread_text.split('\n')
        
        for line in lines:
            line = line.strip()
            if line and ('/' in line):
                # Look for patterns like "1/8", "2/8", etc.
                parts = line.split(' ', 1)
                if len(parts) > 1 and '/' in parts[0]:
                    tweet_content = parts[1].strip()
                    if tweet_content and len(tweet_content) <= 280:
                        tweets.append(tweet_content)
            elif line and line.startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.')):
                # Handle numbered format
                tweet = line.split('.', 1)[-1].strip()
                if tweet and len(tweet) <= 280:
                    tweets.append(tweet)
                    
        return tweets
    
    def _parse_predictions(self, predictions_text: str) -> List[Dict]:
        """Parse predictions from AI response"""
        predictions = []
        lines = predictions_text.split('\n')
        current_prediction = {}
        
        for line in lines:
            line = line.strip()
            if line.startswith('- Prediction:'):
                if current_prediction:
                    predictions.append(current_prediction)
                current_prediction = {"prediction": line.replace('- Prediction:', '').strip()}
            elif line.startswith('- Confidence:'):
                current_prediction["confidence"] = line.replace('- Confidence:', '').strip()
            elif line.startswith('- Rationale:'):
                current_prediction["rationale"] = line.replace('- Rationale:', '').strip()
            elif line.startswith('- Watch for:'):
                current_prediction["indicators"] = line.replace('- Watch for:', '').strip()
                
        if current_prediction:
            predictions.append(current_prediction)
            
        return predictions

if __name__ == "__main__":
    generator = ContentGenerator()
    
    # Load insights
    with open("data/content_analysis.json", "r") as f:
        insights = json.load(f)
        
    content = generator.generate_prosora_content(insights)