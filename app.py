import streamlit as st
import google.generativeai as genai

st.title("🛠️ GEMINI DIAGNOSTIC TOOL")

# Get API Key
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    st.success("API Key Found")
except:
    st.error("No API Key found in Secrets!")
    st.stop()

if st.button("LIST AVAILABLE MODELS"):
    try:
        st.write("Contacting Google API...")
        models = genai.list_models()
        found = False
        for m in models:
            if 'generateContent' in m.supported_generation_methods:
                st.code(f"Model Name: {m.name}")
                found = True
        
        if not found:
            st.error("No text generation models found! Check your API Key permissions.")
    except Exception as e:
        st.error(f"Error: {e}")
