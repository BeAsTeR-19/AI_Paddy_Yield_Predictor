import streamlit as st


def apply_agri_theme():
    st.markdown("""
        <style>
        /* 1. Global Visibility Fix */
        .stApp {
            background-color: #f8faf8 !important;
        }

        /* Force dark text on the light background */
        h1, h2, h3, p, span, label, .stMarkdown {
            color: #1b331b !important;
            font-weight: 600 !important;
        }

        /* 2. Professional Sidebar */
        [data-testid="stSidebar"] {
            background-color: #0d1a0d !important;
            border-right: 2px solid #2e7d32;
        }
        [data-testid="stSidebar"] * {
            color: #ffffff !important;
        }

        /* 3. The Status Light Glow Fix */
        /* Fixed 'invalid decimal literal' by adding 'px' to all values */
        span:contains("🟢") {
            color: #4caf50;
            text-shadow: 0px 0px 8px rgba(76, 175, 80, 0.4);
        }
        span:contains("🟠") {
            color: #ff9800;
            text-shadow: 0px 0px 8px rgba(255, 152, 0, 0.4);
        }

        /* 4. The Button */
        .stButton>button {
            background: linear-gradient(90deg, #1b5e20 0%, #43a047 100%) !important;
            color: white !important;
            border-radius: 50px !important;
            border: none !important;
            font-weight: 700 !important;
            width: 100%;
        }
        </style>
    """, unsafe_allow_html=True)