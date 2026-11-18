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
- Zakres: dodatki niebędące konstrukcją = rdzeń (pkt 6); przeróbki konstrukcji tylko jako kierunek w prezentacji, nie budujemy (P10).

## Czego nie wiem o produkcie
Odpowiedziane przez Artura w pokoju (08:20–08:28): P5–P13 (patrz „Ustalone"). Zostaje:
- P14 — który z trzech szkiców ekranu (moment (c), przed `/write-prd`) — czeka; rekomendacja: wariant 1 z paskiem oceny nad obrazem.
- P15 (pyt. 5 z pliku 01) — odpowiedź Artura 08:32: ramka zostaje w raporcie, bez odrzucania przez operatora (pomysł 6 poza MVP). Zamknięte.

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
- **Rozwijamy: 1 (ramki na obrazie) + 3 (jedna ocena naczepy)**; z odrzuconych **część 9**: przeliczenie folderu bez człowieka, bez interfejsu, wynik w raporcie (skalowalność, 30% oceny). Pomysł 7 (zbiorczy raport partii) wchodzi jako forma wyniku tej części i **jest zawsze w MVP, od kroku 1** (Szef 08:31): narzędzie liczy obrazy bez alarmu, obrazy z alarmem i liczbę ramek; gdy w folderze jest `prawda.json`, ten sam raport dokłada FP/FN i trafione dodatki ze skryptu oceny. Poza MVP: 2 (obok siebie), 4, 5, 6, 8, 10 — poza MVP (5 w części: system sam wybiera wzorzec, P11).
- P14 (08:30): wariant ekranu 1 — jeden obraz na całą szerokość (naczepa długa i płaska), ocena na górze; plus widoczny przełącznik „wzorzec / badany” nad obrazem (to samo miejsce, ta sama skala). **Wchodzi więc do zakresu ta część pomysłu 2**; wzorzec i badany obok siebie nie.
- Zmiany w wybranych: nad obrazem jedna linia z oceną (zielona / do sprawdzenia, liczba miejsc) — to nie osobny ekran; przy ramce pewność (P9).
- Zakres: same dodatki; przeróbki konstrukcji tylko jako kierunek w prezentacji (P10). Wzorzec: para na ekranie, pod spodem model nauczony z wielu czystych (P11). Jeden obraz w pokazie, partia przez raport (P12). Pokaz: dwie naczepy (czysta, potem z dodatkiem), na końcu ~10 s raportu partii (P13).

### Krytyczne założenia
| # | Założenie | Rodzaj | Wpływ | Ryzyko |
|---|---|---|---|---|
| Z1 | Syntetyczne dodatki są wystarczająco podobne do prawdziwych, a narzędzie trafia w dodatki (także małe, w konstrukcji — P5) | wykonalność | wysoki | wysokie |
| Z2 | Różnica po rejestracji daje mało alarmów na czystych obrazach mimo różnic ustawienia | wykonalność | wysoki | wysokie |
| Z3 | Wybrany sposób nauki z wielu czystych wzorców (pkt 5, P11 — wymaganie, nie do odrzucenia) działa lepiej niż najprostszy (np. średnia) | wykonalność | średni | średnie |
| Z4 | Operator zrozumie pasek oceny + ramki bez szkolenia | użyteczność | średni | niskie |
| Z5 | Analiza ≤ 1 min na obraz ~50 MB na sprzęcie jury (P4 czeka) | wykonalność | wysoki | średnie |
| Z6 | Oba błędy (FP i FN) liczą się równo (P3): dwie osobne miary z równymi progami, bez przechyłu w stronę mniejszej liczby ramek | wartość | wysoki | niskie |
| Z7 | Dane KAS nie trafią do repo, slajdów ani makiety | ochrona danych | wysoki | niskie |

**Najryzykowniejsze (do potwierdzenia przez Artura, czeka):** Z1 i Z2. Rekomendacja: potwierdzamy oba; sprawdzamy je pierwsze.

### Eksperymenty
Zbiór pomiarowy dla Z1 i Z2: **trudny** (`generuj … --trudny`) i wariant z pustym wzorcem (`--pusty-wzorzec`), nie zbiór łatwy; ocena skryptem oceny z `prawda.json`. Miary jak w skrypcie oceny: **FP** = odsetek czystych obrazów z jakąkolwiek ramką; **FN** = odsetek obrazów z dodatkiem, w których nie trafiono żadnego dodatku. Liczymy je osobno; roboczy próg jest równy dla obu: **każdy ≤ 10%** (założenie bez źródła; oba błędy równo, P3). Dodatkowo raportujemy trafienia dodatków w podziale na miejsce (konstrukcja / ładunek) i rozmiar (mały / duży) — pod P5.
| Zał. | Eksperyment | Kryterium sukcesu | Kryterium porażki → reguła |
|---|---|---|---|
| Z2 | Różnica po rejestracji na zbiorze trudnym i z pustym wzorcem | FP ≤ 10% i FN ≤ 10% na obu zbiorach (osobno) | FP lub FN > 10% na którymś → przejście na mocniejszą metodę (PatchCore/PaDiM) dla tego zbioru; próg dobieramy tak, by oba błędy były ≤ 10% |
| Z1 | Dodatki o różnej wielkości i w różnych miejscach, ten sam zbiór trudny | FN ≤ 10% (jak w Z2) oraz tabela trafień wg miejsca (konstrukcja/ładunek) × rozmiar (mały/duży); w komórce „mały w konstrukcji” trafienia ≥ 80% (założenie) | FN > 10% lub komórka < 80% → czulsze okno/mniejsze progi; wynik zapisany w ryzykach jako znana słabość |
| Z3 | Porównanie sposobów nauki z N czystych (np. średnia vs model z rozkładem) — nauka zostaje, wybieramy sposób | wybrany sposób ma FP i FN, każdy osobno, niższe o ≥ 20% względnie od najprostszego | brak różnicy → zostaje najprostszy; nauka z wielu czystych pozostaje |
| Z5 | Pomiar czasu na obrazie ~50 MB | < 60 s | ≥ 60 s → zmniejszenie skali + zapis założenia |
| Z4 | Próba z Arturem/Pawłem na makiecie: „czy naczepa jest czysta i gdzie jest dodatek?”, z przełącznikiem „wzorzec / badany” | poprawna odpowiedź w < 10 s bez wyjaśnień | błąd → przeprojektować pasek lub przełącznik |

### Plan i reguły decyzji
Kolejność: (1) generator + skrypt oceny (Programista) **i tryb folderu z raportem partii od razu** (P7, P13) — raport zawiera liczby bez alarmu / z alarmem / ramek oraz FP/FN przy `prawda.json`; (2) różnica po rejestracji + nauka z wielu czystych + ramki, mierzone na zbiorze trudnym i z pustym wzorcem; (3) ekran z jednym obrazem, paskiem oceny i przełącznikiem „wzorzec / badany”; (4) pokaz: dwie naczepy + raport partii. Raport partii nie wypada nawet przy braku czasu; wypadać może tylko ozdobny HTML ponad liczbami i JSON. Jeśli Z2 nie przejdzie, nie dokładamy funkcji — zmieniamy metodę wg reguły wyżej.

<!-- skill: przeplywy-pm -->
