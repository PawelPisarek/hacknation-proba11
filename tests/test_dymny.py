"""Test dymny głównej ścieżki: generuj → porównaj → ocena. Uruchom: python tests/test_dymny.py"""
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from rtg.__main__ import main  # noqa: E402
from rtg.ocena import ocen  # noqa: E402


def test_sciezka():
    with tempfile.TemporaryDirectory() as d:
        main(["generuj", d, "--czyste", "3", "--dodatek", "3", "--szer", "500", "--wys", "180", "--ziarno", "3"])
        pr = json.loads((Path(d) / "prawda.json").read_text())
        assert len(pr["pary"]) == 6 and all(p["dodatki"] for p in pr["pary"] if p["etykieta"] == "dodatek")
        p = pr["pary"][-1]
        main(["porownaj", str(Path(d) / p["wzorzec"]), str(Path(d) / p["badany"]), "--raport", d])
        assert (Path(d) / (Path(p["badany"]).stem + "_raport.png")).exists()
        w = ocen(d)
        assert w["n_czystych"] == 3 and w["n_dodatek"] == 3
        assert w["FP"] + w["FN"] <= 2, w


if __name__ == "__main__":
    test_sciezka()
    print("test dymny: OK")
