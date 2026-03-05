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

# Your n8n Webhook URL
N8N_WEBHOOK_URL = "http://localhost:5678/webhook-test/62564a4d-43be-4634-b888-b62bf777e718"

col1, col2 = st.columns([1, 3], gap="large")

with col1:
    st.subheader("Control Panel")
    st.info("Click below to fetch the latest tech news, generate a new post, and retrieve your database history.")
    generate_btn = st.button("🚀 Scrape & Draft", type="primary", use_container_width=True)

with col2:
    if generate_btn:
        with st.spinner("🤖 Agent is scraping news and drafting content..."):
            try:
                response = requests.post(N8N_WEBHOOK_URL)

                if response.status_code == 200:
                    data = response.json()

                    if isinstance(data, list) and len(data) > 0:
                        st.success(f"✅ Success! Fetched {len(data)} total records from the database.")

                        # --- DEBUG VIEW ---
                        # with st.expander("🔍 Debug: View Raw JSON Payload from n8n"):
                        #     st.json(data)

                        data.reverse()
                        tab1, tab2 = st.tabs(["✨ Latest Draft", "🗄️ History Vault"])

                        # TAB 1: The newest generation
                        with tab1:
                            latest = data[0]
                            # Clean the dictionary keys to ignore case and spaces
                            clean_latest = {str(k).strip().lower(): v for k, v in latest.items()}

                            # Safely extract values regardless of capitalization
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
    else:
        st.markdown("### 👈 Awaiting instructions...")
        st.caption("Hit the 'Scrape & Draft' button in the control panel to spin up the agent.")