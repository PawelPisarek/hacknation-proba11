"""Wczytywanie i zapis obrazów .bmp (skala szarości, 8 bit)."""
from pathlib import Path

import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None  # obrazy KAS ~50 MB


def wczytaj(sciezka: str | Path) -> np.ndarray:
    """Obraz jako float32 w skali 0..255 (kolor → skala szarości)."""
    with Image.open(sciezka) as im:
        if im.mode not in ("L", "I;16", "I", "F"):
            im = im.convert("L")
        return np.asarray(im, dtype=np.float32)


def zapisz_bmp(obraz: np.ndarray, sciezka: str | Path) -> None:
    Path(sciezka).parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(np.clip(obraz, 0, 255).astype(np.uint8), "L").save(sciezka, format="BMP")
