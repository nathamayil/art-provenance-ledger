import os
import faiss
import pickle
import numpy as np
from collections import Counter
from dotenv import load_dotenv

load_dotenv()


class InfluenceGraph:
    def __init__(self):
        index_path = os.getenv("FAISS_INDEX_PATH", "data/art_index.faiss")
        metadata_path = os.getenv("METADATA_PATH", "data/metadata.pkl")

        self.index = faiss.read_index(index_path)
        self.index.hnsw.efSearch = 100

        with open(metadata_path, "rb") as f:
            self.metadata = pickle.load(f)

    def find_closest_artworks(self, query_embedding: np.ndarray, top_k=10) -> list:
        query = query_embedding.reshape(1, -1).astype("float32")
        distances, indices = self.index.search(query, top_k)

        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx == -1:
                continue
            meta = self.metadata[idx]
            results.append({**meta, "similarity_score": float(1 - dist)})
        return results

    def build_influence_summary(self, closest: list) -> dict:
        movement_counts = Counter(r["movement"] for r in closest)
        artist_counts = Counter(r["artist"] for r in closest)
        total = len(closest)

        return {
            "movements": [
                {"name": m, "weight": round(c / total, 2)}
                for m, c in movement_counts.most_common(5)
            ],
            "artists": [
                {"name": a, "weight": round(c / total, 2)}
                for a, c in artist_counts.most_common(5)
            ],
            "top_matches": closest[:3]
        }