"""
Gemini-Optimized Prompts and Features
Leverages Gemini's strengths: reasoning, multimodal, long context
"""

import google.generativeai as genai
from typing import Dict, List
from config import Config

class GeminiOptimizer:
    def __init__(self):
        self.config = Config()
        genai.configure(api_key=self.config.GEMINI_API_KEY)
        
        # Use different models for different tasks
        self.flash_model = genai.GenerativeModel('gemini-1.5-flash')  # Fast, efficient
        self.pro_model = genai.GenerativeModel('gemini-1.5-pro')     # Complex reasoning
        
    def enhanced_cross_domain_analysis(self, content_text: str) -> List[Dict]:
        """Leverage Gemini's reasoning for deeper cross-domain insights"""
        
        prompt = f"""
        You are Akash - an IIT Bombay engineer turned political consultant, now a product operations lead pursuing FinTech MBA. 
        
        Your unique perspective combines:
        - Technical depth from premier engineering education
        - Political strategy from campaign consulting
        - Product execution from operations leadership  
        - Financial innovation from FinTech studies
        
        Analyze this content and find 3 NON-OBVIOUS connections that only someone with your background would see:
        
        {content_text[:4000]}
        
        For each connection, think step-by-step:
        1. What pattern do you see across domains?
        2. Why would others miss this connection?
        3. What's your contrarian take?
        4. How does this create content opportunity?
        
        Format each as:
        **Connection [X]: [Catchy Title]**
        - **Cross-Domain Pattern**: [What you see that others don't]
        - **Why Others Miss It**: [Blind spots in single-domain thinking]  
        - **Your Contrarian Take**: [Provocative but defensible position]
        - **Content Hook**: [Viral social media angle]
        - **Evidence**: [Specific data points from content]
        """
        
        try:
            response = self.pro_model.generate_content(prompt)
            return self._parse_enhanced_connections(response.text)
        except Exception as e:
            print(f"Error in enhanced analysis: {e}")
            return []
    
    def generate_prosora_framework_content(self, topic: str, insights: List[Dict]) -> Dict:
        """Generate signature 'Prosora Framework' content"""
        
        prompt = f"""
        Create a "Prosora Framework" post about: {topic}
        
        You are Akash - the cross-domain expert who sees patterns others miss.
        
        Your signature style:
        - Start with a contrarian observation
        - Use the "3-2-1 Framework" (3 insights, 2 examples, 1 action)
        - Reference your diverse background naturally
        - End with a thought-provoking question
        
        Insights to weave in: {insights}
        
        Structure:
        🧠 **The Prosora Take**: [Contrarian opening]
        
        📊 **The 3-2-1 Framework**:
        
        **3 Cross-Domain Insights:**
        1. [Tech perspective]
        2. [Political/strategy perspective]  
        3. [Product/business perspective]
        
        **2 Real Examples:**
        - [Example from your experience/observation]
        - [Current market example]
        
        **1 Action Item:**
        [Specific, actionable advice]
        
        💭 **Question for you**: [Engagement driver]
        
        Tone: Confident but approachable, data-driven, personally authentic
        Length: 250-300 words for LinkedIn
        """
        
        try:
            response = self.flash_model.generate_content(prompt)
            return {
                "type": "prosora_framework",
                "content": response.text,
                "topic": topic,
                "format": "linkedin_signature"
            }
        except Exception as e:
            print(f"Error generating framework content: {e}")
            return {}
    
    def create_viral_twitter_thread(self, insight: Dict) -> List[str]:
        """Create viral Twitter threads using Gemini's understanding of engagement"""
        
        prompt = f"""
        Create a viral Twitter thread based on this insight:
        {insight}
        
        Thread Strategy:
        - Hook: Start with a surprising statistic or contrarian statement
        - Story: Use personal anecdote or case study
        - Framework: Present your unique methodology
        - Proof: Add credibility with your background
        - CTA: End with engagement question
        
        Rules:
        - Each tweet max 280 characters
        - Use emojis strategically (not overuse)
        - Include line breaks for readability
        - Thread should be 6-8 tweets
        - Make it shareable and quotable
        
        Your background to reference:
        - IIT Bombay (technical credibility)
        - Political consulting (strategy insights)
        - Product ops (execution experience)
        - FinTech MBA (market understanding)
        
        Format as:
        1/8 [Hook tweet]
        2/8 [Story/context]
        ...
        8/8 [CTA/question]
        """
        
        try:
            response = self.flash_model.generate_content(prompt)
            return self._parse_twitter_thread(response.text)
        except Exception as e:
            print(f"Error creating Twitter thread: {e}")
            return []
    
    def generate_weekly_predictions(self, prosora_signals: Dict, trending_topics: List[str]) -> List[Dict]:
        """Generate 'Prosora Predictions' using Gemini's reasoning"""
        
        prompt = f"""
        Generate 3 "Prosora Predictions" for next week based on:
        
        **Current Prosora Index Signals:**
        - Tech Innovation: {prosora_signals.get('tech_innovation', 0)}/100
        - Political Stability: {prosora_signals.get('political_stability', 0)}/100
        - Market Opportunity: {prosora_signals.get('market_opportunity', 0)}/100
        - Social Impact: {prosora_signals.get('social_impact', 0)}/100
        
        **Trending Topics:** {', '.join(trending_topics[:5])}
        
        For each prediction:
        1. Use your cross-domain expertise to see what others miss
        2. Make it specific and measurable
        3. Provide clear reasoning
        4. Include confidence level and what to watch for
        
        Format each as:
        **Prosora Prediction #[X]: [Specific prediction]**
        - **Confidence**: [High/Medium/Low] 
        - **Cross-Domain Logic**: [Why your unique background led to this insight]
        - **What to Watch**: [Specific indicators]
        - **If Right**: [What this means for the market]
        - **If Wrong**: [What we'd learn instead]
        
        Make predictions that showcase your unique perspective across tech, politics, product, and finance.
        """
        
        try:
            response = self.pro_model.generate_content(prompt)
            return self._parse_predictions(response.text)
        except Exception as e:
            print(f"Error generating predictions: {e}")
            return []
    
    def _parse_enhanced_connections(self, text: str) -> List[Dict]:
        """Parse enhanced connection format"""
        connections = []
        sections = text.split("**Connection")
        
        for section in sections[1:]:  # Skip first empty section
            lines = section.strip().split('\n')
            connection = {}
            
            for line in lines:
                if line.startswith('- **Cross-Domain Pattern**:'):
                    connection['pattern'] = line.replace('- **Cross-Domain Pattern**:', '').strip()
                elif line.startswith('- **Why Others Miss It**:'):
                    connection['blind_spots'] = line.replace('- **Why Others Miss It**:', '').strip()
                elif line.startswith('- **Your Contrarian Take**:'):
                    connection['contrarian_take'] = line.replace('- **Your Contrarian Take**:', '').strip()
                elif line.startswith('- **Content Hook**:'):
                    connection['hook'] = line.replace('- **Content Hook**:', '').strip()
                elif line.startswith('- **Evidence**:'):
                    connection['evidence'] = line.replace('- **Evidence**:', '').strip()
            
            if connection:
                connections.append(connection)
                
        return connections
    
    def _parse_twitter_thread(self, text: str) -> List[str]:
        """Parse Twitter thread format"""
        tweets = []
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            if line and ('/' in line and line.split('/')[0].isdigit()):
                # Extract tweet content after the numbering
                tweet_content = line.split(' ', 1)[1] if ' ' in line else line
                if len(tweet_content) <= 280:
                    tweets.append(tweet_content)
                    
        return tweets
    
    def _parse_predictions(self, text: str) -> List[Dict]:
        """Parse prediction format"""
        predictions = []
        sections = text.split("**Prosora Prediction")
        
        for section in sections[1:]:
            lines = section.strip().split('\n')
            prediction = {}
            
            for line in lines:
                if line.startswith('- **Confidence**:'):
                    prediction['confidence'] = line.replace('- **Confidence**:', '').strip()
                elif line.startswith('- **Cross-Domain Logic**:'):
                    prediction['logic'] = line.replace('- **Cross-Domain Logic**:', '').strip()
                elif line.startswith('- **What to Watch**:'):
                    prediction['indicators'] = line.replace('- **What to Watch**:', '').strip()
                elif line.startswith('- **If Right**:'):
                    prediction['if_right'] = line.replace('- **If Right**:', '').strip()
                elif line.startswith('- **If Wrong**:'):
                    prediction['if_wrong'] = line.replace('- **If Wrong**:', '').strip()
            
            if prediction:
                predictions.append(prediction)
                
        return predictions