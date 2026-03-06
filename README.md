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
N8n Workflow Basic :
<img width="1612" height="610" alt="image" src="https://github.com/user-attachments/assets/7e1ee5ae-bddf-4994-9a25-c1a4272e3a63" />
N8n Workflow for version 1.1:
<img width="1348" height="372" alt="image" src="https://github.com/user-attachments/assets/25c15604-03e5-47b2-a2ce-456e93251ed4" />

streamlit output of version 1 basic :
<img width="1917" height="866" alt="image" src="https://github.com/user-attachments/assets/7ff3cc82-9a35-4cf2-8b3a-a17153b83830" />
streamlit output of version1.1 :
<img width="1916" height="971" alt="Linkedinv1_1" src="https://github.com/user-attachments/assets/d9dc0f33-3e13-40c4-b542-890ec23f79ea" />
output in excel:
<img width="1462" height="642" alt="image" src="https://github.com/user-attachments/assets/91c2ced2-eb63-4089-8e2b-6b7e1980c1ba" />



