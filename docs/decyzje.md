# Decyzje

- 08:09 Szef: start próby 11, zadanie KAS RTG w docs/zadanie.md. Typ zadania: A (wynik mierzony na zbiorze jury: FP/FN na obrazach czystych i z dodatkami).
- 08:09 Szef: danych KAS nie mamy — własny syntetyczny zbiór .bmp (naczepy czyste / z dodatkami), generator w repo; nie commitujemy plików ~50 MB (generator + małe próbki).
- 08:09 Szef: zakres próby: krok 0, 0P, łańcuch 1a→1b→2, makieta (gh-pages) + krytyk makiety. Prezenter nie pracuje w tej próbie.
P1 08:09 Paweł: kto jest kim — jakie podpisy urządzeń mają Paweł i Artur (i czy ktoś jeszcze jest w zespole)? — czeka
P2 08:10 Artur: Kto dokładnie będzie używał narzędzia i w jakiej chwili pracy — operator RTG przy stanowisku, patrzący na obraz naczepy tuż po prześwietleniu? (rekomendacja: tak, operator przy stanowisku, decyzja „puścić / kontrola fizyczna” w ok. 1 min na pojazd) — czeka
P3 08:10 Artur: Co jest gorsze dla operatora: fałszywy alarm (zaznacza coś w czystej naczepie) czy przeoczenie (nie zaznacza ukrytego towaru)? (rekomendacja: przeoczenie jest gorsze, ale zadanie liczy oba błędy — ustawiamy czułość tak, by na czystych obrazach prawie nic nie zaznaczało) — czeka
- 08:11 Szef: krok 1a (docs/pm/01) — znacznik skilla OK; recenzja przejścia runda 1 → Analityk
- 08:12 Szef: 1a recenzja runda 1 — 5 braków (luki z materiałów, zakres vs test pkt 6, limit <1 min, papierosy, źródła macierzy) → poprawka Projektanta. Pkt 8 „Kryteria oceny” jest celowo pusty — nie jest brakiem.
P2 08:12 odpowiedź: tak, operator RTG przy stanowisku. Poprawka: „< 1 minuta” z zadania to czas analizy jednego obrazu przez narzędzie, nie czas decyzji operatora; narzędzie działa samo, bez człowieka (pkt 3), operator ogląda gotowy raport z zaznaczeniami — Artur w pokoju
P3 08:12 odpowiedź: zgoda z rekomendacją; oba błędy liczą się razem w 40% oceny, na czystych obrazach nie może nic zaznaczać — Artur w pokoju
- 08:13 Projektant: poprawka 1a runda 1 — uwzględniono wszystkie 5 braków; luki produktowe z materiałów dodane do listy pytań do Artura (pyt. 6–11), techniczne przekazane Szefowi (lista w pliku 01); P2: „< 1 min" = czas analizy narzędzia (pkt 7), usunięte z rekomendacji jako czas decyzji operatora.
- 08:14 Szef: luki techniczne z 01 — rozstrzygam: (a) obrazów nie zakładamy wyrównanych — narzędzie samo dopasowuje badany do wzorca (przesunięcie, skala, jasność); (b) zakładamy, że ktoś z zewnątrz uruchamia kod: CLI na folder obrazów + instrukcja w README; (c) raport: obraz z zaznaczonymi ramkami (PNG) + JSON (ramka, pewność) na obraz + zbiorczy HTML na partię; (d) licencja MIT.
P4 08:14 Paweł: na jakim sprzęcie ma się mieścić „< 1 min na obraz” ~50 MB — zwykły laptop na CPU czy z kartą graficzną? (rekomendacja: laptop CPU, bez internetu; GPU tylko opcjonalnie przyspiesza) — czeka
- 08:14 Szef: 1a runda 2 recenzji przejścia → Analityk
