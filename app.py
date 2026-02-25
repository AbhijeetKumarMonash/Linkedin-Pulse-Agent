import streamlit as st
import requests
import csv
from io import StringIO

# --- Page Configuration ---
st.set_page_config(page_title="LinkedIn Pulse AI | Pro+", page_icon="⚡", layout="wide")

# --- Custom CSS ---
st.markdown("""
    <style>
    .stButton>button {border-radius: 8px; font-weight: bold; height: 50px; width: 100%; transition: all 0.3s;}
    .stButton>button:hover {border: 1px solid #0a66c2; color: #0a66c2;}
    .latest-post {border-left: 5px solid #0a66c2; padding: 1.5rem; background-color: #f8f9fa; border-radius: 0px 8px 8px 0px; margin-bottom: 1rem;}
    </style>
""", unsafe_allow_html=True)

# --- Webhook Configuration ---
# Replace with your actual n8n Test Webhook URL
WEBHOOK_URL = "http://localhost:5678/webhook-test/62564a4d-43be-4634-b888-b62bf777e718"

# --- Session State Management ---
if 'history' not in st.session_state:
    st.session_state['history'] = []


# --- Helper Function: Export to CSV ---
def convert_to_csv(data_list):
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["Headline", "Draft"])
    for row in data_list:
        clean_row = {str(k).strip().lower(): v for k, v in row.items()}
        h = clean_row.get("headline", clean_row.get("title", "Untitled"))
        d = clean_row.get("draft", clean_row.get("text", "No draft text found."))
        writer.writerow([h, d])
    return output.getvalue()


# --- Sidebar: System Status & Metrics ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/c/ca/LinkedIn_logo_initials.png", width=50)
    st.header("⚙️ System Control")
    st.info("Status: API Standby")

    # Live Metrics
    st.metric(label="Total Drafts in Database", value=len(st.session_state['history']))

    st.divider()
    st.markdown("### 🔍 Search Vault")
    search_query = st.text_input("Filter previous articles by keyword...", placeholder="e.g., Waymo, AI, Cyber...")

    if st.session_state['history']:
        st.divider()
        st.markdown("### 💾 Export Data")
        csv_data = convert_to_csv(st.session_state['history'])
        st.download_button(
            label="📥 Download CSV",
            data=csv_data,
            file_name="linkedin_pulse_history.csv",
            mime="text/csv",
            use_container_width=True
        )

# --- Main Dashboard ---
st.title("⚡ LinkedIn Pulse Content Engine")
st.markdown("Automated tech curation and AI-powered post generation.")
st.divider()

col_action, col_display = st.columns([1, 2.5], gap="large")

# -- Left Column: Controls --
with col_action:
    st.markdown("### Action Center")
    generate_btn = st.button("🚀 Scrape News & Draft Posts", type="primary")
    st.caption("Fetches the latest RSS feed, generates drafts via Gemini, and updates the Google Sheet.")

    if generate_btn:
        with st.spinner("🤖 Agent is processing... (Pacing requests to respect API limits)"):
            try:
                res = requests.post(WEBHOOK_URL)

                if res.status_code == 429:
                    st.warning(
                        "⏳ Gemini API rate limit reached. The Wait node in n8n needs to be active. Please try again in a few seconds.")
                elif res.status_code == 200:
                    data = res.json()
                    if isinstance(data, list) and len(data) > 0:
                        st.session_state['history'] = data
                        st.success(f"✅ Success! Database synced with {len(data)} records.")
                    else:
                        st.warning("Executed, but no data returned. Check the n8n read node.")
                else:
                    st.error(f"Workflow failed. HTTP Status: {res.status_code}")

            except Exception as e:
                st.error(f"Connection Error: Is n8n listening? Details: {e}")

# -- Right Column: Display --
with col_display:
    display_data = st.session_state['history']

    if not display_data:
        st.info("Awaiting execution. Click the button to generate and fetch your first batch of articles.")
    else:
        # Reverse list to show newest first
        display_data = list(reversed(display_data))

        # Apply Search Filter
        if search_query:
            display_data = [row for row in display_data if search_query.lower() in str(row).lower()]
            if not display_data:
                st.warning(f"No articles match your search query: '{search_query}'")

        if display_data:
            # Create Navigation Tabs
            tab1, tab2 = st.tabs(["✨ Latest Output", "📚 Full Archive"])

            # Tab 1: Prominent display of the newest post
            with tab1:
                latest = display_data[0]
                clean_latest = {str(k).strip().lower(): v for k, v in latest.items()}
                head = clean_latest.get("headline", clean_latest.get("title", "Untitled"))
                body = clean_latest.get("draft", clean_latest.get("text", "No draft text found."))

                st.markdown(f"""
                <div class="latest-post">
                    <h3>{head}</h3>
                    <p style="white-space: pre-wrap;">{body}</p>
                </div>
                """, unsafe_allow_html=True)

            # Tab 2: Clean expanders for older posts
            with tab2:
                if len(display_data) > 1:
                    for i, row in enumerate(display_data[1:]):
                        clean_row = {str(k).strip().lower(): v for k, v in row.items()}
                        head = clean_row.get("headline", clean_row.get("title", "Untitled"))
                        body = clean_row.get("draft", clean_row.get("text", "No draft available."))

                        with st.expander(f"📝 {head}"):
                            st.markdown(body)
                else:
                    st.write("No historical archives available yet. Run the agent again to build your database!")