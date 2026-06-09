from PIL import Image
import numpy as np
from io import BytesIO
from sklearn.cluster import KMeans


class ImageProcessor:
    def __init__(self, target_size=(224, 224)):
        self.target_size = target_size

    def load_from_bytes(self, raw_bytes: bytes) -> Image.Image:
        image = Image.open(BytesIO(raw_bytes)).convert("RGB")
        return image

    def compute_perceptual_hash(self, image: Image.Image) -> str:
        small = image.resize((8, 8), Image.LANCZOS).convert("L")
        pixels = list(small.getdata())
        avg = sum(pixels) / len(pixels)
        bits = "".join("1" if p > avg else "0" for p in pixels)
        return hex(int(bits, 2))[2:].zfill(16)

    def extract_color_palette(self, image: Image.Image, n=5) -> list:
        img_array = np.array(image.resize((100, 100)))
        pixels = img_array.reshape(-1, 3).astype(float)
        kmeans = KMeans(n_clusters=n, random_state=42, n_init=10)
        kmeans.fit(pixels)
        palette = kmeans.cluster_centers_.astype(int).tolist()
        return [tuple(c) for c in palette]