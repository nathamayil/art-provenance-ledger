from fastapi import APIRouter, UploadFile, File, HTTPException
from PIL import Image
import uuid

from backend.ingestion.image_processor import ImageProcessor
from backend.ingestion.embedding_gen import EmbeddingGenerator
from backend.graphs.influence_graph import InfluenceGraph
from backend.graphs.neo4j_client import Neo4jClient

router = APIRouter()
processor = ImageProcessor()
generator = EmbeddingGenerator()
influence_graph = InfluenceGraph()
neo4j = Neo4jClient()


@router.post("/analyze")
async def analyze_image(file: UploadFile = File(...)):
    raw = await file.read()

    if file.content_type not in ["image/jpeg", "image/png", "image/webp"]:
        raise HTTPException(400, "Unsupported file type")

    image = processor.load_from_bytes(raw)
    phash = processor.compute_perceptual_hash(image)
    palette = processor.extract_color_palette(image)
    embedding = generator.generate_image_embedding(image)
    closest = influence_graph.find_closest_artworks(embedding, top_k=15)
    summary = influence_graph.build_influence_summary(closest)

    image_id = str(uuid.uuid4())
    neo4j.create_influence_edges(image_id, summary["artists"])

    return {
        "image_id": image_id,
        "perceptual_hash": phash,
        "color_palette": palette,
        "influence_summary": summary
    }


@router.get("/graph/{image_id}")
async def get_graph(image_id: str):
    graph_data = neo4j.get_influence_subgraph(image_id)
    return graph_data