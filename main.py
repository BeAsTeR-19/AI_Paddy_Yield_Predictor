import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


# 1. SETUP THE ADVISOR FUNCTION
def get_agricultural_advice(yield_val, rain, soil, location):
    # Use the 2026 model found in your terminal
    model = genai.GenerativeModel('models/gemini-2.5-flash')

    # This is the "Harvard-level" prompt engineering
    prompt = f"""
    Context: You are an AI Agricultural Consultant for Jhapa, Nepal.
    Farmer Data:
    - Location: {location}
    - Soil Type: {soil}
    - Predicted Rainfall: {rain} mm
    - Predicted Yield from ML model: {yield_val} kg/ha

    Task: Provide a 3-sentence recommendation in English. 
    1. Evaluate if the yield is good for {location}.
    2. Give one specific tip for {soil} soil.
    3. Suggest if they should plant paddy or an alternative crop based on rainfall.
    """

    response = model.generate_content(prompt)
    return response.text


# 2. SIMULATE YOUR ML RESULTS (Based on your high R-Squared run)
# Imagine your model just predicted this for a farmer in Sanischare:
predicted_paddy_yield = 4950
current_rainfall = 2100
farmer_soil = "Clay Loam"
farmer_loc = "Sanischare, Jhapa"

# 3. GENERATE THE REPORT
print("--- PREDICTIVE ANALYSIS COMPLETE ---")
print(f"ML Predicted Yield: {predicted_paddy_yield} kg/ha")
print("\n--- GENERATING AI ADVICE ---")

advice = get_agricultural_advice(predicted_paddy_yield, current_rainfall, farmer_soil, farmer_loc)
print(advice)