# Pulse — System Architecture

## Overview
```
User → Frontend (Next.js:3000)
            ↓
       Backend (FastAPI:8000)
            ↓
    GitHub API + ML Module
            ↓
       MongoDB Atlas
```

## Data Flow
1. User enters GitHub repo URL
2. Frontend sends POST /analyze to backend
3. Backend fetches commits from GitHub API
4. ML module classifies + scores each commit
5. Gemini API generates contributor summaries
6. Results saved to MongoDB
7. Frontend displays charts, heatmap, cards

## Key Design Decisions

### Why FastAPI?
- Async support for non-blocking GitHub API calls
- Auto-generated API docs at /docs
- Easy ML module integration

### Why MongoDB?
- Flexible schema for varied commit structures
- Free Atlas tier sufficient

### Why Gemini API?
- Free tier available
- Rule-based fallback if API fails

### Why Next.js?
- Better performance
- Easy deployment
