# Finance Assistant (Demo)

A small demo project built with Streamlit, LangGraph and Gemini. It answers questions from a document (RAG) and shows a customer's portfolio as a pie chart.

> **Note:** All customer names, national/tax IDs and portfolio data in `data/portfolio.db` are **entirely fictional**. `data/veriler/ornek_analiz.docx` is a made-up sample document and does not belong to any real organization. The app UI and sample document are in Turkish.

## Features
- Answers questions using the `.docx` files in `data/veriler/` (retrieval-augmented generation).
- For questions like "portföy müşteri id 5", shows that customer's portfolio distribution as a pie chart.

## Setup
```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env             # Windows: copy .env.example .env
# Open .env and set GOOGLE_API_KEY to your own key
streamlit run app.py
```

## Notes
- `data/portfolio.db` contains demo data. `data/qa_history.db` is created automatically on first run.
