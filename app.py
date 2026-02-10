import streamlit as st
from logic import create_crew

# Page Config
st.set_page_config(page_title="GEMINI SCALPER", page_icon="📈", layout="wide")

# Custom CSS for "Hacker Mode"
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
st.subheader("Powered by Gemini 1.5 Pro & CrewAI")

# sidebar for API key security
with st.sidebar:
    st.header("🔒 Secure Access")
    # Try to load from secrets, otherwise ask user
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
        st.success("API Key Loaded from Cloud Secrets")
    except:
        api_key = st.text_input("Enter Google API Key", type="password")

if st.button("🚀 SCAN MARKETS NOW"):
    if not api_key:
        st.error("Please enter your API Key first!")
        st.stop()
    
    with st.spinner('🤖 AGENTS DEPLOYED... SCANNING GLOBAL FEEDS...'):
        try:
            # Initialize the Crew
            crew = create_crew(api_key)
            # Execute
            result = crew.kickoff()
            
            st.success("✅ INTELLIGENCE ACQUIRED")
            st.markdown("---")
            st.markdown(result)
        except Exception as e:
            st.error(f"Execution Error: {str(e)}")

# Force rebuild 1
