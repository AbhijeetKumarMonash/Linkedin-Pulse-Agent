import streamlit as st
import requests

st.set_page_config(page_title="LinkedIn Pulse AI", page_icon="⚡", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    .block-container { padding-top: 2rem; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; height: 50px;}
    </style>
""", unsafe_allow_html=True)

st.title("⚡ LinkedIn Pulse Agent")
st.markdown("Automated tech news curation and AI-powered LinkedIn draft generation.")
st.divider()

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

                if response.status_code == 200:
                    data = response.json()

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

                            st.subheader(head)
                            st.markdown(f"> {body}")

                        # TAB 2: History loop
                        with tab2:
                            for i, row in enumerate(data[1:]):
                                clean_row = {str(k).strip().lower(): v for k, v in row.items()}
                                head = clean_row.get("headline", clean_row.get("title", "Untitled"))
                                body = clean_row.get("draft", clean_row.get("text", "No Draft available."))

                                with st.expander(f"📝 {head} (Archive #{len(data) - 1 - i})"):
                                    st.markdown(body)
                    else:
                        st.warning("n8n fired successfully, but returned empty data.")
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