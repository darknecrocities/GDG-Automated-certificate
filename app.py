import streamlit as st
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import os
import io
import zipfile
import random
from officers_data import OFFICERS, QUOTES
import base64
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="GDG-HAU | Certificate Generator",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Futuristic UI
def local_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');

    :root {
        --primary: #4285F4;
        --secondary: #9b51e0;
        --accent: #00f2fe;
        --bg: #0E1117;
        --glass: rgba(255, 255, 255, 0.05);
        --glass-border: rgba(255, 255, 255, 0.1);
    }

    * {
        font-family: 'Inter', sans-serif;
    }

    .main {
        background-color: var(--bg);
        background-image: 
            radial-gradient(circle at 10% 20%, rgba(66, 133, 244, 0.05) 0%, transparent 40%),
            radial-gradient(circle at 90% 80%, rgba(155, 81, 224, 0.05) 0%, transparent 40%);
    }

    /* Glassmorphism Card */
    .glass-card {
        background: var(--glass);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid var(--glass-border);
        padding: 2rem;
        margin-bottom: 2rem;
        transition: all 0.3s ease;
    }

    .glass-card:hover {
        border: 1px solid rgba(66, 133, 244, 0.3);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        transform: translateY(-5px);
    }

    /* Animated Gradient Text */
    .gradient-text {
        background: linear-gradient(90deg, #4285F4, #9b51e0, #00f2fe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 3.5rem;
        margin-bottom: 1rem;
        animation: gradient-shift 5s infinite linear;
        background-size: 200% auto;
    }

    @keyframes gradient-shift {
        0% { background-position: 0% center; }
        100% { background-position: 200% center; }
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: rgba(10, 10, 15, 0.95);
        border-right: 1px solid var(--glass-border);
    }

    /* Custom Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #4285F4, #9b51e0);
        color: white;
        border: none;
        padding: 0.6rem 2rem;
        border-radius: 50px;
        font-weight: 600;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 20px rgba(66, 133, 244, 0.4);
    }

    /* Quote Card */
    .quote-card {
        border-left: 4px solid var(--primary);
        background: rgba(66, 133, 244, 0.1);
        padding: 1.5rem;
        border-radius: 0 15px 15px 0;
        font-style: italic;
        font-size: 1.2rem;
        margin: 2rem 0;
    }

    /* Metrics */
    [data-testid="stMetricValue"] {
        color: var(--accent);
        font-weight: 800;
    }

    /* Success Toast Animation */
    @keyframes slide-in {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }

    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    ::-webkit-scrollbar-track {
        background: var(--bg);
    }
    ::-webkit-scrollbar-thumb {
        background: var(--glass-border);
        border-radius: 10px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: var(--primary);
    }
    </style>
    """, unsafe_allow_html=True)

local_css()

# Helper function to get binary of image for base64
def get_image_base64(path):
    with open(path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Certificate Generation Logic
def generate_certificate(name, role, date):
    template_path = "Template.png"
    if not os.path.exists(template_path):
        st.error("Template.png not found!")
        return None

    img = Image.open(template_path)
    draw = ImageDraw.Draw(img)
    
    # ==========================================
    # FONT SIZE CONFIGURATION (Adjust here)
    # ==========================================
    BOLD_SIZE = 45    # Font size for the Officer Name
    REGULAR_SIZE = 35  # Font size for the Position/Role
    # ==========================================
    
    font_bold_path = "assets/fonts/Inter-Bold.ttf"
    font_regular_path = "assets/fonts/Inter-Regular.ttf"
    
    # Fallback paths for different OS environments (Streamlit Cloud uses Linux)
    # 1. Mac Paths
    mac_bold = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
    mac_regular = "/System/Library/Fonts/Supplemental/Arial.ttf"
    
    # 2. Linux Paths (Streamlit Cloud / Debian)
    linux_bold = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    linux_regular = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    
    # 3. Alternative Linux Paths
    linux_bold_alt = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
    linux_regular_alt = "/usr/share/fonts/truetype/liberation/LiberationSans.ttf"
    
    def load_font(path, size, fallbacks):
        try:
            # Try local file first
            return ImageFont.truetype(path, size)
        except:
            for fallback in fallbacks:
                try:
                    return ImageFont.truetype(fallback, size)
                except:
                    continue
            # Absolute last resort (will be small)
            return ImageFont.load_default()

    font_bold = load_font(font_bold_path, BOLD_SIZE, [mac_bold, linux_bold, linux_bold_alt])
    font_regular = load_font(font_regular_path, REGULAR_SIZE, [mac_regular, linux_regular, linux_regular_alt])
    
    # Dynamic Positioning based on the provided Template.png structure
    W, H = img.size
    
    # Auto-scale Name if too long
    while draw.textbbox((0, 0), name, font=font_bold)[2] > (W * 0.7) and BOLD_SIZE > 40:
        BOLD_SIZE -= 5
        font_bold = load_font(font_bold_path, BOLD_SIZE, mac_bold)
    
    # 1. Name (Centered on the first line)
    draw.text((W / 2, 400), name, fill=(0, 0, 0), font=font_bold, anchor="mm")
    
    # 2. Role (Centered on the second line)
    draw.text((W / 2, 505), role, fill=(0, 0, 0), font=font_regular, anchor="mm")

    return img

# Sidebar Navigation
with st.sidebar:
    st.markdown("<h1 style='color:#4285F4; margin-bottom:0;'>GDG On Campus</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:gray; margin-top:0;'>Holy Angel University</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Simplified menu - only Generator remains
    menu = "Generator"
    
    st.markdown("---")
    st.info("💡 Pro Tip: Use High Quality Export for printing certificates.")


# Generator View
if menu == "Generator":
    st.markdown("<h2 style='color:#4285F4;'>Single Generation</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1.5])
    
    with col1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        search_query = st.text_input("Search Officer", "")
        
        filtered_officers = [o['name'] for o in OFFICERS if search_query.lower() in o['name'].lower()]
        selected_name = st.selectbox("Select Officer", filtered_officers if filtered_officers else ["No results"])
        
        officer_data = next((o for o in OFFICERS if o['name'] == selected_name), None)
        
        if officer_data:
            role = st.text_input("Role", officer_data['role'])
            
            if st.button("Generate Preview"):
                with st.spinner("Rendering cinematic certificate..."):
                    img = generate_certificate(selected_name, role, "")
                    st.session_state['preview_img'] = img
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        if 'preview_img' in st.session_state and st.session_state['preview_img']:
            st.image(st.session_state['preview_img'], use_container_width=True)
            
            # Download button
            buf = io.BytesIO()
            st.session_state['preview_img'].save(buf, format="PNG")
            byte_im = buf.getvalue()
            
            st.download_button(
                label="Download Certificate (PNG)",
                data=byte_im,
                file_name=f"GDGOC_HAU_{selected_name.replace(' ', '_')}.png",
                mime="image/png"
            )
            st.success(f"Certificate for {selected_name} is ready!")
            
            # Message from CEO
            st.markdown(f"""
            <div class='glass-card' style='border-left: 5px solid #4285F4; margin-top: 2rem;'>
                <h4 style='color: #4285F4; margin-bottom: 0.5rem;'>✉️ A Message from Arron Kian Parejas</h4>
                <p style='font-style: italic; color: #E0E0E0; line-height: 1.6;'>
                    "Congratulations on this remarkable achievement! As you hold this certificate, remember that this is just 
                    the beginning of your impact in the tech community. Your dedication, hard work, and commitment to innovation 
                    at <b>Google Developer Groups On Campus - Holy Angel University</b> have been truly inspiring. 
                    You have not only mastered new technologies but have also fostered a community of learning and growth. 
                    As you move forward, keep that same curiosity and passion alive. The road ahead is full of opportunities, 
                    and I have no doubt you will excel in everything you pursue. 
                    <br><br>
                    <b>Goodluck on your next journey</b>, and may you continue to lead with excellence and inspire others along the way!"
                </p>
                <p style='text-align: right; font-weight: bold; color: #4285F4;'>— Arron Kian Parejas, CEO & Lead Organizer</p>
            </div>
            """, unsafe_allow_html=True)



# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 2rem; color: #888;'>
    <p style='font-size: 1.2rem; font-style: italic; color: #4285F4; margin-bottom: 0.5rem;'>
        "The journey doesn't end here; it merely takes a new direction. May the code you've written and the community 
        you've built be the foundation for your greatest achievements yet."
    </p>
    <p style='font-size: 0.9rem; margin-top: 1rem;'>
        Onward to your next big adventure! 🚀
    </p>
    <p style='font-size: 0.7rem; color: #444; margin-top: 2rem;'>
        Built with ❤️ for Google Developer Groups On Campus - Holy Angel University
    </p>
</div>
""", unsafe_allow_html=True)
