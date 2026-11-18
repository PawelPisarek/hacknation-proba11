"""Raport: JSON z obszarami + obraz PNG z zaznaczonymi ramkami."""
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw


def zapisz(wynik: dict, badany: np.ndarray, katalog: str | Path, nazwa: str, max_szer: int = 2000) -> dict:
    katalog = Path(katalog)
    katalog.mkdir(parents=True, exist_ok=True)
    im = Image.fromarray(np.clip(badany, 0, 255).astype(np.uint8), "L").convert("RGB")
    f = max(1, int(np.ceil(im.width / max_szer)))
    if f > 1:
        im = im.resize((im.width // f, im.height // f))
    dr = ImageDraw.Draw(im)
    for o in wynik["obszary"]:
        x0, y0, x1, y1 = (v // f for v in o["bbox"])
        dr.rectangle([x0 - 2, y0 - 2, x1 + 2, y1 + 2], outline=(255, 0, 0), width=2)
    png = katalog / f"{nazwa}_raport.png"
    im.save(png)
    js = katalog / f"{nazwa}_raport.json"
    js.write_text(json.dumps(wynik, ensure_ascii=False, indent=1))
    return {"png": str(png), "json": str(js)}
