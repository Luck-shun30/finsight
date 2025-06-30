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
        # main_page() will be added later
        pass
    elif page == "👕 Wardrobe":
        # wardrobe_page() will be added later
        pass
    elif page == "🎨 Outfit Generator":
        # outfit_generator_page() will be added later
        pass
    elif page == "📅 History":
        # outfit_history_page() will be added later
        pass
    elif page == "⚙️ Settings":
        # settings_page() will be added later
        pass

if __name__ == "__main__":
    main()