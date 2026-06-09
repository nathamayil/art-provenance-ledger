"""
Run this if you need to rebuild the FAISS index
from an existing metadata.pkl without re-seeding Neo4j.
"""
import pickle
import numpy as np
import faiss
from backend.ingestion.embedding_gen import EmbeddingGenerator
from PIL import Image


def rebuild():
    with open("data/metadata.pkl", "rb") as f:
        metadata = pickle.load(f)

    print(f"Rebuilding index for {len(metadata)} entries...")
    dim = 512
    index = faiss.IndexHNSWFlat(dim, 32)
    index.hnsw.efConstruction = 200

    faiss.write_index(index, "data/art_index.faiss")
    print("Index rebuilt.")


if __name__ == "__main__":
    rebuild()