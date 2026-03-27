# Pulse — Engineering Intelligence Dashboard

> TOKYO Problem Statement | HBTU Campus Drive | Team T03

## Project Overview
Pulse analyzes any GitHub repository and provides AI-powered insights into team contributions, code activity, and engineering patterns.

## Team Roles
| Member | Role | GitHub |
|---|---|---|
| Shivendra Pal | AI/ML Engineer | shiv010hbtu |
| Amit | Backend Engineer | Amitt-28 |
| Vasundhara Singh | Frontend Engineer | Vasundhara Singh |
| Ankit Tiwary | Database Engineer | ANKIT TIWARY |
| Suraj Maurya | DevOps & Docs | suraj-maurya2 |

## Tech Stack
| Layer | Technology |
|---|---|
| Backend | FastAPI (Python) |
| Frontend | React + Recharts |
| Database | MongoDB Atlas |
| AI/ML | Gemini API + Python |

## Architecture
```
GitHub URL → FastAPI Backend → GitHub API
                  ↓
            ML Module (Gemini)
                  ↓
          MongoDB (Store + Cache)
                  ↓
        React Frontend Dashboard
```

## Setup Instructions
### ML + Backend
```bash
cd ml
pip install -r requirements.txt
cp .env.example .env
# Add GEMINI_API_KEY in .env
```
### Frontend
```bash
cd frontend
npm install
npm start
```

## API Documentation
| Endpoint | Method | Description |
|---|---|---|
| /analyze | POST | Analyze a GitHub repo URL |
| /contributors | GET | Get all contributors data |
| /commits | GET | Get classified commit history |
| /health-score | GET | Get engineering health score |

## Key Design Decisions (ADR)
- **MongoDB**: Flexible schema for varied commit structures
- **Gemini API**: Free tier, handles classification + summarization
- **FastAPI**: Async support for non-blocking API calls
- **Rule-based fallback**: Classifier works even if LLM fails
