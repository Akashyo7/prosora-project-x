#!/usr/bin/env python3
"""
Enhanced Personalization Controls for Prosora Intelligence Engine
Comprehensive user control system for all 5 phases
"""

import streamlit as st
import json
import yaml
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class UserProfile:
    """Complete user personalization profile"""
    # Identity
    name: str
    role: str
    industry: str
    expertise_level: str
    
    # Voice & Style
    voice_style: str
    tone_preference: str
    complexity_level: str
    content_preference: str
    risk_tolerance: str
    
    # Source Preferences
    source_priorities: Dict[str, float]
    freshness_weight: float
    credibility_threshold: float
    geographic_focus: str
    
    # Generation Settings
    output_length: str
    evidence_requirement: str
    contrarian_factor: float
    personalization_strength: float
    
    # Optimization Settings
    ab_testing_enabled: bool
    preferred_variants: List[str]
    engagement_goals: List[str]
    learning_speed: float
    
    # Metadata
    created_at: datetime
    last_updated: datetime
    usage_count: int

class PersonalizationControlCenter:
    """Advanced control center for user personalization"""
    
    def __init__(self):
        self.initialize_session_state()
    
    def initialize_session_state(self):
        """Initialize all session state variables"""
        if 'user_profile' not in st.session_state:
            st.session_state.user_profile = self.get_default_profile()
        if 'active_preset' not in st.session_state:
            st.session_state.active_preset = "Custom"
        if 'show_advanced' not in st.session_state:
            st.session_state.show_advanced = False
    
    def get_default_profile(self) -> UserProfile:
        """Create default user profile"""
        return UserProfile(
            name="User",
            role="Content Creator",
            industry="Technology",
            expertise_level="Intermediate",
            voice_style="Professional",
            tone_preference="Balanced",
            complexity_level="Moderate",
            content_preference="Analytical",
            risk_tolerance="Balanced",
            source_priorities={
                "stratechery": 0.9,
                "techcrunch": 0.8,
                "hacker_news": 0.7,
                "reuters": 0.8,
                "bloomberg": 0.9
            },
            freshness_weight=0.7,
            credibility_threshold=0.6,
            geographic_focus="Global",
            output_length="Medium",
            evidence_requirement="Moderate",
            contrarian_factor=0.3,
            personalization_strength=0.7,
            ab_testing_enabled=True,
            preferred_variants=["analytical", "engaging"],
            engagement_goals=["likes", "comments"],
            learning_speed=0.5,
            created_at=datetime.now(),
            last_updated=datetime.now(),
            usage_count=0
        )
    
    def render_smart_presets(self):
        """Render smart preset selection"""
        st.subheader("🎯 Smart Presets")
        
        presets = {
            "Thought Leader": {
                "description": "High-impact, contrarian insights for industry leadership",
                "settings": {
                    "voice_style": "Thought Leader",
                    "complexity_level": "Expert",
                    "contrarian_factor": 0.8,
                    "evidence_requirement": "Heavy",
                    "risk_tolerance": "Bold"
                }
            },
            "Viral Content": {
                "description": "Engaging, shareable content optimized for reach",
                "settings": {
                    "voice_style": "Engaging",
                    "content_preference": "Story-Driven",
                    "contrarian_factor": 0.4,
                    "engagement_goals": ["likes", "shares", "saves"]
                }
            },
            "Research Mode": {
                "description": "Deep, evidence-based analysis for professionals",
                "settings": {
                    "voice_style": "Academic",
                    "complexity_level": "Expert",
                    "evidence_requirement": "Academic",
                    "output_length": "Long"
                }
            },
            "Quick Insights": {
                "description": "Fast, digestible insights for busy professionals",
                "settings": {
                    "voice_style": "Professional",
                    "output_length": "Short",
                    "complexity_level": "Simple",
                    "freshness_weight": 0.9
                }
            }
        }
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            selected_preset = st.selectbox(
                "Choose a preset:",
                ["Custom"] + list(presets.keys()),
                key="preset_selector"
            )
        
        with col2:
            if st.button("Apply Preset", disabled=(selected_preset == "Custom")):
                if selected_preset in presets:
                    self.apply_preset(presets[selected_preset]["settings"])
                    st.success(f"Applied {selected_preset} preset!")
                    st.rerun()
        
        if selected_preset != "Custom" and selected_preset in presets:
            st.info(f"📝 {presets[selected_preset]['description']}")
        
        st.session_state.active_preset = selected_preset
    
    def render_voice_style_controls(self):
        """Render voice and style personalization controls"""
        st.subheader("🎭 Voice & Style")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.session_state.user_profile.voice_style = st.selectbox(
                "Voice Style:",
                ["Professional", "Casual", "Thought Leader", "Contrarian", "Academic", "Engaging"],
                index=["Professional", "Casual", "Thought Leader", "Contrarian", "Academic", "Engaging"].index(
                    st.session_state.user_profile.voice_style
                )
            )
            
            st.session_state.user_profile.tone_preference = st.selectbox(
                "Tone:",
                ["Formal", "Balanced", "Conversational", "Bold", "Analytical"],
                index=["Formal", "Balanced", "Conversational", "Bold", "Analytical"].index(
                    st.session_state.user_profile.tone_preference
                )
            )
        
        with col2:
            st.session_state.user_profile.complexity_level = st.selectbox(
                "Complexity Level:",
                ["Simple", "Moderate", "Advanced", "Expert"],
                index=["Simple", "Moderate", "Advanced", "Expert"].index(
                    st.session_state.user_profile.complexity_level
                )
            )
            
            st.session_state.user_profile.content_preference = st.selectbox(
                "Content Style:",
                ["Data-Heavy", "Story-Driven", "Analytical", "Engaging", "Contrarian"],
                index=["Data-Heavy", "Story-Driven", "Analytical", "Engaging", "Contrarian"].index(
                    st.session_state.user_profile.content_preference
                )
            )
        
        with col3:
            st.session_state.user_profile.risk_tolerance = st.selectbox(
                "Risk Tolerance:",
                ["Conservative", "Balanced", "Bold", "Contrarian"],
                index=["Conservative", "Balanced", "Bold", "Contrarian"].index(
                    st.session_state.user_profile.risk_tolerance
                )
            )
            
            st.session_state.user_profile.personalization_strength = st.slider(
                "Personalization Strength:",
                0.0, 1.0, st.session_state.user_profile.personalization_strength, 0.1,
                help="How strongly to apply your personal voice"
            )
    
    def render_source_controls(self):
        """Render source management controls"""
        st.subheader("📰 Source Management")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Source Priorities:**")
            sources = ["stratechery", "techcrunch", "hacker_news", "reuters", "bloomberg", "wsj", "ft"]
            
            for source in sources:
                current_priority = st.session_state.user_profile.source_priorities.get(source, 0.5)
                st.session_state.user_profile.source_priorities[source] = st.slider(
                    f"{source.title()}:",
                    0.0, 1.0, current_priority, 0.1,
                    key=f"source_{source}"
                )
        
        with col2:
            st.session_state.user_profile.freshness_weight = st.slider(
                "Freshness Weight:",
                0.0, 1.0, st.session_state.user_profile.freshness_weight, 0.1,
                help="How much to prioritize recent content"
            )
            
            st.session_state.user_profile.credibility_threshold = st.slider(
                "Credibility Threshold:",
                0.0, 1.0, st.session_state.user_profile.credibility_threshold, 0.1,
                help="Minimum credibility score for sources"
            )
            
            st.session_state.user_profile.geographic_focus = st.selectbox(
                "Geographic Focus:",
                ["Global", "North America", "Europe", "Asia", "US Only"],
                index=["Global", "North America", "Europe", "Asia", "US Only"].index(
                    st.session_state.user_profile.geographic_focus
                )
            )
    
    def render_generation_controls(self):
        """Render content generation controls"""
        st.subheader("⚙️ Generation Settings")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.session_state.user_profile.output_length = st.selectbox(
                "Output Length:",
                ["Short", "Medium", "Long", "Custom"],
                index=["Short", "Medium", "Long", "Custom"].index(
                    st.session_state.user_profile.output_length
                )
            )
            
            st.session_state.user_profile.evidence_requirement = st.selectbox(
                "Evidence Level:",
                ["Light", "Moderate", "Heavy", "Academic"],
                index=["Light", "Moderate", "Heavy", "Academic"].index(
                    st.session_state.user_profile.evidence_requirement
                )
            )
        
        with col2:
            st.session_state.user_profile.contrarian_factor = st.slider(
                "Contrarian Factor:",
                0.0, 1.0, st.session_state.user_profile.contrarian_factor, 0.1,
                help="How contrarian/provocative to make insights"
            )
        
        with col3:
            # Real-time preview of settings impact
            st.write("**Settings Impact:**")
            impact_score = self.calculate_settings_impact()
            st.metric("Uniqueness Score", f"{impact_score['uniqueness']:.2f}")
            st.metric("Engagement Potential", f"{impact_score['engagement']:.2f}")
            st.metric("Authority Level", f"{impact_score['authority']:.2f}")
    
    def render_optimization_controls(self):
        """Render optimization and learning controls"""
        st.subheader("🚀 Optimization & Learning")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.session_state.user_profile.ab_testing_enabled = st.checkbox(
                "Enable A/B Testing",
                value=st.session_state.user_profile.ab_testing_enabled
            )
            
            if st.session_state.user_profile.ab_testing_enabled:
                available_variants = ["analytical", "engaging", "contrarian", "data_driven", "storytelling"]
                st.session_state.user_profile.preferred_variants = st.multiselect(
                    "Preferred Variants:",
                    available_variants,
                    default=st.session_state.user_profile.preferred_variants
                )
        
        with col2:
            engagement_options = ["likes", "comments", "shares", "saves", "clicks", "reach"]
            st.session_state.user_profile.engagement_goals = st.multiselect(
                "Engagement Goals:",
                engagement_options,
                default=st.session_state.user_profile.engagement_goals
            )
            
            st.session_state.user_profile.learning_speed = st.slider(
                "Learning Speed:",
                0.0, 1.0, st.session_state.user_profile.learning_speed, 0.1,
                help="How quickly to adapt from feedback"
            )
    
    def render_profile_management(self):
        """Render profile save/load/share functionality"""
        st.subheader("👤 Profile Management")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("💾 Save Profile"):
                self.save_profile()
                st.success("Profile saved!")
        
        with col2:
            if st.button("📤 Export Profile"):
                profile_json = self.export_profile()
                st.download_button(
                    "Download Profile",
                    profile_json,
                    file_name=f"prosora_profile_{datetime.now().strftime('%Y%m%d')}.json",
                    mime="application/json"
                )
        
        with col3:
            uploaded_file = st.file_uploader("📥 Import Profile", type="json")
            if uploaded_file:
                self.import_profile(uploaded_file)
                st.success("Profile imported!")
                st.rerun()
        
        with col4:
            if st.button("🔄 Reset to Default"):
                st.session_state.user_profile = self.get_default_profile()
                st.success("Profile reset!")
                st.rerun()
    
    def apply_preset(self, settings: Dict):
        """Apply preset settings to user profile"""
        for key, value in settings.items():
            if hasattr(st.session_state.user_profile, key):
                setattr(st.session_state.user_profile, key, value)
        st.session_state.user_profile.last_updated = datetime.now()
    
    def calculate_settings_impact(self) -> Dict[str, float]:
        """Calculate impact of current settings"""
        profile = st.session_state.user_profile
        
        # Calculate uniqueness based on contrarian factor and risk tolerance
        uniqueness = (profile.contrarian_factor * 0.6 + 
                     (0.8 if profile.risk_tolerance in ["Bold", "Contrarian"] else 0.3))
        
        # Calculate engagement potential
        engagement = (0.8 if profile.content_preference in ["Story-Driven", "Engaging"] else 0.5) * \
                    (profile.personalization_strength * 0.7 + 0.3)
        
        # Calculate authority level
        authority = (0.9 if profile.evidence_requirement in ["Heavy", "Academic"] else 0.5) * \
                   (0.8 if profile.complexity_level in ["Advanced", "Expert"] else 0.4)
        
        return {
            "uniqueness": min(uniqueness, 1.0),
            "engagement": min(engagement, 1.0),
            "authority": min(authority, 1.0)
        }
    
    def save_profile(self):
        """Save current profile to session state"""
        st.session_state.user_profile.last_updated = datetime.now()
        st.session_state.user_profile.usage_count += 1
    
    def export_profile(self) -> str:
        """Export profile as JSON string"""
        profile_dict = asdict(st.session_state.user_profile)
        # Convert datetime objects to strings
        profile_dict['created_at'] = profile_dict['created_at'].isoformat()
        profile_dict['last_updated'] = profile_dict['last_updated'].isoformat()
        return json.dumps(profile_dict, indent=2)
    
    def import_profile(self, uploaded_file):
        """Import profile from uploaded JSON file"""
        try:
            profile_data = json.load(uploaded_file)
            # Convert datetime strings back to datetime objects
            profile_data['created_at'] = datetime.fromisoformat(profile_data['created_at'])
            profile_data['last_updated'] = datetime.fromisoformat(profile_data['last_updated'])
            
            st.session_state.user_profile = UserProfile(**profile_data)
        except Exception as e:
            st.error(f"Error importing profile: {str(e)}")
    
    def render_complete_control_center(self):
        """Render the complete personalization control center"""
        st.title("🎛️ Prosora Personalization Control Center")
        
        # Toggle for advanced controls
        st.session_state.show_advanced = st.toggle(
            "Show Advanced Controls", 
            value=st.session_state.show_advanced
        )
        
        # Smart presets (always visible)
        self.render_smart_presets()
        
        st.divider()
        
        # Core controls
        self.render_voice_style_controls()
        
        if st.session_state.show_advanced:
            st.divider()
            self.render_source_controls()
            
            st.divider()
            self.render_generation_controls()
            
            st.divider()
            self.render_optimization_controls()
        
        st.divider()
        self.render_profile_management()
        
        # Real-time configuration summary
        with st.expander("📋 Current Configuration Summary"):
            self.render_config_summary()
    
    def render_config_summary(self):
        """Render a summary of current configuration"""
        profile = st.session_state.user_profile
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Voice & Style:**")
            st.write(f"- Style: {profile.voice_style}")
            st.write(f"- Tone: {profile.tone_preference}")
            st.write(f"- Complexity: {profile.complexity_level}")
            st.write(f"- Content: {profile.content_preference}")
            
            st.write("**Generation:**")
            st.write(f"- Length: {profile.output_length}")
            st.write(f"- Evidence: {profile.evidence_requirement}")
            st.write(f"- Contrarian: {profile.contrarian_factor:.1f}")
        
        with col2:
            st.write("**Sources:**")
            top_sources = sorted(profile.source_priorities.items(), 
                               key=lambda x: x[1], reverse=True)[:3]
            for source, priority in top_sources:
                st.write(f"- {source.title()}: {priority:.1f}")
            
            st.write("**Optimization:**")
            st.write(f"- A/B Testing: {'✅' if profile.ab_testing_enabled else '❌'}")
            st.write(f"- Learning Speed: {profile.learning_speed:.1f}")
            st.write(f"- Goals: {', '.join(profile.engagement_goals[:2])}")

# Usage example
if __name__ == "__main__":
    control_center = PersonalizationControlCenter()
    control_center.render_complete_control_center()