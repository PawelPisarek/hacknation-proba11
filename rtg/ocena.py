"""Skrypt oceny wg „Sposób testowania” (docs/zadanie.md §6).

FP: obraz czysty, na którym metoda zgłosiła jakikolwiek obszar.
FN: obraz z dodatkiem, w którym żadna ramka nie trafia w dodatek (decyzja Szefa 08:15).
Trafienie: ramka metody nakłada się na bbox prawdy (IoU>0) albo środek jednej leży w drugiej.
Osobno: dodatki trafione (każdy dodatek z osobna) i fałszywe ramki na obrazach z dodatkiem.
"""
from __future__ import annotations

import json
import time
from pathlib import Path

from .detektor import wykryj
from .obrazy import wczytaj


def nakladaja(a, b):
    return a[0] <= b[2] and b[0] <= a[2] and a[1] <= b[3] and b[1] <= a[3]


def trafiony(prawda_bbox, ramki):
    # środek jednej ramki w drugiej implikuje nakładanie, więc wystarcza IoU>0
    return any(nakladaja(prawda_bbox, r) for r in ramki)


def ocen(katalog: str | Path, metoda=wykryj, **param) -> dict:
    katalog = Path(katalog)
    prawda = json.loads((katalog / "prawda.json").read_text())
    fp = fn = n_cz = n_dod = trafione = wszystkie = falszywe_ramki = 0
    czasy, szczegoly = [], []
    for p in prawda["pary"]:
        W, B = wczytaj(katalog / p["wzorzec"]), wczytaj(katalog / p["badany"])
        t = time.perf_counter()
        wyn = metoda(W, B, **param)
        czasy.append(time.perf_counter() - t)
        ramki = [o["bbox"] for o in wyn["obszary"]]
        if p["etykieta"] == "czysty":
            n_cz += 1
            blad = "FP" if ramki else ""
            fp += bool(ramki)
        else:
            n_dod += 1
            traf = [trafiony(d["bbox"], ramki) for d in p["dodatki"]]
            trafione += sum(traf)
            wszystkie += len(traf)
            falszywe_ramki += sum(not any(nakladaja(r, d["bbox"]) for d in p["dodatki"]) for r in ramki)
            blad = "FN" if not any(traf) else ""
            fn += not any(traf)
        szczegoly.append({"id": p["id"], "etykieta": p["etykieta"], "ramki": len(ramki), "blad": blad})
    return {"FP": fp, "n_czystych": n_cz, "FN": fn, "n_dodatek": n_dod,
            "dodatki_trafione": trafione, "dodatki": wszystkie, "falszywe_ramki_na_dodatkach": falszywe_ramki,
            "czas_na_obraz_s": sum(czasy) / max(1, len(czasy)), "szczegoly": szczegoly}


def linia(w: dict) -> str:
    pr = lambda a, b: f"{a}/{b} ({100 * a / max(1, b):.0f}%)"
    return (f"FP {pr(w['FP'], w['n_czystych'])} | FN {pr(w['FN'], w['n_dodatek'])} | "
            f"dodatki trafione {w['dodatki_trafione']}/{w['dodatki']} | "
            f"fałszywe ramki na obrazach z dodatkiem {w['falszywe_ramki_na_dodatkach']} | "
            f"czas/obraz {w['czas_na_obraz_s']:.2f} s")
