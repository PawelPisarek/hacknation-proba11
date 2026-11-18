# 02 — Odkrywanie produktu (`/discover`)

**Data**: 2026-11-18 · Etap: nowy produkt (brak użytkowników; dane KAS niedostępne) · Opiera się na: `docs/zadanie.md`, `docs/materialy.md`, `docs/pm/01-competitive-analysis.md`, `docs/decyzje.md`.
**Pytanie odkrywcze**: jak narzędzie, które samo porównuje obraz naczepy z wzorcem, ma pokazać operatorowi RTG, gdzie jest „coś, czego nie ma we wzorcu", żeby na czystych obrazach nie alarmowało, a dodatki były wskazane?

## Ustalone (nie pytamy ponownie)
- Odpowiedzi Artura P5–P13 (08:20–08:28) w `docs/decyzje.md`, streszczone niżej.
- Użytkownik: operator RTG przy stanowisku; narzędzie działa samo, operator ogląda gotowy raport (P2). „< 1 min" to czas analizy obrazu przez narzędzie.
- Oba błędy liczą się razem; na czystych obrazach nic nie zaznaczać (P3). FP = czysty obraz z choćby jednym zaznaczeniem; FN = obraz z dodatkiem bez ramki na dodatku (Szef 08:15).
- Narzędzie samo dopasowuje badany obraz do wzorca; wzorzec = obraz tego środka bez anomalii, pusty albo „przed" załadunkiem (Szef 08:14, 08:17).
- Raport: PNG z ramkami + JSON (ramka, pewność) na obraz + zbiorczy HTML na partię; CLI na folder + README; licencja MIT (Szef 08:14).
- Dane: tylko syntetyczne w repo, slajdach i makiecie (zadanie, pkt 7).
- Zakres: dodatki niebędące konstrukcją = rdzeń (pkt 6); przeróbki konstrukcji — otwarte (pyt. 6 z pliku 01).

## Czego nie wiem o produkcie
Odpowiedziane przez Artura w pokoju (08:20–08:28): P5–P13 (patrz „Ustalone"). Zostaje:
- P14 — który z trzech szkiców ekranu (moment (c), przed `/write-prd`) — czeka; rekomendacja: wariant 1 z paskiem oceny nad obrazem.
- Pyt. 5 z pliku 01 (odrzucanie zaznaczeń przez operatora) — nie zadane; pomysł 6 poza wyborem, więc w MVP odrzucamy; wraca w kierunkach.

## Użytkownik, problem, chwile użycia
- **Użytkownik**: operator RTG SCS na granicy zewnętrznej UE (zadanie); przełożony czyta zapis wyniku (P6).
- **Problem (P5)**: drobne ukryte rzeczy w konstrukcji umykają; obecne narzędzie (papierosy) zawodzi przy małych ilościach.
- **Zysk (P6)**: operator — podpowiedź, gdzie patrzeć, mniej zgadywania; przełożony — mniej zbędnych kontroli fizycznych i zapis wyniku przy miejscu kontroli.
- **Chwile użycia (P7)**: (1) tuż po prześwietleniu jednej naczepy — ekran z obrazem; (2) praca partiami bez człowieka od początku (pliki ~50 MB, wynik jako zbiorczy raport). Archiwum — pomijamy.

## Pomysły (faza rozbieżna) — 10
Z trzech perspektyw: PM, projektant (UX), inżynier.
1. **Ramki na obrazie badanym** — narzędzie zaznacza ramką każde miejsce różne od wzorca (PM: rdzeń testu pkt 6).
2. **Wzorzec obok badanego** z wspólnym przybliżaniem — operator widzi „tu było pusto" (UX).
3. **Jedna ocena naczepy** (zielona / do sprawdzenia) plus lista miejsc — szybka decyzja (PM/UX).
4. **Kolejka naczep** posortowana od najbardziej podejrzanej (UX; dla przeglądu partii).
5. **Biblioteka wzorców**: system sam wybiera najbliższy wzorzec (pusty albo „przed") dla danego typu naczepy (inżynier).
6. **Odrzucanie zaznaczeń** przez operatora („to element konstrukcji") i zapamiętanie — mniej fałszywych alarmów przy tym samym typie (UX/inżynier).
7. **Zbiorczy raport HTML partii** z miniaturami i filtrem „tylko z zaznaczeniami" (ustalony format; PM).
8. **Opis miejsca po ludzku**: „lewy dolny róg, przy ramie" — podpowiedź, gdzie szukać przy kontroli fizycznej (UX).
9. **Tryb nocny/partii**: przeliczenie folderu dużych obrazów (~50 MB) bez udziału człowieka, wynik rano (inżynier; wymóg skalowania).
10. **Zapis wyniku przy miejscu i przedmiocie kontroli** (metadane) pod przyszłą integrację z repozytorium (PM; zadanie, pkt 9).

## Wybór pomysłów, założenia, eksperymenty

### Wybór Artura (P8, P9–P13)
- **Rozwijamy: 1 (ramki na obrazie) + 3 (jedna ocena naczepy)**; z odrzuconych **część 9**: przeliczenie folderu bez człowieka, bez interfejsu, wynik w raporcie (skalowalność, 30% oceny). Pomysł 7 (zbiorczy HTML) wchodzi jako forma wyniku tej części; 2, 4, 5, 6, 8, 10 — poza MVP (5 w części: system sam wybiera wzorzec, P11).
- Zmiany w wybranych: nad obrazem jedna linia z oceną (zielona / do sprawdzenia, liczba miejsc) — to nie osobny ekran; przy ramce pewność (P9).
- Zakres: same dodatki; przeróbki konstrukcji tylko jako kierunek w prezentacji (P10). Wzorzec: para na ekranie, pod spodem model nauczony z wielu czystych (P11). Jeden obraz w pokazie, partia przez raport (P12). Pokaz: dwie naczepy (czysta, potem z dodatkiem), na końcu ~10 s raportu partii (P13).

### Krytyczne założenia
| # | Założenie | Rodzaj | Wpływ | Ryzyko |
|---|---|---|---|---|
| Z1 | Syntetyczne dodatki są wystarczająco podobne do prawdziwych, by wynik coś mówił | wykonalność | wysoki | wysokie |
| Z2 | Różnica po rejestracji daje mało alarmów na czystych obrazach mimo różnic ustawienia | wykonalność | wysoki | wysokie |
| Z3 | Nauczony model z wielu czystych obrazów obniża FP względem pojedynczego wzorca | wykonalność | średni | średnie |
| Z4 | Operator zrozumie pasek oceny + ramki bez szkolenia | użyteczność | średni | niskie |
| Z5 | Analiza ≤ 1 min na obraz ~50 MB na sprzęcie jury (P4 czeka) | wykonalność | wysoki | średnie |
| Z6 | Mała liczba ramek (mało FP) jest ważniejsza niż wykrycie każdego (oba błędy liczą się razem, P3) | wartość | wysoki | niskie |
| Z7 | Dane KAS nie trafią do repo, slajdów ani makiety | ochrona danych | wysoki | niskie |

**Najryzykowniejsze (do potwierdzenia przez Artura, czeka):** Z1 i Z2. Rekomendacja: potwierdzamy oba; sprawdzamy je pierwsze.

### Eksperymenty
| Zał. | Eksperyment | Kryterium sukcesu | Kryterium porażki → reguła |
|---|---|---|---|
| Z2 | Różnica po rejestracji na zestawie czystych par syntetycznych (generator Programisty) | ≥ 90% czystych obrazów bez ramki | < 90% → próg wyżej lub wariant mocniejszy (PatchCore) |
| Z1 | Dodatki o różnej wielkości w generatorze, skrypt oceny | ≥ 80% dodatków z ramką na dodatku | < 80% → mniejsze okno/czulsze progi, wpisać w ryzyka |
| Z3 | Porównanie: jeden wzorzec vs model z N czystych | FP niższe o ≥ 20% względnie | brak różnicy → zostaje para |
| Z5 | Pomiar czasu na obrazie ~50 MB | < 60 s | ≥ 60 s → zmniejszenie skali + zapis założenia |
| Z4 | Próba z Arturem/Pawłem na makiecie: „czy obraz jest czysty?" | poprawna odpowiedź w < 10 s bez wyjaśnień | błąd → przeprojektować pasek |
Progi 90/80/20% to założenia robocze (bez źródła), do skorygowania po pierwszym przebiegu.

### Plan i reguły decyzji
Kolejność: (1) generator + skrypt oceny (Programista), (2) różnica po rejestracji + ramki, (3) pasek oceny i ekran z jednym obrazem, (4) tryb folderu + raport HTML, (5) pokaz: dwie naczepy + raport partii. Jeśli Z2 nie przejdzie, nie dokładamy funkcji — poprawiamy wykrywanie. Jeśli czas się kończy, wypada zbiorczy HTML, zostaje JSON na obraz.

<!-- skill: przeplywy-pm -->
