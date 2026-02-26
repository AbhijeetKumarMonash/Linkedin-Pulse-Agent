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

if 'history' not in st.session_state:
    st.session_state['history'] = []


def extract_hashtags(text):
    return re.findall(r'#\w+', text)


def estimate_read_time(text):
    words = len(text.split())
    minutes = max(1, round(words / 200))
    return f"{minutes} MIN READ"


def convert_to_csv(data_list):
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["Headline", "Draft Content"])
    for row in data_list:
        clean = {str(k).strip().lower(): v for k, v in row.items()}
        h = clean.get("headline", clean.get("title", "UNTITLED"))
        d = clean.get("draft", clean.get("text", ""))
        writer.writerow([h, d])
    return output.getvalue()


# --- 4. Sidebar Controls (Features Restored) ---
with st.sidebar:
    st.markdown("<h2 class='gradient-text'>💠 NEXUS SYSTEM</h2>", unsafe_allow_html=True)
    st.info("STATUS: SECURE UPLINK")
    st.metric(label="DATABASE RECORDS", value=len(st.session_state['history']))

    st.divider()
    st.markdown("### 🔍 SEARCH VAULT")
    search_query = st.text_input("Filter database...", placeholder="Enter keyword...")

    if st.session_state['history']:
        st.divider()
        st.markdown("### 💾 EXPORT")
        st.download_button("DOWNLOAD CSV", data=convert_to_csv(st.session_state['history']),
                           file_name="nexus_database.csv", mime="text/csv", use_container_width=True)

# --- 5. Main Layout ---
st.markdown(
    "<h1 style='text-align: center; font-size: 3.5rem; margin-top: 1rem;' class='gradient-text'>LINKEDIN PULSE MATRIX</h1>",
    unsafe_allow_html=True)
st.markdown(
    "<p style='text-align: center; margin-bottom: 2rem; color: #94a3b8;'>Autonomous RSS Synthesis & Content Orchestration</p>",
    unsafe_allow_html=True)

col_action, col_display = st.columns([1, 2.5], gap="large")

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
                    st.error(f"HTTP ERROR: {res.status_code}")
            except Exception as e:
                st.error("CONNECTION SEVERED: Is n8n listening?")

# -- Right Column: Data Visualization --
with col_display:
    display_data = st.session_state.get('history', [])

    if not display_data:
        st.markdown("""
        <div class="glass-card" style="text-align: center;">
            <h3 style="color: #64748b;">AWAITING COMMAND</h3>
            <p style="color: #475569;">Initiate Scrape to populate the visualization matrix.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        display_data = list(reversed(display_data))

        # Apply Search Filter
        if search_query:
            display_data = [row for row in display_data if search_query.lower() in str(row).lower()]
            if not display_data:
                st.warning("No records match your query.")

        if display_data:
            # Tabbed View Restored
            tab_latest, tab_archive = st.tabs(["✨ LIVE SIGNAL", "📚 ARCHIVAL LOGS"])

            with tab_latest:
                latest = display_data[0]
                clean = {str(k).strip().lower(): v for k, v in latest.items()}

                # Resilient Fallback mapping
                body = clean.get("draft", clean.get("text", "No transmission data."))
                head = clean.get("headline", clean.get("title", ""))

                if not head or head == "":
                    subject_match = re.search(r'\*\*Subject:\s*(.*?)\*\*', body)
                    head = subject_match.group(1) if subject_match else "AUTOMATED TRANSMISSION"

                # Clean up the body text
                display_body = re.sub(r'\*\*Subject:\s*.*?\*\*', '', body).strip()

                hashtags = extract_hashtags(display_body)
                tags_html = "".join([f"<span class='data-tag'>{tag}</span>" for tag in hashtags])

                st.markdown(f"""
                <div class="glass-card">
                    <span class="meta-text">{estimate_read_time(display_body)}</span>
                    <h2 style="color: #f8fafc; margin-top: 0;">{head}</h2>
                    <div class="glass-text">{display_body}</div>
                    <div style="margin-top: 1.5rem;">{tags_html}</div>
                </div>
                """, unsafe_allow_html=True)

            with tab_archive:
                if len(display_data) > 1:
                    for i, row in enumerate(display_data[1:]):
                        clean = {str(k).strip().lower(): v for k, v in row.items()}
                        body = clean.get("draft", clean.get("text", "No text."))
                        head = clean.get("headline", clean.get("title", ""))

                        if not head or head == "":
                            subject_match = re.search(r'\*\*Subject:\s*(.*?)\*\*', body)
                            head = subject_match.group(1) if subject_match else f"ARCHIVE_LOG_{i}"

                        with st.expander(f"📁 {head}"):
                            st.markdown(f"<span class='meta-text'>{estimate_read_time(body)}</span>",
                                        unsafe_allow_html=True)
                            st.markdown(re.sub(r'\*\*Subject:\s*.*?\*\*', '', body).strip())

                            hashtags = extract_hashtags(body)
                            if hashtags:
                                tags_html = "".join([f"<span class='data-tag'>{tag}</span>" for tag in hashtags])
                                st.markdown(tags_html, unsafe_allow_html=True)
                else:
                    st.info("No older archives available. Run the sequence again to build history.")