# 02 — Odkrywanie produktu (`/discover`)

**Data**: 2026-11-18 · Etap: nowy produkt (brak użytkowników; dane KAS niedostępne) · Opiera się na: `docs/zadanie.md`, `docs/materialy.md`, `docs/pm/01-competitive-analysis.md`, `docs/decyzje.md`.
**Pytanie odkrywcze**: jak narzędzie, które samo porównuje obraz naczepy z wzorcem, ma pokazać operatorowi RTG, gdzie jest „coś, czego nie ma we wzorcu", żeby na czystych obrazach nie alarmowało, a dodatki były wskazane?

## Ustalone (nie pytamy ponownie)
- Użytkownik: operator RTG przy stanowisku; narzędzie działa samo, operator ogląda gotowy raport (P2). „< 1 min" to czas analizy obrazu przez narzędzie.
- Oba błędy liczą się razem; na czystych obrazach nic nie zaznaczać (P3). FP = czysty obraz z choćby jednym zaznaczeniem; FN = obraz z dodatkiem bez ramki na dodatku (Szef 08:15).
- Narzędzie samo dopasowuje badany obraz do wzorca; wzorzec = obraz tego środka bez anomalii, pusty albo „przed" załadunkiem (Szef 08:14, 08:17).
- Raport: PNG z ramkami + JSON (ramka, pewność) na obraz + zbiorczy HTML na partię; CLI na folder + README; licencja MIT (Szef 08:14).
- Dane: tylko syntetyczne w repo, slajdach i makiecie (zadanie, pkt 7).
- Zakres: dodatki niebędące konstrukcją = rdzeń (pkt 6); przeróbki konstrukcji — otwarte (pyt. 6 z pliku 01).

## Czego nie wiem o produkcie (przed momentem (b))
Z pliku 01, nadal otwarte i zadawane Arturowi po jednym: P5 największy problem operatora, P6 co zyskuje operator i przełożony, P7 chwile użycia, a dalej: co operator widzi najpierw i jak opisane jest miejsce (pyt. 3), jedna ocena naczepy czy lista miejsc (4), odrzucanie zaznaczeń (5), przeróbki konstrukcji (6), para czy grupa (9), kolejka czy jeden obraz (10), pokaz (11). Odpowiedzi wpisujemy do `docs/decyzje.md`; ten plik uzupełniam po nich.

## Użytkownik, problem, chwile użycia
*Do uzupełnienia po P5–P7 (czekają na Artura; po 10 min bierzemy rekomendacje).* Roboczo z zadania: operator RTG SCS na granicy zewnętrznej UE; problem — drobne ukryte przedmioty i przeróbki w konstrukcji oraz w towarze; obecne narzędzie (papierosy) zawodzi przy małych ilościach (zadanie, pkt 1).

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
*Czeka na wybór Artura (P8: 1–2 pomysły, potem co zmienić i czy któryś odrzucony wziąć w części). Dalszych sekcji — krytyczne założenia (wartość, użyteczność, wykonalność, ochrona danych), macierz Wpływ × Ryzyko, eksperymenty z kryteriami sukcesu, plan i reguły decyzji — nie piszę przed wyborem.*

<!-- skill: przeplywy-pm -->
