import streamlit as st
from logic import create_crew

st.set_page_config(page_title="GEMINI SCALPER", page_icon="📈", layout="wide")

st.markdown("""
<style>
    .stApp {
        background-color: #000000;
        color: #00FF00;
    }
    .stButton>button {
        color: #000000;
        background-color: #00FF00;
        border: none;
    }
</style>
""", unsafe_allow_html=True)

st.title("💸 GEMINI MARKET SCALPER")
st.subheader("Powered by Gemini 2.5 Flash")

# Secure API Key Access
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except:
    # Fallback for local testing
    api_key = st.text_input("Enter Google API Key", type="password")

if st.button("🚀 SCAN MARKETS NOW"):
    if not api_key:
        st.error("API Key missing! Check Streamlit Secrets.")
        st.stop()
    
    with st.spinner('🤖 AGENTS DEPLOYED... SCANNING GLOBAL FEEDS...'):
        try:
            crew = create_crew(api_key)
            result = crew.kickoff()
            
            st.success("✅ INTELLIGENCE ACQUIRED")
            st.markdown("---")
            st.markdown(result)
        except Exception as e:
            st.error(f"Execution Error: {str(e)}")
