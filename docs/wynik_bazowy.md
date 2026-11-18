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

## Metoda v1 (domyślna; `--metoda v0` = stara) — `rtg/detektor_v1.py`

1. Wyrównanie pasów detektora: przesunięcie log-jasności wierszy (z kolumn powietrza przy brzegach) i kolumn (z wierszy powietrza u góry), osobno w obu obrazach.
2. Dopasowanie w osi jazdy: globalne przesunięcie, potem u(x) z NCC pasów pionowych (macierz pas × przesunięcie) + programowanie dynamiczne z karą za skok — bez kary łapało sąsiednie żebro (żebra są okresowe).
3. Ładunek: lokalne przesunięcie poziome s*(y, x) z dopasowania bloków w paśmie gładkim, wygładzone medianą (paleta rusza się w całości, dodatek jest mniejszy). Badany porównywany z wzorcem bez przesunięcia (konstrukcja) i z przesunięciem s* (ładunek) — bierzemy lepsze dopasowanie.
4. Dwa pasma osobno (drobne: żebra/krawędzie; gładkie: palety) — w log tłumienia się sumują, więc żebro na przesuniętej palecie było ciemniejsze niż każde z osobna we wzorcu.
5. Normalizacja szumu i próg jak w v0 (k=4·MAD), obszary ≥ 15 px.

Strojone tylko na trudnym dev (ziarno 0) i łatwym dev; test (ziarno 1) uruchomiony raz na końcu. Parametry: k=4, tol_x=0,025·szer, tol_h=0,01·szer, kara=0,05, min_pole=15.
Trafienia w podziale: miejsce (konstrukcja/ładunek) i rozmiar z pola `rozmiar` w `prawda.json` (spec §2, decyzja 08:52: „mały” = pole bboxa < 0,1% obrazu, < 360 px² przy 1000×360). Linie przeliczone 09:14 po zmianie reguły; obrazy bez zmian, zmienił się tylko `prawda.json`.

| zbiór | v1 | v0 (dla porównania) |
|---|---|---|
| **trudny test** | FP 5/20 (25%) \| FN 2/20 (10%) \| trafione 28/32 (konstr. 15/18, ład. 13/14, małe 3/3, duże 25/29; konstr./małe 2/2, konstr./duże 13/16, ład./małe 1/1, ład./duże 12/13) \| fałszywe ramki 8 \| 0,61 s/obraz | FP 20/20 \| FN 4/20 \| 25/32 \| fałszywe ramki 419 |
| trudny dev | FP 2/20 (10%) \| FN 3/20 (15%) \| trafione 25/31 \| fałszywe ramki 1 \| 0,60 s | FP 19/20 \| FN 0/20 \| 27/31 |
| **łatwy test** | FP 0/20 \| FN 3/20 (15%) \| trafione 25/30 (konstr. 13/16, ład. 12/14, małe 7/8, duże 18/22; konstr./małe 5/5, konstr./duże 8/11, ład./małe 2/3, ład./duże 10/11) \| 0,62 s | FP 0/20 \| FN 2/20 \| 25/30 |
| łatwy dev | FP 0/20 \| FN 0/20 \| trafione 33/35 | FP 0/20 \| FN 0/20 \| 33/35 |
| **pusty wzorzec test** | FP 20/20 (100%) \| FN 2/20 (10%) \| trafione 27/30 (konstr. 7/10, ład. 20/20, małe 3/4, duże 24/26; konstr./małe 0/1, konstr./duże 7/9, ład./małe 3/3, ład./duże 17/17) \| fałszywe ramki 241 \| 0,61 s | FP 20/20 \| FN 4/20 \| 23/30 |
| duże 12000×4200 (1+1) | FP 0/1 \| FN 1/1 \| 4,0 s/obraz | FP 0/1 \| FN 0/1 |

Wnioski:
- Trudny: FP 100% → 25% (test), FN 20% → 10%. Resztkowe FP: styki sąsiednich palet przesuniętych o różne wartości (często na żebrze).
- Łatwy: na dev bez zmian; na test o 1 obraz więcej FN (2 → 3), trafione dodatki te same 25/30 — granica „nie pogorszyć” na teście naruszona o jeden obraz.
- Duży obraz: jedyny dodatek był graniczny już w v0 (siła 5,6 przy progu 4), w v1 spada pod próg (2,9). Wyrównanie pasów i u(x) wykluczone jako przyczyna; do zbadania (rozmycie / pasma przy zmniejszeniu ×6). Zbiór dużych to 1 para — mało miarodajny.
- Pusty wzorzec: przy porównaniu para-do-pary cały ładunek jest „nowy” → FP 100% z definicji. Wymaga innego wzorca (niżej).

## Następny krok: wzorzec jako model z wielu czystych obrazów (P11, 08:25)

Ustalenie z Arturem (P11, pkt 5 zadania): pod spodem „wzorzec” może być modelem nauczonym z wielu czystych obrazów tego samego typu pojazdu; wzorzec wybiera system. Nie zmieściło się w tej rundzie. Plan:
1. Generator: `--grupa N` — N czystych skanów tego samego typu pojazdu (ta sama konstrukcja, różny ładunek / jego brak, różne rozciągnięcie, pasy, jasność) + badany.
2. Model: wszystkie czyste wyrównane do wspólnej geometrii (u(x) jak w v1), na piksel/kafelek mediana i rozrzut (MAD) tłumienia konstrukcji; ładunek odróżniony jako to, co zmienne między czystymi.
3. Detekcja: badany wyrównany do modelu, alarm gdy tłumienie > mediana + k·rozrzut poza obszarem ładunku; w ładunku — porównanie v1.
4. Pusty wzorzec przestaje być problemem, bo konstrukcja jest znana z wielu skanów, a ładunek modelowany osobno.

## Zbiory z wymuszonymi małymi dodatkami (pomiar Z1)

Generator: `--male 0.5` (około połowy dodatków ma pole < 0,1% obrazu; pole bboxa losowane z 30–80% progu). Przy `--male 0` stare ziarna dają bajt w bajt te same zbiory (sprawdzone na trudny test).
Zbiory: `trudny_male_dev` / `pusty_male_dev` (ziarno 2), `trudny_male_test` / `pusty_male_test` (ziarno 3), po 20 czystych + 20 z dodatkiem:
`python -m rtg generuj dane/gen/trudny_male_test --ziarno 3 --trudny --male 0.5` (dla pustego: `--pusty-wzorzec`).
Metoda v1 bez strojenia, test puszczony raz (09:17).

| zbiór | v1 |
|---|---|
| **trudny, małe, test** | FP 3/20 (15%) \| FN 3/20 (15%) \| trafione 27/31 (konstr. 16/18, ład. 11/13, małe 14/17, duże 13/14; konstr./małe 7/8, konstr./duże 9/10, ład./małe 7/9, ład./duże 4/4) \| fałszywe ramki 5 \| 0,63 s/obraz |
| **pusty wzorzec, małe, test** | FP 20/20 (100%) \| FN 2/20 (10%) \| trafione 25/32 (konstr. 15/22, ład. 10/10, małe 13/18, duże 12/14; konstr./małe 7/12, konstr./duże 8/10, ład./małe 6/6, ład./duże 4/4) \| fałszywe ramki 187 \| 0,60 s/obraz |

**Z1 (mały w konstrukcji ≥ 80%, trudny + pusty łącznie): 14/20 = 70% — nie spełnione.** Na pustym wzorcu trafienia są zawyżone przez 187 fałszywych ramek (trafienie przypadkiem).
