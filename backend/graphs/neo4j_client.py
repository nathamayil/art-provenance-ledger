import os
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()


class Neo4jClient:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            os.getenv("NEO4J_URI", "bolt://localhost:7687"),
            auth=(
                os.getenv("NEO4J_USER", "neo4j"),
                os.getenv("NEO4J_PASSWORD", "yourpassword")
            )
        )

    def create_artwork_node(self, title, artist, movement, embedding):
        with self.driver.session() as session:
            session.run("""
                MERGE (a:Artist {name: $artist})
                MERGE (m:Movement {name: $movement})
                MERGE (a)-[:BELONGS_TO]->(m)
                CREATE (art:Artwork {title: $title, artist: $artist, movement: $movement})
                MERGE (art)-[:CREATED_BY]->(a)
                MERGE (art)-[:PART_OF]->(m)
            """, artist=artist, movement=movement, title=title)

    def create_influence_edges(self, uploaded_image_id: str, influences: list):
        with self.driver.session() as session:
            session.run("""
                MERGE (u:UploadedImage {id: $id})
            """, id=uploaded_image_id)

            for influence in influences:
                session.run("""
                    MATCH (u:UploadedImage {id: $id})
                    MATCH (a:Artist {name: $artist})
                    MERGE (u)-[:INFLUENCED_BY {weight: $weight, score: $score}]->(a)
                """,
                id=uploaded_image_id,
                artist=influence["artist"],
                weight=influence["weight"],
                score=influence.get("similarity_score", 0.0))

    def get_influence_subgraph(self, image_id: str) -> dict:
        with self.driver.session() as session:
            result = session.run("""
                MATCH (u:UploadedImage {id: $id})-[r:INFLUENCED_BY]->(a:Artist)
                MATCH (a)-[:BELONGS_TO]->(m:Movement)
                RETURN u, r, a, m
            """, id=image_id)

            nodes, links = [], []
            seen = set()

            for record in result:
                artist = record["a"]["name"]
                movement = record["m"]["name"]
                weight = record["r"]["weight"]

                if artist not in seen:
                    nodes.append({"id": artist, "type": "artist"})
                    seen.add(artist)
                if movement not in seen:
                    nodes.append({"id": movement, "type": "movement"})
                    seen.add(movement)

                links.append({"source": image_id, "target": artist, "value": weight})
                links.append({"source": artist, "target": movement, "value": 1})

            nodes.append({"id": image_id, "type": "query"})
            return {"nodes": nodes, "links": links}