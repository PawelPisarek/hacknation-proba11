"""Generator syntetycznych obrazów RTG naczep (skala szarości, ciemne = gęste).

Model: obraz = 255 * wzmocnienie * exp(-A) + szum, gdzie A to mapa tłumienia
(konstrukcja naczepy + opcjonalny ładunek + opcjonalne dodatki).
Para „czysta”: wzorzec i badany to ten sam pojazd (ten sam ładunek), różnią się
szumem, przesunięciem (subpikselowym) i jasnością. Para „dodatek”: jak czysta,
ale w badanym są 1–2 obiekty niebędące elementem konstrukcji (w konstrukcji lub w ładunku).
Prawda: prawda.json z bboxami dodatków w układzie obrazu badanego [x0, y0, x1, y1] (włącznie).
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from scipy import ndimage

from .obrazy import zapisz_bmp


def _tekstura(rng, h, w, skala, siatka=24):
    """Gładki szum 0..1 (mały szum powiększony — tanio też dla dużych obrazów)."""
    gh, gw = max(2, h // max(1, skala)), max(2, w // max(1, skala))
    gh, gw = min(gh, siatka * 8), min(gw, siatka * 8)
    m = rng.random((gh, gw), dtype=np.float32)
    m = ndimage.zoom(m, (h / gh, w / gw), order=1)[:h, :w]
    if m.shape != (h, w):
        m = np.pad(m, ((0, h - m.shape[0]), (0, w - m.shape[1])), mode="edge")
    return m.astype(np.float32)


@dataclass
class Pojazd:
    A: np.ndarray            # mapa tłumienia (konstrukcja + ładunek)
    strefy: dict             # nazwa -> lista prostokątów (y0, y1, x0, x1) do wstawiania dodatków
    A_kon: np.ndarray = None  # sama konstrukcja
    palety: list = None      # [(py0, py1, lx, pw, warstwa)] — warstwa = tłumienie palety (ph x pw)
    granice: tuple = None    # (x0, x1) wnętrza naczepy


def pojazd(rng: np.random.Generator, h: int, w: int, z_ladunkiem: bool) -> Pojazd:
    A = np.zeros((h, w), np.float32)
    s = w / 1000.0  # skala względem szerokości 1000 px
    x0, x1 = int(w * rng.uniform(0.03, 0.07)), int(w * rng.uniform(0.93, 0.97))
    y0, y1 = int(h * rng.uniform(0.10, 0.16)), int(h * rng.uniform(0.68, 0.74))
    sc = max(1, int(3 * s))
    # ściany (rzut boczny: cienka blacha na całej powierzchni) + ramy górna/dolna/przód/tył
    A[y0:y1, x0:x1] += 0.12
    A[y0:y0 + 2 * sc, x0:x1] += 0.9
    A[y1 - 3 * sc:y1, x0:x1] += 1.1
    A[y0:y1, x0:x0 + 3 * sc] += 0.9
    A[y0:y1, x1 - 3 * sc:x1] += 0.9
    # żebra pionowe
    krok = int(w * rng.uniform(0.035, 0.05))
    for x in range(x0 + krok, x1 - sc, krok):
        A[y0:y1, x:x + sc] += 0.35
    # podwozie: dwie podłużnice
    c0 = y1 + int(h * 0.01)
    c1 = c0 + int(h * rng.uniform(0.04, 0.06))
    A[c0:c1, x0 + int(20 * s):x1 - int(10 * s)] += 1.3
    A[c0 + (c1 - c0) // 3:c0 + 2 * (c1 - c0) // 3, x0 + int(20 * s):x1 - int(10 * s)] -= 0.5  # profil C
    # zbiornik / skrzynia narzędziowa
    t0 = int(w * rng.uniform(0.25, 0.40))
    tw = int(w * rng.uniform(0.08, 0.13))
    tt0, tt1 = c1, c1 + int(h * rng.uniform(0.07, 0.10))
    A[tt0:tt1, t0:t0 + tw] += 0.7
    A[tt0:tt0 + sc, t0:t0 + tw] += 0.6
    # osie i koła
    r = int(h * rng.uniform(0.075, 0.09))
    n_osi = int(rng.integers(2, 4))
    xs = x1 - int(w * 0.08) - np.arange(n_osi) * int(2.3 * r)
    yc = c1 + r
    oy, ox = np.ogrid[-r:r + 1, -r:r + 1]
    d = np.hypot(oy, ox).astype(np.float32)
    kolo = (d < r) * 1.6 - (d < 0.45 * r) * 0.9
    for xc in xs:
        ya, xa = yc - r, xc - r
        yb, xb = min(h, yc + r + 1), min(w, xc + r + 1)
        A[ya:yb, xa:xb] += kolo[:yb - ya, :xb - xa]
    # sworzeń / podpory z przodu
    A[c1:c1 + int(h * 0.12), x0 + int(60 * s):x0 + int(60 * s) + 2 * sc] += 1.0
    strefy = {
        "konstrukcja": [(c0, c1, x0 + int(30 * s), x1 - int(30 * s)),
                        (tt0, tt1, t0, t0 + tw),
                        (y1 - int(h * 0.06), y1, x0 + int(10 * s), x1 - int(10 * s))],
        "ladunek": [],
    }
    A_kon = A.copy()
    palety = []
    if z_ladunkiem:
        lx = x0 + int(10 * s)
        while lx < x1 - int(80 * s):
            pw = int(w * rng.uniform(0.06, 0.12))
            ph = int((y1 - y0) * rng.uniform(0.35, 0.85))
            if lx + pw > x1 - int(10 * s):
                break
            if rng.random() < 0.85:
                py1 = y1 - 3 * sc
                py0 = py1 - ph
                gest = rng.uniform(0.25, 0.9)
                tex = _tekstura(rng, ph, pw, max(2, int(12 * s)))
                warstwa = (gest * (0.7 + 0.6 * tex)).astype(np.float32)
                warstwa[ph - 2 * sc:, :] += 0.5  # paleta
                A[py0:py1, lx:lx + pw] += warstwa
                palety.append((py0, py1, lx, pw, warstwa))
                strefy["ladunek"].append((py0, py1 - 2 * sc, lx, lx + pw))
            lx += pw + int(w * rng.uniform(0.005, 0.03))
    if not strefy["ladunek"]:
        strefy["ladunek"].append((y0 + int(h * 0.1), y1 - int(h * 0.1), x0 + int(40 * s), x1 - int(40 * s)))
    return Pojazd(A, strefy, A_kon, palety, (x0 + int(10 * s), x1 - int(10 * s)))


def dodatek(rng, A_shape, strefa, s):
    """Maska dodatku (prostokąt albo nieregularny kształt) w strefie; zwraca (maska, tłumienie)."""
    h, w = A_shape
    zy0, zy1, zx0, zx1 = strefa
    zh, zw = zy1 - zy0, zx1 - zx0
    bw = int(min(zw * 0.8, w * rng.uniform(0.02, 0.07)))
    bh = int(min(zh * 0.8, max(4 * s, bw * rng.uniform(0.3, 1.2))))
    bw, bh = max(bw, 4), max(bh, 4)
    py = int(rng.integers(zy0, max(zy0 + 1, zy1 - bh)))
    px = int(rng.integers(zx0, max(zx0 + 1, zx1 - bw)))
    m = np.zeros((h, w), bool)
    if rng.random() < 0.5:
        m[py:py + bh, px:px + bw] = True
    else:
        yy, xx = np.mgrid[0:bh, 0:bw]
        el = ((yy - bh / 2) / (bh / 2)) ** 2 + ((xx - bw / 2) / (bw / 2)) ** 2
        tex = _tekstura(rng, bh, bw, max(2, bw // 4))
        m[py:py + bh, px:px + bw] = el + 0.6 * (tex - 0.5) < 0.8
    return m, float(rng.uniform(0.15, 0.6))


def renderuj(rng, A, dx, dy, wzm, szum):
    if dx or dy:
        A = ndimage.shift(A, (dy, dx), order=1, mode="constant", cval=0.0)
    I = 255.0 * 0.93 * wzm * np.exp(-A)
    I += szum * rng.standard_normal(A.shape, dtype=np.float32)
    I += rng.normal(0, szum * 0.5, (1, A.shape[1])).astype(np.float32)  # pasy detektora
    return I, A


def _uloz_inaczej(rng, p: Pojazd, w):
    """Ten sam ładunek, inaczej ułożony: każda paleta przesunięta, część odwrócona. Zwraca (A_ladunku, przesunięcia)."""
    h = p.A.shape[0]
    A = np.zeros_like(p.A)
    lo, hi = p.granice
    przes = []
    prawy_brzeg = lo
    for (py0, py1, lx, pw, warstwa) in p.palety:
        nx = int(round(lx + rng.uniform(-0.02, 0.02) * w))
        nx = max(nx, prawy_brzeg + 1)
        nx = min(nx, hi - pw)
        nx = max(nx, lo)
        war = warstwa[:, ::-1] if rng.random() < 0.3 else warstwa
        A[py0:py1, nx:nx + pw] += war[:, :max(0, min(pw, w - nx))]
        prawy_brzeg = nx + pw
        przes.append((lx, pw, nx - lx))
    return A, przes


def _przes_ladunku(przes, mx0, mx1):
    """Przesunięcie palety, w której leży dodatek (po środku x maski)."""
    cx = (mx0 + mx1) / 2
    for lx, pw, d in przes:
        if lx <= cx < lx + pw:
            return d
    return 0


def _mapa_x(rng, w, dx, s):
    """Źródłowe x dla każdej kolumny badanego: przesunięcie + rozciągnięcie + zmienna prędkość przejazdu."""
    x = np.arange(w, dtype=np.float64)
    skala = rng.uniform(0.97, 1.03)
    amp, f, faza = rng.uniform(0, 0.004) * w, rng.uniform(0.5, 2.0), rng.uniform(0, 2 * np.pi)
    c = w / 2
    return (x - dx - c) / skala + c + amp * np.sin(2 * np.pi * f * x / w + faza)


def _zastosuj_x(A, xsrc):
    w = A.shape[1]
    x0 = np.clip(np.floor(xsrc).astype(np.int64), 0, w - 2)
    fr = np.clip(xsrc - x0, 0, 1).astype(np.float32)
    out = A[:, x0] * (1 - fr) + A[:, x0 + 1] * fr
    out[:, (xsrc < 0) | (xsrc > w - 1)] = 0.0
    return out


def _artefakty(rng, I, szum):
    """Pasy detektora: wzmocnienie kolumn (wahania źródła w czasie) i wierszy (elementy detektora), martwy wiersz."""
    h, w = I.shape
    kol = 1 + 0.01 * rng.standard_normal(w) + 0.03 * (_tekstura(rng, 1, w, max(2, w // 40))[0] - 0.5)
    for _ in range(int(rng.integers(1, 5))):
        x = int(rng.integers(0, w)); sz = int(rng.integers(1, max(2, w // 200)))
        kol[x:x + sz] *= rng.uniform(0.94, 1.06)
    wie = 1 + 0.015 * rng.standard_normal(h)
    if rng.random() < 0.3:
        wie[int(rng.integers(0, h))] *= 0.3
    return I * wie[:, None].astype(np.float32) * kol[None, :].astype(np.float32)


def _para_trudna(rng, katalog, pid, rodzaj, h, w, s, pusty_wzorzec):
    p = pojazd(rng, h, w, z_ladunkiem=pusty_wzorzec or bool(rng.random() < 0.7))
    sz = rng.uniform(1.5, 3.5)
    Iw, _ = renderuj(rng, p.A_kon if pusty_wzorzec else p.A, 0, 0, 1.0, sz)
    Iw = _artefakty(rng, Iw, sz)
    A_lad, przes = _uloz_inaczej(rng, p, w)
    A_b = p.A_kon + A_lad
    maski, miejsca = [], []
    if rodzaj == "dodatek":
        for _ in range(int(rng.integers(1, 3))):
            miejsce = "konstrukcja" if rng.random() < 0.5 else "ladunek"
            strefa = p.strefy[miejsce][int(rng.integers(len(p.strefy[miejsce])))]
            m, t = dodatek(rng, p.A.shape, strefa, s)
            if miejsce == "ladunek":  # dodatek jedzie razem ze swoją paletą
                xs = np.nonzero(m.any(axis=0))[0]
                m = np.roll(m, _przes_ladunku(przes, xs.min(), xs.max()), axis=1)
            A_b[m] += t
            maski.append(m)
            miejsca.append(miejsce)
    dx, dy = rng.uniform(-12, 12) * s, rng.uniform(-4, 4) * s
    xsrc = _mapa_x(rng, w, dx, s)
    A_b = _zastosuj_x(A_b, xsrc)
    if dy:
        A_b = ndimage.shift(A_b, (dy, 0), order=1, mode="constant", cval=0.0)
    sz = rng.uniform(1.5, 3.5)
    Ib, _ = renderuj(rng, A_b, 0, 0, rng.uniform(0.88, 1.12), sz)
    Ib = _artefakty(rng, Ib, sz)
    bboxy = []
    for m in maski:
        ys = np.nonzero(m.any(axis=1))[0]
        xs = np.nonzero(m.any(axis=0))[0]
        kol = np.nonzero((xsrc >= xs.min() - 0.5) & (xsrc <= xs.max() + 0.5))[0]
        bboxy.append([int(kol.min()), max(0, int(np.floor(ys.min() + dy))),
                      int(kol.max()), min(h - 1, int(np.ceil(ys.max() + dy)))])
    zapisz_bmp(Iw, katalog / f"{pid}_wzorzec.bmp")
    zapisz_bmp(Ib, katalog / f"{pid}_badany.bmp")
    return {"id": pid, "wzorzec": f"{pid}_wzorzec.bmp", "badany": f"{pid}_badany.bmp",
            "etykieta": rodzaj, "dodatki": [{"bbox": b, "miejsce": m} for b, m in zip(bboxy, miejsca)],
            "przesuniecie": [round(dx, 2), round(dy, 2)]}


def generuj_zbior(katalog: str | Path, n_czystych: int, n_dodatek: int, h: int = 360, w: int = 1000,
                  ziarno: int = 0, trudny: bool = False, pusty_wzorzec: bool = False) -> dict:
    """trudny: ładunek inaczej ułożony, rozciągnięcie w osi jazdy, pasy detektora.
    pusty_wzorzec: wzorzec bez ładunku, badany z ładunkiem (dodatki w konstrukcji i w ładunku)."""
    if pusty_wzorzec:
        trudny = True
    katalog = Path(katalog)
    katalog.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(ziarno)
    s = w / 1000.0
    pary = []
    rodzaje = ["czysty"] * n_czystych + ["dodatek"] * n_dodatek
    for i, rodzaj in enumerate(rodzaje):
        pid = f"para_{i:03d}"
        if trudny:
            pary.append(_para_trudna(rng, katalog, pid, rodzaj, h, w, s, pusty_wzorzec))
            continue
        p = pojazd(rng, h, w, z_ladunkiem=bool(rng.random() < 0.7))
        Iw, _ = renderuj(rng, p.A, 0, 0, 1.0, rng.uniform(1.5, 3.5))
        A_b = p.A.copy()
        bboxy, miejsca = [], []
        maski = []
        if rodzaj == "dodatek":
            for _ in range(int(rng.integers(1, 3))):
                miejsce = "konstrukcja" if rng.random() < 0.5 else "ladunek"
                strefa = p.strefy[miejsce][int(rng.integers(len(p.strefy[miejsce])))]
                m, t = dodatek(rng, p.A.shape, strefa, s)
                A_b[m] += t
                maski.append(m)
                miejsca.append(miejsce)
        dx, dy = rng.uniform(-12, 12) * s, rng.uniform(-4, 4) * s
        Ib, _ = renderuj(rng, A_b, dx, dy, rng.uniform(0.88, 1.12), rng.uniform(1.5, 3.5))
        for m in maski:
            ys, xs = np.nonzero(m)
            x0b, x1b = int(np.floor(xs.min() + dx)), int(np.ceil(xs.max() + dx))
            y0b, y1b = int(np.floor(ys.min() + dy)), int(np.ceil(ys.max() + dy))
            bboxy.append([max(0, x0b), max(0, y0b), min(w - 1, x1b), min(h - 1, y1b)])
        zapisz_bmp(Iw, katalog / f"{pid}_wzorzec.bmp")
        zapisz_bmp(Ib, katalog / f"{pid}_badany.bmp")
        pary.append({"id": pid, "wzorzec": f"{pid}_wzorzec.bmp", "badany": f"{pid}_badany.bmp",
                     "etykieta": rodzaj, "dodatki": [{"bbox": b, "miejsce": m} for b, m in zip(bboxy, miejsca)],
                     "przesuniecie": [round(dx, 2), round(dy, 2)]})
    prawda = {"rozmiar": [w, h], "ziarno": ziarno, "trudny": trudny, "pusty_wzorzec": pusty_wzorzec, "pary": pary}
    (katalog / "prawda.json").write_text(json.dumps(prawda, ensure_ascii=False, indent=1))
    return prawda
