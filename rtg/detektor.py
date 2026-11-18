"""Metoda bazowa: rejestracja (korelacja fazowa) + różnica w dziedzinie log + próg.

Dodatki zwiększają tłumienie → badany ciemniejszy niż wzorzec. Liczymy
d = log(wzorzec) - log(badany) po dopasowaniu przesunięcia i jasności (mediana),
wygładzamy, progujemy k * sigma (MAD), zostawiamy spójne obszary ≥ min_pole.
Duże obrazy (~50 MB) liczone w zmniejszeniu (średnia blokowa) do szer. ≤ max_szer.
"""
from __future__ import annotations

import numpy as np
from scipy import ndimage


def _zmniejsz(I, f):
    if f == 1:
        return I
    h, w = (I.shape[0] // f) * f, (I.shape[1] // f) * f
    return I[:h, :w].reshape(h // f, f, w // f, f).mean(axis=(1, 3))


def przesuniecie(a, b):
    """(dy, dx) takie, że b ≈ a przesunięte o (dy, dx); subpiksel z paraboli."""
    a = a - a.mean()
    b = b - b.mean()
    okno = np.outer(np.hanning(a.shape[0]), np.hanning(a.shape[1])).astype(np.float32)
    R = np.fft.rfft2(b * okno) * np.conj(np.fft.rfft2(a * okno))
    R /= np.abs(R) + 1e-9
    r = np.fft.irfft2(R, s=a.shape)
    py, px = np.unravel_index(np.argmax(r), r.shape)

    def sub(c, n, wzdl):
        lo, hi = wzdl((c - 1) % n), wzdl((c + 1) % n)
        mid = wzdl(c)
        d = lo - 2 * mid + hi
        return 0.0 if d == 0 else 0.5 * (lo - hi) / d

    dy = py + sub(py, r.shape[0], lambda k: r[k, px])
    dx = px + sub(px, r.shape[1], lambda k: r[py, k])
    if dy > r.shape[0] / 2:
        dy -= r.shape[0]
    if dx > r.shape[1] / 2:
        dx -= r.shape[1]
    return float(dy), float(dx)


def wykryj(wzorzec: np.ndarray, badany: np.ndarray, k: float = 4.0, sigma: float = 2.0,
           min_pole: int = 30, max_szer: int = 2000) -> dict:
    f = max(1, int(np.ceil(wzorzec.shape[1] / max_szer)))
    W = _zmniejsz(wzorzec.astype(np.float32), f)
    B = _zmniejsz(badany.astype(np.float32), f)
    h, w = min(W.shape[0], B.shape[0]), min(W.shape[1], B.shape[1])
    W, B = W[:h, :w], B[:h, :w]
    LW, LB = np.log(W + 1.0), np.log(B + 1.0)
    dy, dx = przesuniecie(LW, LB)
    LWs = ndimage.shift(LW, (dy, dx), order=1, mode="nearest")
    wazne = np.ones((h, w), bool)
    m = int(np.ceil(max(abs(dx), abs(dy)))) + 2
    wazne[:m, :] = wazne[-m:, :] = wazne[:, :m] = wazne[:, -m:] = False
    # tolerancja krawędzi: badany musi być ciemniejszy niż najciemniejszy sąsiad wzorca (3x3)
    d = ndimage.minimum_filter(LWs, size=3) - LB
    d -= np.median(d[wazne])  # zmiana jasności = stałe przesunięcie w log
    # szum w dziedzinie log rośnie w ciemnych miejscach (~ sigma_I / I): normalizujemy
    jasne = wazne & (W > np.percentile(W[wazne], 70))
    s_I = np.median(np.abs(d[jasne] - np.median(d[jasne]))) * 1.4826 * np.median(W[jasne]) + 1e-6
    sig = np.sqrt(2.0) * s_I / (np.exp(LWs) + 1.0)
    d = ndimage.gaussian_filter(d / sig, sigma)
    d[~wazne] = 0
    mad = np.median(np.abs(d[wazne])) * 1.4826 + 1e-6
    maska = d > k * mad
    maska = ndimage.binary_opening(maska, iterations=1)
    etyk, n = ndimage.label(maska)
    obszary = []
    for i, sl in enumerate(ndimage.find_objects(etyk), start=1):
        pole = int((etyk[sl] == i).sum())
        if pole < min_pole:
            continue
        y0, y1, x0, x1 = sl[0].start, sl[0].stop - 1, sl[1].start, sl[1].stop - 1
        sila = float(d[sl][etyk[sl] == i].mean() / mad)
        obszary.append({"bbox": [x0 * f, y0 * f, (x1 + 1) * f - 1, (y1 + 1) * f - 1],
                        "pole_px": pole * f * f, "sila": round(sila, 2)})
    obszary.sort(key=lambda o: -o["sila"])
    return {"alarm": bool(obszary), "obszary": obszary,
            "przesuniecie": [round(dx * f, 2), round(dy * f, 2)], "skala": f}
