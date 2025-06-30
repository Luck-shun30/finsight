import streamlit as st
import json
import os
from datetime import datetime, timedelta
from PIL import Image
import tempfile
from src.FitIdentification import image_to_json, add_to_wardrobe
from src.Wardrobe import OutfitSuggestionCrew

# Page configuration
st.set_page_config(
    page_title="Shipwrecked Outfit Suggestion",
    page_icon="👕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main navigation
def main():
    # Sidebar navigation
    st.sidebar.title("👕 Shipwrecked")
    st.sidebar.write("Your AI-powered wardrobe assistant")
    
    # Navigation
    page = st.sidebar.selectbox(
        "Navigate",
        ["🏠 Dashboard", "👕 Wardrobe", "🎨 Outfit Generator", "📅 History", "⚙️ Settings"]
    )
    
    # Display selected page
    if page == "🏠 Dashboard":
        
        pass
    elif page == "👕 Wardrobe":
        
        pass
    elif page == "🎨 Outfit Generator":
        
        pass
    elif page == "📅 History":
        
        pass
    elif page == "⚙️ Settings":
        
        pass

if __name__ == "__main__":
    main()

# Initialize session state
if 'user_settings' not in st.session_state:
    st.session_state.user_settings = {
        'name': 'User',
        'laundry_cycle_days': 7,
        'location': 'Chicago, US',
        'preferred_formality': 'Casual',
        'preferred_activity': 'General'
    }

if 'wardrobe_items' not in st.session_state:
    try:
        with open("data/wardrobe.json", "r") as f:
            wardrobe_data = json.load(f)
            st.session_state.wardrobe_items = wardrobe_data["items"]
    except FileNotFoundError:
        st.session_state.wardrobe_items = []

if 'outfit_history' not in st.session_state:
    st.session_state.outfit_history = []

def save_user_settings():
    """Save user settings to a JSON file"""
    with open("data/user_settings.json", "w") as f:
        json.dump(st.session_state.user_settings, f, indent=2)

def load_user_settings():
    """Load user settings from JSON file"""
    try:
        with open("data/user_settings.json", "r") as f:
            st.session_state.user_settings = json.load(f)
    except FileNotFoundError:
        pass

def save_wardrobe():
    """Save wardrobe items to JSON file"""
    wardrobe_data = {"items": st.session_state.wardrobe_items}
    with open("data/wardrobe.json", "w") as f:
        json.dump(wardrobe_data, f, indent=2)