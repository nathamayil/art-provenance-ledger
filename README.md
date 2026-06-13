# Art Provenance Ledger

> Trace the stylistic DNA of any artwork using AI-powered visual embeddings and graph-based provenance tracking.
> <img width="720" height="892" alt="image" src="https://github.com/user-attachments/assets/a97c7b76-81ff-4224-bcd2-220538a011e1" />


Upload any painting or AI-generated image and the system identifies which artists and movements most influenced its visual style.

**Example:** Upload a Nicholas Roerich-style painting and get back:
<img width="851" height="897" alt="image" src="https://github.com/user-attachments/assets/e9f054d6-64dc-4598-9c4a-630769d77634" />

- Nicholas Roerich — 53%
- Gustave Doré — 33%
- Albrecht Dürer — 7%

---

## Tech Stack

- **ML:** OpenAI CLIP (`clip-vit-large-patch14`) via HuggingFace
- **Vector Search:** FAISS (HNSW, 1024-dim)
- **Graph DB:** Neo4j 5.15
- **Backend:** FastAPI + Uvicorn
- **Frontend:** React + Vite + react-force-graph-2d
- **Dataset:** WikiArt (27 movements, 129 artists)
- **Infrastructure:** Docker Compose

---

## How It Works

1. CLIP encodes the uploaded image into a 1024-dimensional embedding
2. FAISS finds the 15 closest artworks in the index
3. Artist/movement influence weights are computed from the matches
4. Neo4j stores provenance relationships as a graph
5. The frontend renders influence cards, movement bars, and a force graph

---

## Prerequisites

- Python 3.9+
- Node.js 18+
- Docker Desktop

---

## Local Setup

### 1. Clone the repo

```bash
git clone https://github.com/nathamayil/art-provenance-ledger.git
cd art-provenance-ledger
```

### 2. Start Neo4j

```bash
docker compose up -d
```

### 3. Set up Python environment

```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\Activate.ps1       # Windows

pip install -r requirements.txt
```

### 4. Configure environment

Create a `.env` file in the project root:

```env
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=yourpassword
FAISS_INDEX_PATH=<absolute-path-to-project>/data/art_index.faiss
METADATA_PATH=<absolute-path-to-project>/data/metadata.pkl
```

### 5. Seed the database

```bash
# Windows:
$env:PYTHONPATH = "C:\path\to\art-provenance-ledger"
# Mac/Linux:
export PYTHONPATH=$(pwd)

python scripts/seedDB.py
```

This downloads WikiArt, generates CLIP embeddings, builds the FAISS index, and populates Neo4j. Takes ~10-15 minutes on CPU for 500 artworks.

### 6. Start the backend

```bash
uvicorn backend.api.main:app --reload --port 8000
```

API docs at `http://localhost:8000/docs`

### 7. Start the frontend

```bash
cd frontend
npm install
npm run dev
```

App at `http://localhost:5173`

---

## API

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/analyze` | Upload image, returns influence analysis |
| GET | `/api/graph/{image_id}` | Returns Neo4j provenance subgraph |

---

## Future Scope

- Seed with the full WikiArt dataset (80k+ artworks) for richer results
- Text-based search using CLIP text embeddings ("find artworks like Starry Night")
- Fine-tune CLIP on art-specific data for better domain accuracy
- Deploy to Render + Vercel for a live demo URL
- Add GitHub Actions CI with pytest coverage
- Swap local FAISS for Pinecone or Weaviate for scalability

---

## License

MIT
