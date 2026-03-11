# Team Profile RAG

Internal RAG system for searching ~70-80 consulting team member profiles by skills, experience, certifications, and availability.

## Stack

| Layer | Tech |
|---|---|
| Backend | FastAPI + Python 3.11 |
| Frontend | Jinja2 + HTMX |
| Vector DB | ChromaDB (local, file-persisted) |
| Embeddings | sentence-transformers (`all-MiniLM-L6-v2`) |
| LLM | Anthropic Claude (`claude-sonnet-4-20250514`) |
| CV parsing | python-pptx |

## Quick Start

### 1. Install dependencies

```bash
python -m venv cvrag
cvrag\Scripts\activate.bat
python -m pip install -r requirements.txt
```

### 2. Generate sample data (for testing)

```bash
python scripts/generate_sample_data.py
```

This creates 10 fake consulting CVs in `./data/cvs/` and `./data/availability.csv`.

### 3. Index CVs

```bash
python scripts/ingest_cvs.py
```

Re-run with `--force` to re-index all files regardless of changes.

### 4. Run the app

```bash
uvicorn app.main:app --reload
```

Open http://localhost:8000

## Using Your Own CVs

1. Copy `.pptx` CV files to `./data/cvs/`
2. Update `./data/availability.csv` with team availability (see format below)
3. Run `python scripts/ingest_cvs.py`

### availability.csv format

```csv
name,current_project,availability_date,availability_percentage,location,grade
Ana García,Digital Transformation,2026-04-01,0,Madrid,Senior Consultant
Carlos Martínez,,2026-03-03,100,Barcelona,Manager
```

- `name` must match the name extracted from the CV (check the admin dashboard for mismatches)
- `availability_date`: ISO format `YYYY-MM-DD`
- `availability_percentage`: 0–100 (0 = fully engaged, 100 = fully available)

## Search Examples

- *"Azure data engineer available next month"*
- *"Who has Python and NLP skills and is on the bench?"*
- *"Certified cloud architect in Madrid"*
- *"Data engineer with Databricks, available at least 50%"*
- *"Spanish and English speaking consultants with cloud architecture experience"*

## Admin

Visit `/admin` to:
- View indexing stats
- Upload new CV files (.pptx)
- Upload updated availability data (.csv/.xlsx)
- Trigger re-indexing

## Docker

```bash
# Copy your .env file first
docker-compose up --build
```

Data in `./data/` is mounted as a volume and persists across restarts.

## Project Structure

```
team-profile-rag/
├── app/
│   ├── main.py                    # FastAPI app and routes
│   ├── config.py                  # Settings (pydantic-settings)
│   ├── models.py                  # Pydantic models
│   ├── search/
│   │   ├── engine.py              # RAG pipeline (ChromaDB + Claude reranking)
│   │   ├── embeddings.py          # sentence-transformers wrapper
│   │   └── filters.py             # Faceted filter logic
│   ├── ingestion/
│   │   ├── pptx_parser.py         # PowerPoint text extraction
│   │   ├── profile_builder.py     # Claude-powered structured parsing
│   │   ├── availability.py        # CSV/Excel adapter (pluggable)
│   │   └── sharepoint_connector.py # SharePoint stub (future)
│   ├── templates/                 # Jinja2 HTML templates
│   └── static/                    # CSS + JS
├── data/
│   ├── cvs/                       # .pptx files go here
│   ├── availability.csv
│   └── chroma_db/                 # ChromaDB persistence
├── scripts/
│   ├── ingest_cvs.py
│   └── generate_sample_data.py
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## RAG Pipeline

```
User query
    │
    ▼
Generate embedding (sentence-transformers)
    │
    ▼
ChromaDB cosine similarity search (top-20)
    │
    ▼
Apply faceted filters (skills, availability, grade, location)
    │
    ▼
Claude reranking + match explanation (top-10)
    │
    ▼
Ranked results with reasoning
```

## SharePoint Integration

The `sharepoint_connector.py` stub is ready for future implementation. See the module docstring for the full auth flow using Microsoft Graph API + MSAL. Once implemented, swap the manual file copy step with `connector.sync_to_local()`.

## Security Notes

Set both `ADMIN_USERNAME` and `ADMIN_PASSWORD` in `.env` to protect `/admin` endpoints with HTTP Basic Auth.

`MAX_UPLOAD_MB` controls maximum accepted file size for admin uploads.

## Scoring Notes

Displayed match percentages are calibrated from hybrid relevance (embedding similarity + keyword/phrase overlap), so exact role matches like "solutions architect" score more intuitively.