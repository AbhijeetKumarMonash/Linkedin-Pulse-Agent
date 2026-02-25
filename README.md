# 🤖 LinkedIn Pulse Agent

An automated content generation pipeline that scrapes tech news, uses AI to draft LinkedIn posts, and displays the status via a custom Streamlit dashboard.

## 🚀 Features
* **Automated News Scraping:** Pulls the latest articles via RSS.
* **AI Content Generation:** Uses Gemini to instantly draft professional LinkedIn posts based on the news.
* **Database Integration:** Automatically appends drafts to a Google Sheet.
* **Custom Frontend:** A Streamlit UI to trigger the agent and monitor success.

## 🛠️ Tech Stack
* **Workflow Automation:** n8n
* **Frontend:** Python & Streamlit
* **AI/LLM:** Google Gemini
* **Database:** Google Sheets API

## 📸 Screenshots
*(Drop your image files into an `assets` folder and link them here)*
![n8n Workflow](assets/n8n-workflow.png)
![Streamlit UI](assets/streamlit-ui.png)

## ⚙️ How to Run Locally

1. **Install Python Dependencies:**
   pip install -r requirements.txt

2. **Import the n8n Workflow:**
   Open n8n, click "Import from File", and select `workflow.json`.

3. **Run the Streamlit App:**
   streamlit run app.py
