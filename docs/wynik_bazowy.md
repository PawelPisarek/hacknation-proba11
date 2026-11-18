# Wynik bazowy

Metoda: rejestracja (korelacja fazowa, subpiksel) → różnica log(wzorzec)−log(badany) z tolerancją krawędzi (min 3×3 wzorca)
→ normalizacja szumu (σ_log ~ σ_I/I) → wygładzenie σ=2 → próg k·MAD (k=4) → obszary ≥ 30 px. Kod: `rtg/detektor.py`.

| zbiór | wynik |
|---|---|
| test (ziarno 1, 20 czystych + 20 z dodatkiem, 1000×360) | FP 0/20 (0%) \| FN 4/20 (20%) \| dodatki trafione 25/30 \| fałszywe ramki 0 \| czas/obraz 0.16 s |
| dev (ziarno 0, do strojenia k) | FP 0/20 (0%) \| FN 2/20 (10%) \| dodatki trafione 33/35 |
| duże (12000×4200, ~50 MB/plik, 1+1 para) | FP 0/1 \| FN 0/1 \| liczenie 1,7 s/obraz, z wczytaniem ~4 s, RAM < 1 GB |

Odtworzenie:
```
python -m rtg generuj dane/gen/test --ziarno 1
python -m rtg ocena dane/gen/test
```
Uwaga: syntetyczne pary czyste różnią się tylko szumem/przesunięciem/jasnością — dlatego FP=0. Prawdziwe obrazy (przesunięty
ładunek, inna geometria skanu) będą trudniejsze; to wskazówka do trudniejszego generatora.
