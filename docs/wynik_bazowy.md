# Wynik bazowy

FN liczone na obraz wg decyzji Szefa 08:15 (żadna ramka nie trafia w dodatek); „dodatki trafione” — każdy dodatek osobno.

Metoda: rejestracja (korelacja fazowa, subpiksel) → różnica log(wzorzec)−log(badany) z tolerancją krawędzi (min 3×3 wzorca)
→ normalizacja szumu (σ_log ~ σ_I/I) → wygładzenie σ=2 → próg k·MAD (k=4) → obszary ≥ 30 px. Kod: `rtg/detektor.py`.

| zbiór | wynik |
|---|---|
| test (ziarno 1, 20 czystych + 20 z dodatkiem, 1000×360) | FP 0/20 (0%) \| FN 2/20 (10%) \| dodatki trafione 25/30 \| fałszywe ramki 0 \| czas/obraz 0.17 s |
| dev (ziarno 0, do strojenia k) | FP 0/20 (0%) \| FN 0/20 (0%) \| dodatki trafione 33/35 |
| duże (12000×4200, ~50 MB/plik, 1+1 para) | FP 0/1 \| FN 0/1 \| liczenie 1,7 s/obraz, z wczytaniem ~4 s, RAM < 1 GB |

Odtworzenie:
```
python -m rtg generuj dane/gen/test --ziarno 1
python -m rtg ocena dane/gen/test
```
Uwaga: syntetyczne pary czyste różnią się tylko szumem/przesunięciem/jasnością — dlatego FP=0. Prawdziwe obrazy (przesunięty
ładunek, inna geometria skanu) będą trudniejsze; to wskazówka do trudniejszego generatora.

## Zbiór trudny (`generuj --trudny`, `--pusty-wzorzec`)

Czyste pary jak w prawdziwych skanach: ten sam ładunek inaczej ułożony (palety przesunięte o ±2% długości, 30% odwróconych),
rozciągnięcie w osi jazdy 0,97–1,03 plus falowanie prędkości przejazdu, pasy detektora (wzmocnienie kolumn i wierszy,
pojedyncze pasy pionowe, czasem martwy wiersz). Dodatek w ładunku przesuwa się razem ze swoją paletą. `--pusty-wzorzec`:
wzorzec bez ładunku, badany z ładunkiem. Metoda bazowa bez zmian (k=4, nic nie strojone na trudnym zbiorze).

| zbiór (20 czystych + 20 z dodatkiem, 1000×360) | wynik |
|---|---|
| trudny test (ziarno 1) | FP 20/20 (100%) \| FN 4/20 (20%) \| dodatki trafione 25/32 \| fałszywe ramki 419 \| czas/obraz 0.17 s |
| trudny dev (ziarno 0) | FP 19/20 (95%) \| FN 0/20 (0%) \| dodatki trafione 27/31 \| fałszywe ramki 420 |
| pusty wzorzec test (ziarno 1) | FP 20/20 (100%) \| FN 4/20 (20%) \| dodatki trafione 23/30 \| fałszywe ramki 238 \| czas/obraz 0.16 s |
| pusty wzorzec dev (ziarno 0) | FP 20/20 (100%) \| FN 6/20 (30%) \| dodatki trafione 16/28 \| fałszywe ramki 229 |

Wniosek: sama różnica pikseli po przesunięciu nie wystarcza — alarmuje na rozjechanych żebrach (rozciągnięcie)
i na przesuniętych paletach. Potrzebne: rejestracja nieliniowa w osi x (np. dopasowanie kolumn / DTW), wyrównanie pasów
detektora (normalizacja wierszy i kolumn), a dla ładunku porównanie inne niż piksel‑w‑piksel (cechy/segmenty, model „normalnego” ładunku).
FN liczone na obraz jest tu mało mówiące przy setkach ramek — miarodajne jest FP.
