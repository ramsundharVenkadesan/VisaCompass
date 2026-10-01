# 🧭 VisaCompass

**VisaCompass** is a specialized U.S. Immigration Law AI Assistant tailored for international students, workers, and immigrants. Powered by a **LangGraph/Langchain ReAct Agent** and **Google Gemini 3.5 Flash**, VisaCompass breaks down dense federal codes into friendly, **6th-grade reading-level** advice using intuitive analogies while strictly grounding all facts in real-time, official government sources (USCIS, DOL, DHS, and eCFR).

---

## ✨ Key Features

- **Live Government Intel (ReAct Architecture)**: VisaCompass doesn’t guess. It uses dynamic tool calling to search the **eCFR**, **USCIS Policy Manuals**, **Department of State FAM**, and **GovInfo**.
- **Transparent Reasoning**: As the agent researches your question, the frontend streams its real-time "Thoughts" and "Actions"—letting you peek under the hood at exactly what sources it is checking.
- **Structured Legal Formatting**: Responses aren't massive walls of scary legal jargon. They are mapped into strict JSON Pydantic models and beautifully rendered in the UI into 5 clean sections:
  1. 🎯 **Direct Verdict & Your Situation**
  2. 📋 **Your Options & Simple Steps**
  3. ⚠️ **Big Mistakes to Avoid**
  4. ⚖️ **Questions to Ask an Immigration Lawyer**
  5. 🏛️ **Official References**

---

## 🏗️ Project Architecture

```text
VisaCompass/
├── Application.py         # 🚀 FastAPI server with SSE streaming endpoints
├── Agent.py               # 🧠 Core LangChain/LangGraph ReAct Agent setup
├── Prompt.py              # 📝 AI System prompts holding the 6th-grade analogical reasoning rules
├── StructuredModels.py    # 📦 Pydantic schemas (ImmigrationResponse) to enforce UI output boundaries
├── ExecutableTools/       # 🛠️ Toolkit for live web scraping & API queries
│   ├── ECFR.py            # Code of Federal Regulations lookups (Title 8, 20, 22)
│   ├── GuidanceSources.py # USCIS, DHS, and DOS web crawling tools
│   └── GOV_INFO.py        # Federal Register operations
├── templates/
│   └── index.html         # 🎨 A sleek, responsive, vanilla JS + CSS frontend
└── .env                   # 🔑 Your secret API keys
```

---

## 🚀 Getting Started

### 1. Prerequisites
Ensure you have **Python 3.10+** installed on your machine.

### 2. Environment Setup
1. Clone this repository.
2. Create and activate a Virtual Environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
   ```
3. Install standard requirements (FastAPI, Langchain, Pydantic, Uvicorn, etc.).
   ```bash
   pip install fastapi uvicorn pydantic langchain langchain-google-genai python-dotenv langsmith
   ```
   *(Note: Adjust your pip installs based on the specific required libraries used inside your `ExecutableTools`)*

### 3. API Keys (`.env`)
Create a `.env` file in the root navigation and paste your required keys. At minimum, VisaCompass requires:
```env
GOOGLE_API_KEY=your_gemini_api_key_here
TAVILY_API_KEY=your_tavily_search_api_key_here
```

### 4. Run the Application
Boot up the FastAPI server via Uvicorn:
```bash
uvicorn Application:app --port 8000 --reload
```

Then, open your web browser and navigate to:
**[http://localhost:8000](http://localhost:8000)**

---

## ⚙️ How it Works Under the Hood

1. **User Input:** A user types a question in the frontend (e.g. *"What are my F1 visa options if it expires in 6 months?"*). 
2. **SSE Streaming:** `index.html` fires a POST to `/stream`. FastAPI hands the prompt over to `stream_query()` inside `Agent.py`.
3. **ReAct Loop Execution:** Gemini starts reasoning. Every time it decides to use a tool (like `search_uscis_data`), a `react_step` JSON event is streamed back to the UI in real-time, appearing in the sleek loading accordion.
4. **Structured JSON Output:** Once the AI has enough government evidence, it formats its final analysis according to the `ImmigrationResponse` schema.
5. **UI Rendering:** The frontend captures the `done` event, breaks apart the JSON, and elegantly paints the browser with colored headers, tooltips, and clickable reference links.

---

## ⚖️ Disclaimer
**VisaCompass is a Legal Technology tool, not a law firm.** It is built for educational orientation and strategy brainstorming. Users must always verify the generated outputs with a licensed U.S. Immigration Attorney before making any life-altering legal decisions.
