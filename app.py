import streamlit as st
import os
from google import genai
from dotenv import load_dotenv

# --- 1. INITIALIZATION ---
load_dotenv()
# Automatically switches between local .env and Streamlit Cloud Secrets
API_KEY = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)

# Initialize Session State for language selection
if 'lang' not in st.session_state:
    st.session_state.lang = None


# --- 2. YOUR ORIGINAL CODE (THE "SAFETY NET") ---
# This ensures the app always works, even on "unbuilt roads" or busy servers.
def get_local_expert_advice(ward, soil, rainfall, lang):
    # Your original yield calculation
    yield_estimate = 3100 + (rainfall * 0.75) + (200 if "Clay" in soil else 0)

    if lang == "Nepali":
        advice = f"**झापा स्थानीय विशेषज्ञ सल्लाह ({ward}):**\n"
        if rainfall > 2200:
            advice += "- धेरै वर्षा हुने सम्भावना छ, निकासको व्यवस्था मिलाउनुहोस्।"
        else:
            advice += "- सिँचाइको उचित व्यवस्था गर्नुहोस्।"
    else:
        advice = f"**Local Expert Advice ({ward}):**\n"
        if rainfall > 2200:
            advice += "- High rainfall expected. Ensure proper field drainage."
        else:
            advice += "- Moderate rainfall. Monitor irrigation during flowering."

    return int(yield_estimate), advice


# --- 3. THE HYBRID AI CONTROLLER ---
def get_final_results(ward, soil, rainfall, lang):
    """Tries AI first. If it's busy or offline, triggers your original code."""
    try:
        # Send to Gemini 1.5 Flash-8B (Highest free tier limits)
        prompt = f"Rice advice for {ward}, Jhapa. Soil: {soil}, Rain: {rainfall}mm. {lang} only."
        response = client.models.generate_content(
            model="gemini-1.5-flash-8b",
            contents=prompt
        )
        # Success path: Use AI text but keep your trusted math for yield
        yield_val = 3100 + (rainfall * 0.78) + (200 if "Clay" in soil else 0)
        return int(yield_val), response.text, "LIVE AI"

    except Exception:
        # Failure path: Instantly run your manual code (User never sees an error)
        y, a = get_local_expert_advice(ward, soil, rainfall, lang)
        return y, a, "LOCAL MODE"


# --- 4. THE USER INTERFACE ---
# PART A: THE LANGUAGE START-SCREEN
if st.session_state.lang is None:
    st.set_page_config(page_title="Jhapa Paddy Advisor", page_icon="🌾")
    st.title("🌾 Jhapa Paddy Advisor")
    st.subheader("Choose Language / भाषा छान्नुहोस्")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("English", use_container_width=True):
            st.session_state.lang = "English"
            st.rerun()
    with col2:
        if st.button("नेपाली", use_container_width=True):
            st.session_state.lang = "Nepali"
            st.rerun()

# PART B: THE MAIN ADVISOR (Shows only after selection)
else:
    # Set titles based on language
    title_text = "🌾 Jhapa Paddy Advisor" if st.session_state.lang == "English" else "🌾 झापा धान सल्लाहकार"
    st.title(title_text)

    with st.sidebar:
        if st.button("Change Language / भाषा फेर्नुहोस्"):
            st.session_state.lang = None
            st.rerun()

        st.header("Settings" if st.session_state.lang == "English" else "सेटिङ")
        ward = st.selectbox("Ward/Location", ["Sanischare", "Jalthal", "Budhabare", "Dhaijan"])
        soil = st.selectbox("Soil Type", ["Clay Loam", "Sandy Loam", "Loam"])
        rainfall = st.slider("Rainfall (mm)", 1500, 3000, 2100)

    # Trigger calculation
    btn_text = "Analyze Results" if st.session_state.lang == "English" else "विश्लेषण गर्नुहोस्"
    if st.button(btn_text):
        with st.spinner("Processing..." if st.session_state.lang == "English" else "प्रक्रिया हुँदैछ..."):
            f_yield, f_advice, mode = get_final_results(ward, soil, rainfall, st.session_state.lang)

            # Display Metric
            y_label = "Estimated Yield" if st.session_state.lang == "English" else "अनुमानित उत्पादन"
            st.metric(y_label, f"{f_yield} kg/ha")

            # System Status Indicator
            if mode == "LIVE AI":
                st.success("🟢 Connected to AI" if st.session_state.lang == "English" else "🟢 एआई जडान भयो")
            else:
                st.warning("🟠 Offline/Busy Mode" if st.session_state.lang == "English" else "🟠 अफलाइन मोड सक्रिय")

            st.info(f_advice)

st.divider()
st.caption("Prototype Jan 2026| Developed by Ujjwal Dhungana| Powered by:gemini-1.5-flash-8b |")