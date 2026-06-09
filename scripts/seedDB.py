from datasets import load_dataset
from backend.ingestion.embedding_gen import EmbeddingGenerator
from backend.graphs.neo4j_client import Neo4jClient
import numpy as np
import faiss
import pickle
import os

os.makedirs("data", exist_ok=True)


def seed():
    generator = EmbeddingGenerator()
    neo4j = Neo4jClient()

    dataset = load_dataset("huggan/wikiart", split="train", streaming=True)

    embeddings = []
    metadata = []

    print("Starting seed... this may take a while.")

    for i, item in enumerate(dataset):
        if i >= 5000:   # Limit to 5000 for initial seed; increase as needed
            break

        artist = item.get("artist", "Unknown")
        movement = item.get("style", "Unknown")
        image = item["image"]

        try:
            embedding = generator.generate_image_embedding(image)
            embeddings.append(embedding)
            metadata.append({
                "artist": artist,
                "movement": movement,
                "title": item.get("title", "Untitled")
            })

            neo4j.create_artwork_node(
                title=item.get("title", "Untitled"),
                artist=artist,
                movement=movement,
                embedding=embedding.tolist()
            )

            if i % 100 == 0:
                print(f"Processed {i} artworks...")

        except Exception as e:
            print(f"Skipping item {i}: {e}")
            continue

    dim = 512
    index = faiss.IndexHNSWFlat(dim, 32)
    index.hnsw.efConstruction = 200
    index.add(np.array(embeddings).astype("float32"))

    faiss.write_index(index, "data/art_index.faiss")
    with open("data/metadata.pkl", "wb") as f:
        pickle.dump(metadata, f)

    print(f"Done. Seeded {len(embeddings)} artworks.")


if __name__ == "__main__":
    seed()