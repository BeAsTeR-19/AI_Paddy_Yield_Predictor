import streamlit as st
import os
import io
import time
import pandas as pd
from gtts import gTTS
from google import genai
from google.api_core import exceptions
from dotenv import load_dotenv
from style_utils import apply_agri_theme

# --- INITIALIZATION ---
load_dotenv()
apply_agri_theme()  # Apply our modern UI
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# --- DATA ---
LOCATION = {
    "Sanischare": {"lat": 26.6853, "lon": 87.9944},
    "Jalthal": {"lat": 26.5458, "lon": 88.0253},
    "Budhabare": {"lat": 26.7328, "lon": 88.0414},
    "Dhaijan": {"lat": 26.6575, "lon": 88.0833},
}

CONTENT = {
    "English": {
        "title": "🌾 Jhapa Paddy Yield Advisor",
        "sidebar_header": "Field Parameters",
        "predict_btn": "Analyze & Speak Advice",
        "result_label": "Predicted Yield",
        "audio_label": "🔊 Listen to Recommendation",
        "lang_code": "en"
    },
    "Nepali": {
        "title": "🌾 झापा धान उत्पादन सल्लाहकार",
        "sidebar_header": "खेतको विवरण",
        "predict_btn": "विश्लेषण र सुझाव सुन्नुहोस्",
        "result_label": "अनुमानित उत्पादन",
        "audio_label": "🔊 सुझाव सुन्नुहोस्",
        "lang_code": "ne"
    }
}


# --- FUNCTIONS ---
def get_ai_advice(prompt):
    """
    Fetches advice from Gemini AI.
    Returns a tuple: (advice_text, is_live_status)
    """
    try:
        # Attempt to get a response from the Gemini 2.0 Flash model
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        return response.text, True  # True means Green Light

    except Exception as e:
        # Fallback triggers for token exhaustion or network issues
        fallback = "The system is busy right now. Note: Rice needs steady water during the flowering stage."
        return fallback, False  # False means Orange Light


def text_to_speech(text, lang):
    tts = gTTS(text=text, lang=lang)
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    return fp.getvalue()


# --- APP FLOW ---
if 'lang' not in st.session_state:
    st.session_state.lang = None

# 1. Language Gate
if st.session_state.lang is None:
    st.title("🌾Paddy yields🌾")
    col1, col2 = st.columns(2)
    if col1.button("English"):
        st.session_state.lang = "English";
        st.rerun()
    if col2.button("नेपाली"):
        st.session_state.lang = "Nepali";
        st.rerun()

# 2. Main Application
else:
    L = CONTENT[st.session_state.lang]
    st.title(L["title"])

    with st.sidebar:
        st.header(L["sidebar_header"])
        ward = st.selectbox("Select location", list(LOCATION.keys()))
        soil = st.selectbox("Soil Type",
                            ["Clay Loam: चिप्याइलो दोमट माटो", "Sandy Loam: बलौटे दोमट माटो", "Loam: दोमट माटो"])
        rainfall = st.slider("Rainfall (mm)", 1500, 3000, 2100)

        # Show local map
        st.map(pd.DataFrame([LOCATION[ward]]), zoom=12)

        if st.button("Change Language / भाषा बदल्नुहोस्"):
            st.session_state.lang = None;
            st.rerun()

    if st.button(L["predict_btn"]):
        # Model: Based on your 0.95 R-squared research
        yield_pred = 3100 + (rainfall * 0.78) + (200 if "Clay" in soil else 0)

        st.metric(L["result_label"], f"{int(yield_pred)} kg/ha")

        with st.spinner("AI Generating Recommendation..."):
            prompt = f"Agri-expert advice for {ward}, Jhapa. Soil: {soil}, Rain: {rainfall}mm. Yield: {int(yield_pred)}kg/ha. Provide 2 short sentences in {st.session_state.lang} only."

            # Receive both the advice and the status boolean
            advice, is_live = get_ai_advice(prompt)

            # --- THE STATUS LIGHT LOGIC ---
            if is_live:
                st.markdown("🟢 **System Status:** Live AI Intelligence")
                st.info(advice)
            else:
                st.markdown("🟠 **System Status:** Local Knowledge Mode (Offline/Busy)")
                st.warning(advice)

            # Audio Output - Properly aligned with the button logic
            audio_bytes = text_to_speech(advice, L["lang_code"])
            st.write(L["audio_label"])
            st.audio(audio_bytes, format="audio/mp3")

st.divider()
st.caption("| Prototype 2026 | Built by Ujjwal Dhungana |")