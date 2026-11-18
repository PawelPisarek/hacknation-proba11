"""Metoda v1: odporna na skan „jak prawdziwy”.

1. Wyrównanie pasów detektora: przesunięcie log-jasności wierszy (z kolumn powietrza przy lewym/prawym brzegu)
   i kolumn (z wierszy powietrza u góry), osobno dla wzorca i badanego.
2. Rejestracja: globalne przesunięcie (korelacja fazowa), potem nieliniowe dopasowanie w osi jazdy:
   przesunięcie u(x) z pasów pionowych (NCC na obrazie górnoprzepustowym), grubo → odporna prosta → dokładnie.
3. Różnica „badany ciemniejszy niż najciemniejszy wzorzec w otoczeniu ±R w poziomie” — toleruje przesunięte palety
   i resztki rozciągnięcia; normalizacja szumu jak w v0; próg k·MAD, obszary ≥ min_pole.
"""
from __future__ import annotations

import numpy as np
from scipy import ndimage

from .detektor import _zmniejsz, przesuniecie


def wyrownaj_pasy(L, brzeg_x=0.008, brzeg_y=0.06):
    h, w = L.shape
    bx, by = max(3, int(w * brzeg_x)), max(3, int(h * brzeg_y))
    r = np.median(np.concatenate([L[:, :bx], L[:, -bx:]], axis=1), axis=1)
    L = L - (r - np.median(r))[:, None]
    c = np.median(L[:by, :], axis=0)
    return L - (c - np.median(c))[None, :]


def _ncc_przes(Fw, Fb, x0, x1, srodek, zakres):
    """Najlepsze przesunięcie s (Fb[:, x] ≈ Fw[:, x - s]) w [srodek-zakres, srodek+zakres] dla okna [x0, x1)."""
    w = Fw.shape[1]
    b = Fb[:, x0:x1]
    b = b - b.mean()
    nb = np.sqrt((b * b).sum()) + 1e-9
    wyniki = []
    for s in range(int(srodek) - zakres, int(srodek) + zakres + 1):
        a0, a1 = x0 - s, x1 - s
        if a0 < 0 or a1 > w:
            wyniki.append(-1.0)
            continue
        a = Fw[:, a0:a1]
        a = a - a.mean()
        wyniki.append(float((a * b).sum() / (np.sqrt((a * a).sum()) * nb + 1e-9)))
    wyniki = np.array(wyniki)
    i = int(np.argmax(wyniki))
    sub = 0.0
    if 0 < i < len(wyniki) - 1:
        lo, mid, hi = wyniki[i - 1], wyniki[i], wyniki[i + 1]
        dd = lo - 2 * mid + hi
        sub = 0.0 if dd == 0 else 0.5 * (lo - hi) / dd
    return int(srodek) - zakres + i + sub, float(wyniki[i])


def mapa_przesuniec(LW, LB, dx0, hp=3.0, pas=0.05, zakres=0.03, kara=0.05, max_skok=2):
    """u(x): przesunięcie kolumn badanego względem wzorca (B[:, x] ≈ W[:, x - u(x)]).

    NCC pasów pionowych dla każdego przesunięcia (macierz pas × przesunięcie), potem programowanie dynamiczne
    z karą za skok między sąsiednimi pasami — rozciągnięcie jest gładkie, a żebra okresowe (bez kary łapie sąsiednie żebro).
    """
    h, w = LW.shape
    Fw = (LW - ndimage.gaussian_filter1d(LW, hp, axis=1))[::4]  # co 4. wiersz: cechy pionowe
    Fb = (LB - ndimage.gaussian_filter1d(LB, hp, axis=1))[::4]
    pw = max(16, int(pas * w))
    krok = pw // 2
    starty = np.arange(0, w - pw + 1, krok)
    S = max(4, int(zakres * w))
    przes = np.arange(int(round(dx0)) - S, int(round(dx0)) + S + 1)
    B2 = np.concatenate([[0], np.cumsum((Fb * Fb).sum(0))])
    C = np.full((len(starty), len(przes)), -1.0)
    for j, s in enumerate(przes):
        idx = np.arange(w) - s
        ok = (idx >= 0) & (idx < w)
        A = Fw[:, np.clip(idx, 0, w - 1)] * ok
        P = np.concatenate([[0], np.cumsum((A * Fb).sum(0))])
        A2 = np.concatenate([[0], np.cumsum((A * A).sum(0))])
        okc = np.concatenate([[0], np.cumsum(~ok)])
        e = starty + pw
        num = P[e] - P[starty]
        den = np.sqrt((A2[e] - A2[starty]) * (B2[e] - B2[starty])) + 1e-9
        c = num / den
        c[(okc[e] - okc[starty]) > 0] = -1.0
        C[:, j] = c
    # programowanie dynamiczne: maks. suma NCC − kara·|skok|, |skok| ≤ max_skok
    n, m = C.shape
    D = C[0].copy()
    wstecz = np.zeros((n, m), np.int64)
    for i in range(1, n):
        kand = np.full((2 * max_skok + 1, m), -np.inf)
        for t, dd in enumerate(range(-max_skok, max_skok + 1)):
            src = np.arange(m) - dd
            ok = (src >= 0) & (src < m)
            kand[t, ok] = D[src[ok]] - kara * abs(dd)
        best = np.argmax(kand, axis=0)
        wstecz[i] = np.arange(m) - (best - max_skok)
        D = kand[best, np.arange(m)] + C[i]
    sc = np.empty(n, np.int64)
    sc[-1] = int(np.argmax(D))
    for i in range(n - 1, 0, -1):
        sc[i - 1] = wstecz[i, sc[i]]
    u = przes[sc].astype(np.float64)
    for i in range(n):  # subpiksel z paraboli
        j = sc[i]
        if 0 < j < m - 1:
            lo, mid, hi = C[i, j - 1], C[i, j], C[i, j + 1]
            dd = lo - 2 * mid + hi
            if dd < 0:
                u[i] += 0.5 * (lo - hi) / dd
    return np.interp(np.arange(w), starty + pw / 2, u)


def przesuniecie_ladunku(nW, nB, R, blok):
    h, w = nW.shape
    a, b = nW[::2, ::2], nB[::2, ::2]
    R2 = max(1, R // 2)
    naj = np.full(b.shape, np.inf, np.float32)
    s_naj = np.zeros(b.shape, np.int16)
    for s in range(-R2, R2 + 1):
        idx = np.clip(np.arange(b.shape[1]) - s, 0, b.shape[1] - 1)
        E = ndimage.uniform_filter(np.abs(a[:, idx] - b), 9)
        lepsze = E < naj - 1e-6 * (s != 0)  # przy remisie zostaje mniejsze |s| (zaczynamy od -R2, więc korekta niżej)
        naj = np.where(lepsze, E, naj)
        s_naj = np.where(lepsze, s, s_naj)
    E0 = ndimage.uniform_filter(np.abs(a - b), 9)
    s_naj = np.where(E0 <= naj * 1.05, 0, s_naj)  # brak wyraźnej poprawy → bez przesunięcia
    s_naj = ndimage.median_filter(s_naj, size=max(3, blok // 2))
    return np.repeat(np.repeat(s_naj * 2, 2, axis=0), 2, axis=1)[:h, :w].astype(np.int64)


def wykryj(wzorzec: np.ndarray, badany: np.ndarray, k: float = 4.0, sigma: float = 2.0,
           min_pole: int = 15, max_szer: int = 2000, tol_x: float = 0.025, tol_y: int = 1, pasmo: float = 3.0, tol_h: float = 0.01, blok: int = 31, kara: float = 0.05) -> dict:
    f = max(1, int(np.ceil(wzorzec.shape[1] / max_szer)))
    W = _zmniejsz(wzorzec.astype(np.float32), f)
    B = _zmniejsz(badany.astype(np.float32), f)
    h, w = min(W.shape[0], B.shape[0]), min(W.shape[1], B.shape[1])
    W, B = W[:h, :w], B[:h, :w]
    LW = wyrownaj_pasy(np.log(W + 1.0))
    LB = wyrownaj_pasy(np.log(B + 1.0))
    dy, dx = przesuniecie(LW, LB)
    LWy = ndimage.shift(LW, (dy, 0), order=1, mode="nearest")
    u = mapa_przesuniec(LWy, LB, dx, kara=kara)
    xsrc = np.arange(w) - u
    x0 = np.clip(np.floor(xsrc).astype(np.int64), 0, w - 2)
    fr = np.clip(xsrc - x0, 0, 1).astype(np.float32)
    LWs = LWy[:, x0] * (1 - fr) + LWy[:, x0 + 1] * fr
    wazne = np.ones((h, w), bool)
    m = int(np.ceil(abs(dy))) + 2
    wazne[:m, :] = wazne[-m:, :] = False
    wazne[:, (xsrc < 2) | (xsrc > w - 3)] = False
    wazne[:, :2] = wazne[:, -2:] = False
    R = max(1, int(round(tol_x * w)))
    LWg = ndimage.gaussian_filter(LWs, 1.0)
    LB = ndimage.gaussian_filter(LB, 1.0)  # to samo rozmycie co wzorzec (interpolacja + filtr) — inaczej cienkie żebra „ciemnieją”
    # poziom szumu i jasności z różnicy bez tolerancji (3x3) — tolerancja tylko obniża d
    d0 = ndimage.minimum_filter(LWg, size=3) - LB
    off = np.median(d0[wazne])
    d0 -= off
    jasne = wazne & (LWs > np.percentile(LWs[wazne], 70))
    s_I = np.median(np.abs(d0[jasne] - np.median(d0[jasne]))) * 1.4826 * np.median(np.exp(LWs[jasne])) + 1e-6
    sig = np.sqrt(2.0) * s_I / (np.exp(LWs) + 1.0)
    z0 = ndimage.gaussian_filter(d0 / sig, sigma)
    mad = np.median(np.abs(z0[wazne] - np.median(z0[wazne]))) * 1.4826 + 1e-6
    # dwa pasma osobno: drobne (żebra, krawędzie) i gładkie (palety) — w log tłumienia się sumują,
    # więc żebro na przesuniętej palecie jest ciemniejsze niż każde z nich we wzorcu; w pasmach już nie
    rozm = (2 * tol_y + 1, 2 * R + 1)
    nW = ndimage.gaussian_filter1d(LWg, pasmo, axis=1)
    nB = ndimage.gaussian_filter1d(LB, pasmo, axis=1)
    rozm_n = (2 * tol_y + 1, 2 * max(1, int(round(tol_h * w))) + 1)
    hW, hB = LWg - nW, LB - nB
    # ładunek: lokalne przesunięcie poziome s*(y, x) z dopasowania bloków w paśmie gładkim (na 1/2 rozdzielczości),
    # wygładzone medianą — paleta rusza się w całości, dodatek jest od niej mniejszy, więc go nie „wyjaśni”
    sstar = przesuniecie_ladunku(nW, nB, R, blok)
    yy = np.arange(h)[:, None]
    xs = np.clip(np.arange(w)[None, :] - sstar, 0, w - 1)
    nWs, hWs = nW[yy, xs], hW[yy, xs]
    # badany wyjaśniony przez wzorzec bez przesunięcia (konstrukcja) albo z przesunięciem (ładunek) — bierzemy lepsze
    dl = np.minimum(ndimage.minimum_filter(nW, size=rozm_n), ndimage.minimum_filter(nWs, size=rozm_n)) - nB
    dh = np.minimum(ndimage.minimum_filter(hW, size=rozm_n), ndimage.minimum_filter(hWs, size=rozm_n)) - hB
    d = dl + dh - off
    d = ndimage.gaussian_filter(d / sig, sigma)
    d[~wazne] = 0
    maska = ndimage.binary_opening(d > k * mad, iterations=1)
    etyk, _ = ndimage.label(maska)
    obszary = []
    for i, sl in enumerate(ndimage.find_objects(etyk), start=1):
        pole = int((etyk[sl] == i).sum())
        if pole < min_pole:
            continue
        y0, y1, xa, xb = sl[0].start, sl[0].stop - 1, sl[1].start, sl[1].stop - 1
        sila = float(d[sl][etyk[sl] == i].mean() / mad)
        obszary.append({"bbox": [xa * f, y0 * f, (xb + 1) * f - 1, (y1 + 1) * f - 1],
                        "pole_px": pole * f * f, "sila": round(sila, 2)})
    obszary.sort(key=lambda o: -o["sila"])
    return {"alarm": bool(obszary), "obszary": obszary,
            "przesuniecie": [round(float(u.mean()) * f, 2), round(dy * f, 2)],
            "rozciagniecie_px": round(float(u.max() - u.min()) * f, 2), "skala": f}
