import streamlit as st
import requests

st.set_page_config(page_title="LinkedIn Pulse V1", layout="centered")
st.title("🤖 LinkedIn Pulse Agent")

# Replace this with your actual n8n Test Webhook URL
N8N_WEBHOOK_URL = "http://localhost:5678/webhook-test/62564a4d-43be-4634-b888-b62bf777e718"

if st.button("🚀 Scrape Tech News & Draft Posts"):
    with st.spinner("Agent is working..."):
        try:
            response = requests.post(N8N_WEBHOOK_URL)
            if response.status_code == 200:
                st.success("Success! Check your Google Sheet for the drafts.")
            else:
                st.error(f"n8n returned an error: {response.status_code}")
        except Exception as e:
            st.error(f"Could not connect to n8n: {e}")

st.divider()
st.caption("V1.0 | LinkedIn Pulse Control Center")