import streamlit as st
import requests
import re
import csv
from io import StringIO

# --- 1. Page Configuration ---
st.set_page_config(page_title="Nexus Hub | Pro", page_icon="💠", layout="wide", initial_sidebar_state="expanded")

# --- 2. Advanced CSS Injection ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');

    /* Global Theme */
    .stApp {
        background: radial-gradient(circle at top left, #0f172a, #020617);
        font-family: 'Outfit', sans-serif;
        color: #e2e8f0;
    }

    /* Typography Overrides */
    h1, h2, h3 { font-family: 'Outfit', sans-serif; font-weight: 800; }
    .gradient-text {
        background: -webkit-linear-gradient(#38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Glassmorphism Cards */
    .glass-card {
        background: rgba(30, 41, 59, 0.4);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
        margin-bottom: 1.5rem;
        transition: transform 0.3s ease, border 0.3s ease;
    }
    .glass-card:hover { border: 1px solid rgba(56, 189, 248, 0.3); }
    .glass-text { color: #cbd5e1; font-size: 1.05rem; line-height: 1.6; white-space: pre-wrap; }

    /* Animated Primary Button */
    .stButton>button {
        background: linear-gradient(-45deg, #0ea5e9, #3b82f6, #8b5cf6, #ec4899);
        background-size: 300% 300%;
        animation: gradient-shift 4s ease infinite;
        border: none !important;
        color: white !important;
        font-weight: 800;
        font-size: 1.1rem;
        border-radius: 12px;
        height: 60px;
        width: 100%;
        box-shadow: 0 8px 20px -10px rgba(14, 165, 233, 0.8);
        transition: all 0.3s ease;
    }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 15px 25px -10px rgba(14, 165, 233, 1); }

    @keyframes gradient-shift { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }

    /* Tags and Meta */
    .data-tag { display: inline-block; background: rgba(56, 189, 248, 0.1); color: #38bdf8; padding: 4px 12px; border-radius: 20px; font-size: 0.85rem; font-weight: 600; margin-right: 8px; margin-bottom: 8px; border: 1px solid rgba(56, 189, 248, 0.2); }
    .meta-text { color: #64748b; font-size: 0.85rem; font-weight: 600; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 0.5rem; display: block;}
    </style>
""", unsafe_allow_html=True)

# --- 3. App Logic & Configuration ---
WEBHOOK_URL = "http://localhost:5678/webhook/62564a4d-43be-4634-b888-b62bf777e718"

# --- URLs ---
# generation Webhook URL (POST)
N8N_WEBHOOK_URL = "http://localhost:5678/webhook-test/62564a4d-43be-4634-b888-b62bf777e718"

# GET Method for History Vault V1.1
N8N_FETCH_URL = "http://localhost:5678/webhook-test/132e1cb7-e4b6-4bc4-9ee4-81f791671dfb"

col1, col2 = st.columns([1, 3], gap="large")

with col1:
    st.subheader("Control Panel")
    st.info("Choose an action below to manage your LinkedIn content.")

    # Existing generation button
    generate_btn = st.button("🚀 Scrape & Draft", type="primary", use_container_width=True)

    # New fetch history button
    fetch_btn = st.button("🗄️ Fetch History Only", type="secondary", use_container_width=True)

with col2:
    # --- LOGIC 1: RUN THE AGENT ---
    if generate_btn:
        with st.spinner("🤖 Agent is scraping news and drafting content..."):
            try:
                response = requests.post(N8N_WEBHOOK_URL)

def estimate_read_time(text):
    words = len(text.split())
    minutes = max(1, round(words / 200))
    return f"{minutes} MIN READ"

                    if isinstance(data, list) and len(data) > 0:
                        st.success(f"✅ Success! Fetched {len(data)} total records from the database.")
                        data.reverse()
                        tab1, tab2 = st.tabs(["✨ Latest Draft", "🗄️ History Vault"])

                        # TAB 1: The newest generation
                        with tab1:
                            latest = data[0]
                            clean_latest = {str(k).strip().lower(): v for k, v in latest.items()}
                            head = clean_latest.get("headline", clean_latest.get("title", "No Headline Available"))
                            body = clean_latest.get("draft", clean_latest.get("text", "No Draft text found."))

    if st.session_state['history']:
        st.divider()
        st.markdown("### 💾 EXPORT")
        st.download_button("DOWNLOAD CSV", data=convert_to_csv(st.session_state['history']),
                           file_name="nexus_database.csv", mime="text/csv", use_container_width=True)

                        # TAB 2: History loop
                        with tab2:
                            for i, row in enumerate(data[1:]):
                                clean_row = {str(k).strip().lower(): v for k, v in row.items()}
                                head = clean_row.get("headline", clean_row.get("title", "Untitled"))
                                body = clean_row.get("draft", clean_row.get("text", "No Draft available."))

# -- Left Column: Triggers --
with col_action:
    if st.button("🚀 INITIATE AI SCRAPE"):
        with st.spinner("Connecting to n8n pipeline... (Respecting API rate limits)"):
            try:
                res = requests.post(WEBHOOK_URL)
                if res.status_code == 200:
                    data = res.json()
                    if isinstance(data, list) and len(data) > 0:
                        st.session_state['history'] = data
                        st.toast("✅ Synchronization Complete", icon="💠")
                    else:
                        st.warning("Executed, but payload was empty.")
                elif res.status_code == 429:
                    st.error("SYSTEM OVERLOAD: Gemini API Limit. Wait 10 seconds.")
                else:
                    st.error(f"n8n returned an error: {response.status_code}")
            except Exception as e:
                st.error(f"Could not connect to n8n. Error: {e}")

    # --- LOGIC 2: FETCH HISTORY ONLY ---
    elif fetch_btn:
        with st.spinner("🗄️ Fetching your database history..."):
            try:
                # Note the requests.get() instead of requests.post()
                response = requests.get(N8N_FETCH_URL)

                if response.status_code == 200:
                    data = response.json()

                    if isinstance(data, list) and len(data) > 0:
                        st.success(f"✅ Success! Retrieved {len(data)} records from the vault.")
                        data.reverse()

                        st.subheader("🗄️ History Vault")

                        for i, row in enumerate(data):
                            clean_row = {str(k).strip().lower(): v for k, v in row.items()}
                            head = clean_row.get("headline", clean_row.get("title", "Untitled"))
                            body = clean_row.get("draft", clean_row.get("text", "No Draft available."))

                            with st.expander(f"📝 {head} (Archive #{len(data) - i})"):
                                st.markdown(body)
                    else:
                        st.warning("Database connected, but no history found.")
                else:
                    st.error(f"n8n returned an error: {response.status_code}")
            except Exception as e:
                st.error(f"Could not connect to n8n. Error: {e}")

    # --- LOGIC 3: DEFAULT STATE ---
    else:
        st.markdown("### 👈 Awaiting instructions...")
        st.caption("Hit 'Scrape & Draft' to run the agent, or 'Fetch History' to view past drafts.")
