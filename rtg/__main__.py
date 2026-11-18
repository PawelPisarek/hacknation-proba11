"""CLI:  python -m rtg porownaj WZORZEC.bmp BADANY.bmp [--raport KATALOG]
        python -m rtg generuj KATALOG [--czyste N --dodatek N --szer W --wys H --ziarno S --trudny --pusty-wzorzec --male U]
        python -m rtg ocena KATALOG [--k K] [--json PLIK]
"""
import argparse
import json
import sys
import time
from pathlib import Path


def _metoda(nazwa):
    if nazwa == "v0":
        from .detektor import wykryj
    else:
        from .detektor_v1 import wykryj
    return wykryj


def main(argv=None):
    ap = argparse.ArgumentParser(prog="rtg", description="Porównanie obrazów RTG: wzorzec vs badany")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("porownaj", help="porównaj parę obrazów i zapisz raport")
    p.add_argument("wzorzec"); p.add_argument("badany")
    p.add_argument("--raport", default="wyniki"); p.add_argument("--k", type=float, default=4.0)
    p.add_argument("--metoda", choices=["v0", "v1"], default="v1", help="v0 = różnica po przesunięciu, v1 = odporna (domyślna)")
    g = sub.add_parser("generuj", help="syntetyczny zbiór par .bmp + prawda.json")
    g.add_argument("katalog")
    g.add_argument("--czyste", type=int, default=20); g.add_argument("--dodatek", type=int, default=20)
    g.add_argument("--szer", type=int, default=1000); g.add_argument("--wys", type=int, default=360)
    g.add_argument("--ziarno", type=int, default=0)
    g.add_argument("--trudny", action="store_true", help="ładunek inaczej ułożony, rozciągnięcie, pasy detektora")
    g.add_argument("--pusty-wzorzec", action="store_true", help="wzorzec bez ładunku, badany z ładunkiem (implikuje --trudny)")
    g.add_argument("--male", type=float, default=0.0, help="udział dodatków wymuszonych jako małe (pole < 0,1%% obrazu), np. 0.5")
    o = sub.add_parser("ocena", help="FP/FN na zbiorze z prawda.json")
    o.add_argument("katalog"); o.add_argument("--k", type=float, default=4.0); o.add_argument("--json")
    o.add_argument("--metoda", choices=["v0", "v1"], default="v1")
    a = ap.parse_args(argv)

    if a.cmd == "porownaj":
        from .obrazy import wczytaj
        wykryj = _metoda(a.metoda)
        from .raport import zapisz
        t = time.perf_counter()
        B = wczytaj(a.badany)
        wyn = wykryj(wczytaj(a.wzorzec), B, k=a.k)
        wyn["czas_s"] = round(time.perf_counter() - t, 3)
        pliki = zapisz(wyn, B, a.raport, Path(a.badany).stem)
        print(json.dumps({**wyn, "raport": pliki}, ensure_ascii=False))
    elif a.cmd == "generuj":
        from .generator import generuj_zbior
        pr = generuj_zbior(a.katalog, a.czyste, a.dodatek, h=a.wys, w=a.szer, ziarno=a.ziarno,
                           trudny=a.trudny, pusty_wzorzec=a.pusty_wzorzec, male=a.male)
        print(f"wygenerowano {len(pr['pary'])} par w {a.katalog}")
    elif a.cmd == "ocena":
        from .ocena import linia, ocen
        w = ocen(a.katalog, metoda=_metoda(a.metoda), k=a.k)
        if a.json:
            Path(a.json).write_text(json.dumps(w, ensure_ascii=False, indent=1))
        print(linia(w))
    return 0


if __name__ == "__main__":
    sys.exit(main())
