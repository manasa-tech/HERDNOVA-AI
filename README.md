# 🐄 HerdWise AI

### Multi-Agent AI Livestock Farm Decision Support System

**Smarter Farms. Healthier Herds.**

HerdWise AI is an AI-powered livestock farm management platform that helps farmers make smarter, data-driven decisions using a multi-agent AI system.

## ✨ Features

- 🩺 **Animal Health Agent** – Identifies potential livestock health concerns.
- 🌿 **Nutrition Agent** – Provides feed optimization recommendations.
- 🧬 **Breeding Agent** – Supports breeding and lactation decisions.
- 📦 **Inventory Agent** – Tracks feed, medicines, and farm supplies.
- 💰 **Finance Agent** – Analyzes farm expenses and potential losses.
- 🤖 **Farm Manager** – Coordinates specialist agents to analyze farm problems.
- 📊 **Smart Dashboard** – Displays farm statistics, alerts, and milk production insights.
- 💬 **AI Farm Analysis** – Lets farmers describe problems in natural language and receive recommendations.

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Frontend | React.js, Vite, CSS |
| Backend | Python, FastAPI |
| AI Integration | Google Gemini API |
| API Communication | REST API |
| Version Control | Git and GitHub |

## 🏗️ How It Works

1. The farmer submits a question or describes a farm problem.
2. The Farm Manager identifies relevant specialist agents.
3. The agents analyze the problem from their respective perspectives.
4. Google Gemini helps generate AI-powered insights.
5. The system displays findings and suggested actions.

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Node.js and npm
- Google Gemini API key

### Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd livestock-ai
```

### Run the Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file inside the `backend` folder:

```env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-flash-latest
```

Start the backend server:

```bash
uvicorn main:app --reload
```

Backend: `http://127.0.0.1:8000`

API documentation: `http://127.0.0.1:8000/docs`

### Run the Frontend

Open a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the local URL shown in your terminal, usually `http://localhost:5173`.

## 🌱 Expected Impact

- Support earlier identification of potential livestock health issues.
- Improve feed and inventory management.
- Help farmers understand farm expenses and potential losses.
- Support more informed livestock management decisions.
- Make AI-powered farm insights easier to access.

## 🔮 Future Scope

- IoT-based livestock monitoring.
- Predictive milk production analytics.
- Veterinary consultation support.
- Local language support.
- Persistent database integration.
- Weather and market price analysis.

## 🔐 Security

Never commit API keys or `.env` files to GitHub. Keep credentials private and use environment variables for configuration.

## 🤝 Contributing

Contributions and suggestions are welcome. Fork the repository, create a feature branch, and submit a pull request.

## 📄 License

An appropriate open-source license can be added before public distribution.

---

**HerdWise AI — Empowering farmers through intelligent livestock management.**
