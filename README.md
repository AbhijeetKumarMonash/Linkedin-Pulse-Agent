# 🤖 LinkedIn Pulse Agent

An end-to-end automated content pipeline that scrapes tech news, drafts LinkedIn posts using AI, and maintains a persistent history database, all controlled via a custom frontend UI.

## 🚀 Features
* **RSS Integration:** Automatically pulls the latest tech news feeds.
* **AI Content Generation:** Uses Google Gemini to draft professional LinkedIn posts.
* **Database Memory:** Saves all generated headlines and drafts to a Google Sheets database.
* **History Dashboard:** A Streamlit frontend to trigger the n8n workflow and instantly display the history of all generated posts.

## 🛠️ Tech Stack
* **Orchestration:** n8n
* **Frontend:** Python, Streamlit
* **AI/LLM:** Google Gemini
* **Database:** Google Sheets API

## ⚙️ Setup Instructions

1. **Clone the repository**
   \`\`\`bash
   git clone  https://github.com/AbhijeetKumarMonash/Linkedin-Pulse-Agent.git
   cd Linkedin-Pulse-Agent
   \`\`\`

2. **Install dependencies**
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

3. **Import the Workflow**
   * Open your n8n instance.
   * Click **Import from File** and select the `workflow.json` included in this repository.
   * Update the Google Sheets and Gemini credentials inside the n8n nodes.

4. **Run the Application**
   \`\`\`bash
   streamlit run app.py
   \`\`\`

## 📸 Screenshots
<img width="1612" height="610" alt="image" src="https://github.com/user-attachments/assets/7e1ee5ae-bddf-4994-9a25-c1a4272e3a63" />
