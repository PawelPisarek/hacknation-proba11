# Decyzje

- 08:09 Szef: start próby 11, zadanie KAS RTG w docs/zadanie.md. Typ zadania: A (wynik mierzony na zbiorze jury: FP/FN na obrazach czystych i z dodatkami).
- 08:09 Szef: danych KAS nie mamy — własny syntetyczny zbiór .bmp (naczepy czyste / z dodatkami), generator w repo; nie commitujemy plików ~50 MB (generator + małe próbki).
- 08:09 Szef: zakres próby: krok 0, 0P, łańcuch 1a→1b→2, makieta (gh-pages) + krytyk makiety. Prezenter nie pracuje w tej próbie.
P1 08:09 Paweł: kto jest kim — jakie podpisy urządzeń mają Paweł i Artur (i czy ktoś jeszcze jest w zespole)? — czeka
P1 08:21 bez odpowiedzi Paweł → rekomendacja: Paweł = ta rozmowa (technika), Artur = Claude w pokoju Produkt, nikt więcej
P2 08:10 Artur: Kto dokładnie będzie używał narzędzia i w jakiej chwili pracy — operator RTG przy stanowisku, patrzący na obraz naczepy tuż po prześwietleniu? (rekomendacja: tak, operator przy stanowisku, decyzja „puścić / kontrola fizyczna” w ok. 1 min na pojazd) — czeka
P3 08:10 Artur: Co jest gorsze dla operatora: fałszywy alarm (zaznacza coś w czystej naczepie) czy przeoczenie (nie zaznacza ukrytego towaru)? (rekomendacja: przeoczenie jest gorsze, ale zadanie liczy oba błędy — ustawiamy czułość tak, by na czystych obrazach prawie nic nie zaznaczało) — czeka
- 08:11 Szef: krok 1a (docs/pm/01) — znacznik skilla OK; recenzja przejścia runda 1 → Analityk
- 08:12 Szef: 1a recenzja runda 1 — 5 braków (luki z materiałów, zakres vs test pkt 6, limit <1 min, papierosy, źródła macierzy) → poprawka Projektanta. Pkt 8 „Kryteria oceny” jest celowo pusty — nie jest brakiem.
P2 08:12 odpowiedź: tak, operator RTG przy stanowisku. Poprawka: „< 1 minuta” z zadania to czas analizy jednego obrazu przez narzędzie, nie czas decyzji operatora; narzędzie działa samo, bez człowieka (pkt 3), operator ogląda gotowy raport z zaznaczeniami — Artur w pokoju
P3 08:12 odpowiedź: zgoda z rekomendacją; oba błędy liczą się razem w 40% oceny, na czystych obrazach nie może nic zaznaczać — Artur w pokoju
- 08:13 Projektant: poprawka 1a runda 1 — uwzględniono wszystkie 5 braków; luki produktowe z materiałów dodane do listy pytań do Artura (pyt. 6–11), techniczne przekazane Szefowi (lista w pliku 01); P2: „< 1 min" = czas analizy narzędzia (pkt 7), usunięte z rekomendacji jako czas decyzji operatora.
- 08:14 Szef: luki techniczne z 01 — rozstrzygam: (a) obrazów nie zakładamy wyrównanych — narzędzie samo dopasowuje badany do wzorca (przesunięcie, skala, jasność); (b) zakładamy, że ktoś z zewnątrz uruchamia kod: CLI na folder obrazów + instrukcja w README; (c) raport: obraz z zaznaczonymi ramkami (PNG) + JSON (ramka, pewność) na obraz + zbiorczy HTML na partię; (d) licencja MIT.
P4 08:14 Paweł: na jakim sprzęcie ma się mieścić „< 1 min na obraz” ~50 MB — zwykły laptop na CPU czy z kartą graficzną? (rekomendacja: laptop CPU, bez internetu; GPU tylko opcjonalnie przyspiesza) — czeka
P4 08:24 bez odpowiedzi Paweł → rekomendacja: limit < 1 min na obraz ~50 MB mierzymy na zwykłym laptopie CPU, offline; GPU tylko opcjonalnie przyspiesza
- 08:14 Szef: 1a runda 2 recenzji przejścia → Analityk
08:14 Projektant: podpis „Artur (Claude za Pawła)” = Artur, gra go Claude na Macu Pawła, pisze tylko w pokoju Produkt (wpisane do docs/zespol.md) — Artur w pokoju
- 08:15 Szef: definicje liczenia (z pkt 6 zadania): FP = obraz czysty z choćby jednym zaznaczeniem (liczone na obraz); FN = obraz z dodatkiem, w którym żadna ramka nie nachodzi na dodatek (IoU>0 albo środek ramki w dodatku). Nie pytamy o to Artura.
- 08:15 Szef: 1a recenzja runda 2 — 4 braki (rozstrzygnięcia Szefa nieprzeniesione, pyt. 7–8 do złego adresata, twierdzenia o konkurencji bez źródeł, ochrona danych) → poprawka Projektanta
- 08:15 Programista: skrypt oceny (`python -m rtg ocena KATALOG`) wg §6 zadania: FP = obraz czysty z jakąkolwiek ramką; FN = obraz z dodatkiem, w którym żadna ramka nie nachodzi na dodatek (wg decyzji Szefa 08:15; IoU>0 — środek w ramce implikuje nachodzenie). Osobno raportuję dodatki trafione pojedynczo. Dodatkowo raportuję fałszywe ramki na obrazach z dodatkiem (nie liczone jako FP — §6 mówi o FP tylko na obrazach czystych).
- 08:15 Programista: syntetyczne dane (założenie techniczne, łatwe do zmiany): naczepa w rzucie bocznym, obraz = 255·g·exp(−tłumienie)+szum, 8‑bit BMP. Para czysta = ten sam pojazd i ten sam ładunek, inny szum, przesunięcie subpikselowe (±12 px przy 1000 px), jasność ±12 %. Para z dodatkiem = to samo + 1–2 obiekty (prostokąt / nieregularny, tłumienie 0,15–0,6) w konstrukcji (podłużnice, zbiornik, dolna rama) albo w ładunku. Prawda: `prawda.json` (bbox w układzie badanego). Wzorzec ma ten sam ładunek co badany (para „przed/po” jak w §7); wariant „wzorzec pusty vs badany z ładunkiem” — do decyzji w specu.
- 08:15 Programista: strojenie progu k na zbiorze dev (ziarno 0), wynik raportowany na test (ziarno 1). Próbka w repo: dane/probka (600×216, 8 par, 2 MB); większe zbiory i obrazy ~50 MB generowane lokalnie do dane/gen/ (nie w repo).
- 08:16 Projektant: poprawka 1a runda 2 — rozstrzygnięcia Szefa 08:14–08:15 przeniesione jako ustalone, pyt. 7–8 usunięte z listy do Artura, pyt. 3 zawężone, źródła/„niezweryfikowane” przy twierdzeniach o konkurencji, ochrona danych (pkt 7) w zagrożeniach i rekomendacjach
- 08:16 Szef: 1a recenzja przejścia runda 3 (ostatnia) → Analityk
- 08:16 Szef: krok 0P zamknięty — wynik bazowy test: FP 0/20, FN 2/20, 0,17 s/obraz; 50 MB ~4 s. Dalej (obok łańcucha): trudniejszy generator czystych par → Programista.
- 08:17 Szef: 1a recenzja runda 3 — „brak braków zmieniających zakres lub kryteria” → krok 1a zamknięty (3 rundy). Start 1b /discover → Projektant.
- 08:17 Szef: rodzaj wzorca — obsługujemy oba warianty z zadania (pkt 3 i 7): wzorzec = obraz tego środka bez anomalii, pusty albo „przed” załadunkiem; narzędzie nie zakłada, który.
P5 08:17 Artur: Jaki problem operatora jest dziś największy: drobne ukryte rzeczy umykają, zmęczenie przy dużej liczbie obrazów, czy pośpiech? (rekomendacja: drobne ukryte rzeczy w konstrukcji i ładunku, bo to opisuje zadanie i tam obecne narzędzie zawodzi) — czeka
P6 08:17 Artur: Co zyska operator, a co jego przełożony dzięki narzędziu? (rekomendacja: operator — podpowiedź, gdzie patrzeć, i mniej zgadywania; przełożony — mniej niepotrzebnych kontroli fizycznych i zapis wyniku przy miejscu kontroli) — czeka
P7 08:17 Artur: W jakich chwilach operator użyje narzędzia: tuż po prześwietleniu jednej naczepy, przy przeglądzie kolejki naczep, czy przy późniejszym sprawdzeniu archiwum? (rekomendacja: najpierw tuż po prześwietleniu jednej naczepy, potem kolejka; archiwum pomijamy) — czeka
P8 08:18 Artur: Wybierz 1–2 pomysły, które rozwijamy (numery z listy w wiadomości). (rekomendacja: 1 i 3 — zaznaczenia na obrazie plus jedna ocena naczepy; to najkrótsza ścieżka do pokazu w 2 min) — czeka
- 08:19 Programista: zbiór trudny = flaga `--trudny` generatora (ładunek tego samego typu inaczej ułożony, rozciągnięcie w osi jazdy 0,97–1,03 + falowanie prędkości, pasy detektora kolumn/wierszy, martwy wiersz); `--pusty-wzorzec` = wzorzec bez ładunku, badany z ładunkiem (implikuje trudny). Zbiór łatwy bez zmian (te same pliki przy tym samym ziarnie). Dev = ziarno 0, test = ziarno 1; metody nie stroję na test.
P9 08:19 Artur: Co operator widzi na ekranie najpierw po otwarciu naczepy: obraz z zaznaczonymi miejscami, czy najpierw krótkie podsumowanie? I jak opisać zaznaczone miejsce: sama ramka, ramka z pewnością (np. 87%), czy ramka z krótkim opisem miejsca? (rekomendacja: najpierw obraz z ramkami, przy ramce pewność; krótki opis miejsca opcjonalnie) — czeka
P10 08:19 Artur: Czy narzędzie ma też szukać przeróbek konstrukcji i uszkodzeń pojazdu, czy wystarczą dodatki, których nie ma we wzorcu (to mierzy test)? (rekomendacja: dodatki są rdzeniem; przeróbki tylko jeśli zostanie czas) — czeka
P11 08:19 Artur: Co daje narzędziu wzorzec: jedną parę (wzorzec + badany), czy grupę kilku obrazów naraz? I kto wybiera wzorzec: system czy operator? (rekomendacja: para jako podstawa, grupa jako rozszerzenie; wzorzec wybiera system, operator może go zmienić) — czeka
P12 08:19 Artur: Czy operator pracuje na jednym obrazie naraz, czy na kolejce wielu naczep? (rekomendacja: jeden obraz w pokazie, kolejka jako zbiorczy raport partii) — czeka
P13 08:19 Artur: Jak ma wyglądać pokaz do 2 minut: jedna naczepa od wczytania do raportu, czy seria naczep z czystą i z dodatkiem? (rekomendacja: dwie naczepy pod rząd — czysta bez zaznaczeń, potem z dodatkiem z ramką) — czeka
P5 08:20 odpowiedź: tak, drobne ukryte rzeczy w konstrukcji (zadanie: małe ilości papierosów w elementach konstrukcyjnych; obecne narzędzie tam zawodzi) — Artur w pokoju
P6 08:20 odpowiedź: zgoda z rekomendacją (operator — podpowiedź gdzie patrzeć; przełożony — mniej zbędnych kontroli i zapis wyniku) — Artur w pokoju
P7 08:20 odpowiedź: tuż po prześwietleniu jednej naczepy, ALE praca partiami bez człowieka (pkt 3, pliki ~50 MB) jest od początku, choćby prosta — nie „potem” — Artur w pokoju
P8 08:20 odpowiedź: wybrane 1 i 3 (ramki na obrazie + jedna ocena naczepy); z odrzuconych w części 9: przeliczenie folderu bez człowieka, bez interfejsu, wynik w raporcie (skalowalność 30% oceny) — Artur w pokoju
P9 08:22 odpowiedź: obraz z ramkami, nad nim jedna linia z oceną naczepy (zielona / do sprawdzenia, liczba miejsc) — to pomysł 3, nie osobny ekran; pewność przy ramce tak — Artur w pokoju
P10 08:23 odpowiedź: zgoda, same dodatki (to mierzy test); przeróbki konstrukcji tylko wspomnieć w prezentacji jako kierunek (zadanie je wymienia), nie budujemy — Artur w pokoju
P11 08:25 odpowiedź: para (wzorzec + badany) jako podstawa na ekranie; wg pkt 5 zadania narzędzie ma się NAUCZYĆ z wielu czystych obrazów wzorcowych — „wzorzec” to też model nauczony z czystych, pod spodem; wzorzec wybiera system (rekomendacja przyjęta) — Artur w pokoju
P11 08:27 potwierdzenie: system wybiera wzorzec — Artur w pokoju
P12 08:27 odpowiedź: w pokazie jeden obraz; partia (kolejka) przez zbiorczy raport z przeliczenia folderu — Artur w pokoju
P13 08:28 odpowiedź: pokaz = dwie naczepy pod rząd (czysta bez zaznaczeń, potem z dodatkiem z ramką); na koniec ~10 s na raport z partii: ile czystych bez alarmu, ile dodatków znalezionych (liczby dla jury, 40%) — Artur w pokoju
P14 08:28 Artur: Który z trzech szkiców ekranu bierzemy: (1) jeden obraz na cały ekran, (2) najpierw lista/kolejka naczep, (3) wzorzec i badany obok siebie? (rekomendacja: wariant 1 z paskiem oceny nad obrazem, partia jako osobny raport) — czeka
1b recenzja przejścia runda 1 → Analityk (08:30)
P14 08:30 odpowiedź: wariant 1 (jeden obraz na całą szerokość, ocena na górze; naczepa długa i płaska). Zmiana: widoczny przełącznik „wzorzec / badany” nad obrazem (to samo miejsce, ta sama skala), nie osobny widok — Artur w pokoju
P15 08:30 Artur: Co robi operator z ramką, której nie uważa za dodatek (np. element konstrukcji): zostawia ją w raporcie, czy może ją odrzucić? (rekomendacja: zostawia, bez odrzucania — odrzucanie to pomysł 6, którego nie wybrałeś) — czeka
1b recenzja runda 1: 5 braków (P13/P7 plan, Z3 vs pkt 5, Z2 zbiór, Z6 vs P3, P14/P15) → Projektant (08:31)
08:31 Szef: raport partii zawsze w MVP i od kroku 1 (tryb folderu przed ekranem). Narzędzie liczy obrazy bez alarmu / z alarmem i liczbę ramek; gdy w folderze jest prawda.json, ten sam raport dokłada FP/FN i trafione dodatki ze skryptu oceny.
08:31 Szef: nauka z wielu czystych wzorców (pkt 5, P11) jest wymaganiem, nie eksperymentem do odrzucenia; eksperyment wybiera tylko sposób.
08:31 Szef: oba błędy (FP i FN) traktujemy równo (P3); bez hierarchii „mało ramek ważniejsze”.
P15 08:32 odpowiedź: ramka zostaje w raporcie, bez odrzucania przez operatora — Artur w pokoju
P16 08:32 Artur: Co dokładnie jest na ramce: sama ramka z pewnością (np. 87%), czy jeszcze krótki opis miejsca („lewy dolny róg, przy ramie”)? (rekomendacja: ramka z pewnością i numerem na liście; opis słowny odpada — P9 wybrał pewność, opis nie jest potrzebny do liczb jury) — czeka
1b recenzja przejścia runda 2 → Analityk (08:32)
1b recenzja runda 2: 3 braki (przeróbki otwarte/zamknięte, mianownik Z1/Z2, brak pomiaru małych dodatków w konstrukcji) → Projektant (08:32)
08:32 Szef: miary jak w skrypcie oceny — FP = odsetek czystych obrazów z ramką, FN = odsetek obrazów z dodatkiem bez trafienia; liczone osobno, robocze progi równe (każdy ≤ 10%, bez źródła).
08:32 Szef: wynik trafień dodatków raportujemy też w podziale na miejsce (konstrukcja / ładunek) i rozmiar (mały / duży).
1b recenzja przejścia runda 3 → Analityk (08:33)
P16 08:33 odpowiedź: ramka = pewność i numer z listy miejsc, bez opisu słownego — Artur w pokoju
P17 08:33 Artur: Raport z partii pokazujemy w pokazie jako jedną stronę z liczbami (ile czystych bez alarmu, ile dodatków znalezionych) i listą naczep z oceną — otwieraną z tego samego ekranu, czy jako osobny plik do otwarcia? (rekomendacja: strona otwierana z ekranu przyciskiem, ten sam plik da się też zapisać) — czeka
1b recenzja runda 3: 2 braki (Z2 w dwóch wersjach; Z3/Z6/Z1 nadal „suma FP+FN”) — 3 rundy wyczerpane (08:34)
P18 08:34 Paweł: 1b po 3 rundach ma 2 braki (niespójne zapisy miar FP/FN w pliku 02). Puszczamy dalej do /write-prd? (rekomendacja: tak — braki zapisane jako ryzyka w specu, Projektant ujednolica zapis do decyzji 08:33 przy /write-prd) — czeka
P17 08:35 odpowiedź: raport z partii otwierany przyciskiem z ekranu, plus zapis do pliku — Artur w pokoju
P19 08:35 Artur: Kiedy naczepa dostaje ocenę „zielona”: tylko gdy nie ma żadnego zaznaczonego miejsca, czy też gdy są tylko miejsca o niskiej pewności? (rekomendacja: zielona tylko przy zerze zaznaczeń; narzędzie samo odcina słabe trafienia progiem, żeby czyste naczepy nie dawały alarmu — i tak liczy się to 40% oceny) — czeka
P19 08:37 odpowiedź: zgoda, zielona tylko przy zerze zaznaczeń; próg odcinania słabych trafień to najważniejsza gałka dla liczb jury — ma być jawnie zapisany w raporcie (w pokoju to pytanie nosiło numer P18, w tym pliku P19 — numer zajęty przez Pawła) — Artur w pokoju
08:38 Artur w pokoju: co wyrzucić z ekranu — lista miejsc wylatuje z głównego ekranu (trafia do raportu z partii); „zapis do pliku” też tylko w widoku raportu z partii. Główny ekran: ocena, obraz z ramkami, przełącznik wzorzec/badany, przycisk raportu
P18 08:44 bez odpowiedzi Paweł → rekomendacja: puszczamy 1b dalej do /write-prd; 2 braki (zapis miar FP/FN w 02) jako ryzyka w specu, Projektant ujednolica zapis do decyzji 08:33
08:46 Szef: tryb folderu = `python -m rtg porownaj --folder KATALOG` (zgoda na propozycję Projektanta); generator dopisuje do prawda.json pola `miejsce` i `rozmiar` dodatku.
08:46 Szef: krok 2 (/write-prd) recenzja przejścia R1 → Analityk (03 vs 02).
08:47 Szef: krok 2 R1 — 5 braków (Analityk) → Projektant poprawia 03 i spec.
08:47 Szef: próg odcinania pokazujemy w raporcie z partii (P19), nie na głównym ekranie; główny ekran = dokładnie 4 elementy z 08:38 (bez Poprzednia/Następna).
08:47 Szef: liczby udawane w makiecie podpisane, z którego zbioru są (łatwy / trudny); w raporcie partii pokazujemy oba zbiory.
08:48 Szef: krok 2 R2 → Analityk.
P20 08:49 Artur: Najpierw sprawdzamy, czy narzędzie nie alarmuje na czystych naczepach, gdy ładunek jest ułożony inaczej niż we wzorcu albo wzorzec to pusta naczepa. Czy to jest dla Ciebie pierwsze ryzyko do sprawdzenia? (rekomendacja: tak — to pierwsze ryzyko: bez tego operator przestanie ufać zielonej ocenie) — czeka
08:49 Szef: krok 2 R2 — 2 braki (Analityk) → Projektant.
08:49 Szef: Z3 = FP i FN osobno, żaden nie gorszy od najprostszego sposobu, a co najmniej jeden niższy o ≥ 20% względnie (gdy bazowy > 0); 20% to założenie bez źródła — jedna wersja w 02, 03 i specu.
08:49 Szef: raport partii (ekran B) pokazuje trzy zbiory: łatwy, trudny, pusty wzorzec — każdy podpisany.
08:50 Szef: krok 2 R3 → Analityk.
P20 08:51 odpowiedź: tak, to pierwsze ryzyko; fałszywe alarmy na czystych to połowa 40% oceny — Artur w pokoju
08:51 Szef: krok 2 R3 — „brak braków zmieniających zakres lub kryteria” (Analityk); pętla zamknięta po 3 rundach. Recenzja odbiorcy → Programista.
08:52 Szef: recenzja odbiorcy R1 — 5 braków (Programista) → Projektant. Rozstrzygnięcia:
08:52 Szef: „mały/duży” — reguła ze speca (pole < 0,1% obrazu, do czasu odpowiedzi Artura P22); generator zapisuje `rozmiar` w prawda.json, `ocena` czyta to pole.
08:52 Szef: `porownaj --folder` — pary po nazwach `*_wzorzec.bmp` / `*_badany.bmp`; opcjonalnie `--wzorce KATALOG` (pula czystych); każdy podkatalog = osobny zbiór, nazwa = podpis w raporcie.
08:52 Szef: testy akceptacji — 20 czystych + 20 z dodatkiem na zbiór; ziarno 0 strojenie, ziarno 1 ocena (bez strojenia); test „mały w konstrukcji” liczony łącznie na trudnym i pustym wzorcu.
08:52 Szef: próg odcinania = minimalna pewność ramki w %; `k` parametr wewnętrzny; oba w JSON.
P21 08:52 Artur: Drugie ryzyko do sprawdzenia: czy narzędzie znajdzie małe dodatki w konstrukcji (osobno małe i duże)? (rekomendacja: tak, a słabość jawnie w raporcie) — czeka
P21 08:53 odpowiedź: tak, to sedno zadania — obecne narzędzie KAS zawodzi na małych ilościach w konstrukcji; jawna słabość w raporcie — Artur w pokoju
08:53 Szef: odbiorca R1 poprawione przez Projektanta (spec); recenzja odbiorcy R2 → Programista.
08:53 Szef: recenzja odbiorcy R2 — brak braków; spec do budowy. Pole JSON: prog_pewnosci (Programista). Makieta → Programista.
08:58 Szef: makieta R1 na gh-pages (200), zrzuty docs/makieta/ekran-a.png, ekran-b.png; krytyk R1 → Analityk.
08:59 Szef: krytyk makiety R1 — ocena 6/10, 5 braków (wszystkie poprawki Programisty) + lista miejsc na ekranie B wbrew Arturowi 08:38 → usunąć. Poprawka R1 → Programista.
09:01 Szef: cofnięte przez Szefa — mój wpis 08:59 o usunięciu listy miejsc był błędny: Artur 08:38 przeniósł listę miejsc do raportu z partii (ekran B), spec §2 pkt 4 słusznie. Programista przywraca listę na ekranie B.
09:01 Szef: makieta — duża liczba zielona od 90% (spójnie z celem FP/FN ≤ 10%); przyjęte.
- 09:04 Szef: lista miejsc przywrócona na ekranie B (main 46c5559, gh-pages 74f7545, HTTP 200); krytyk R2 → Analityk.
- 09:05 Szef: krytyk makiety R2 8/10, 3 braki (kolor dużej liczby dodatków, 9 wierszy w karcie, brak zrzutu czystej naczepy) → Programista.
- 09:05 Szef: duża liczba „dodatki znalezione” zostaje w dodatkach (Artur P13), ale kolor bierze z celu FN ≤ 10% na obraz (zielona, gdy cel spełniony); wiersze dublujące duże liczby chowamy pod „szczegóły”.
