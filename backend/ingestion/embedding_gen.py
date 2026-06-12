import torch
import numpy as np
from PIL import Image
from transformers import CLIPProcessor, CLIPModel


class EmbeddingGenerator:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = CLIPModel.from_pretrained(
            "openai/clip-vit-large-patch14"
        ).to(self.device)
        self.processor = CLIPProcessor.from_pretrained(
            "openai/clip-vit-large-patch14"
        )
        print(f"CLIP model loaded on {self.device}")

    def generate_image_embedding(self, image: Image.Image) -> np.ndarray:
        inputs = self.processor(
            images=image,
            return_tensors="pt"
        ).to(self.device)

        with torch.no_grad():
            features = self.model.vision_model(**inputs)

        embedding = features.pooler_output.cpu().numpy().flatten()
        embedding = embedding / np.linalg.norm(embedding)
        return embedding

    def generate_text_embedding(self, text: str) -> np.ndarray:
        inputs = self.processor(
            text=[text],
            return_tensors="pt",
            padding=True
        ).to(self.device)

        with torch.no_grad():
            features = self.model.text_model(**inputs)

        embedding = features.pooler_output.cpu().numpy().flatten()
        embedding = embedding / np.linalg.norm(embedding)
        return embedding