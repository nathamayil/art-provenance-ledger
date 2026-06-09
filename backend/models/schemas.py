from pydantic import BaseModel
from typing import List, Optional


class ArtistInfluence(BaseModel):
    name: str
    weight: float


class MovementInfluence(BaseModel):
    name: str
    weight: float


class InfluenceSummary(BaseModel):
    movements: List[MovementInfluence]
    artists: List[ArtistInfluence]
    top_matches: List[dict]


class AnalyzeResponse(BaseModel):
    image_id: str
    perceptual_hash: str
    color_palette: List[tuple]
    influence_summary: InfluenceSummary


class GraphNode(BaseModel):
    id: str
    type: str


class GraphLink(BaseModel):
    source: str
    target: str
    value: float


class GraphResponse(BaseModel):
    nodes: List[GraphNode]
    links: List[GraphLink]