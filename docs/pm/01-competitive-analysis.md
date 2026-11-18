# 01 — Analiza konkurencji i podejść (`/competitive-analysis`)

**Data**: 2026-11-18 · **Produkt**: narzędzie, które samo (bez człowieka, zadanie pkt 3) porównuje obraz naczepy/środka przewozowego z wzorcem i przygotowuje raport z zaznaczonymi różnicami; operator RTG ogląda gotowy raport (Artur, P2).
**Źródła**: `docs/zadanie.md`, `docs/materialy.md`, `docs/decyzje.md`; wyszukiwanie w sieci 18.11 (linki na końcu). Liczby z materiałów producentów to deklaracje marketingowe, nie niezależne testy — oznaczone „(deklaracja)".

**Zakres (z zadania, pkt 6):** test mierzy **„dodatki", które nie są elementami konstrukcyjnymi pojazdu** — to rdzeń produktu. Przeróbki konstrukcji i uszkodzenia (pkt 1–2) są w treści zadania, ale nie w opisie testu — to **otwarte pytanie do Artura** (lista niżej, pozycja 6). Wykrywamy „coś, czego nie ma we wzorcu"; **nie klasyfikujemy towaru** (papierosy, broń itd.). Wejście: pary i grupy obrazów (pkt 3, 7), nie tylko pary.

## Przegląd rynku
Wielkogabarytowe skanery RTG ładunków (Nuctech, Multicontrol, Smiths Detection, Rapiscan) są standardem na granicach. Oprogramowanie wspierające operatora dzieli się na dwie szkoły: (1) **detekcja znanych obiektów** (papierosy, broń — uczone na oznaczonych przykładach), (2) **detekcja anomalii** (odstępstwo od „normalnego" obrazu, bez znajomości zakazanego przedmiotu). KAS ma już narzędzie z grupy (1) (papierosy), które słabo radzi sobie z małymi ilościami ukrytymi w konstrukcji pojazdu (zadanie, pkt 1). Nasze rozwiązanie wchodzi w lukę grupy (2): porównanie z wzorcem + zaznaczenie różnicy, także dla przedmiotów, których nikt nie oznaczył, bez rozpoznawania, co to jest.

## Konkurenci bezpośredni (rozwiązania dla operatora)
| Rozwiązanie | Pozycjonowanie | Mocne strony | Słabości / luka |
|---|---|---|---|
| Obecne narzędzie KAS (papierosy) | Detekcja papierosów w towarze i konstrukcji | Już wdrożone, znane operatorom | Słabe przy małych ilościach papierosów w konstrukcji (zadanie, pkt 1); rozpoznaje tylko jeden rodzaj towaru |
| Rapiscan (oprogramowanie ładunków) | Dwa tory: anomalie (intensywność, tekstura, kształt) i głębokie uczenie dla wskazanych towarów (broń, papierosy); 96% wykryć przy 3% fałszywych alarmów (deklaracja, prezentacja CBP 2023) | Pełny pakiet ze sprzętem | Dane i modele zamknięte; brak niezależnych wyników |
| Nuctech (platforma inteligentnej inspekcji) | Warstwa AI na platformie producenta; walidacja wg norm lotniczych (dotyczy bagażu, nie ładunków) | Dostawca sprzętu KAS — łatwa integracja | Brak jawnych danych o ładunkach; zamknięty ekosystem |
| Smiths Detection | Algorytmy materiałowe/wybuchowe, certyfikacje | Marka, certyfikaty | Brak znalezionych danych o AI dla ładunków |
| Multicontrol | Sprzęt dostawcy KAS | Integracja z obecnym parkiem | Brak jawnych danych o AI |

## Konkurenci pośredni
- **Operator bez wsparcia** (ocena „na oko"): drobne zmiany i dodatki mogą umknąć (założenie, bez źródła; czasu decyzji operatora zadanie nie podaje).
- **Kontrola fizyczna / psy / ważenie**: pewna, ale droga i wolna; nasz produkt ma pomóc wybrać, co kontrolować.
- **Prace badawcze** (UCL + Rapiscan: „Assisted Inspection / Assisted Selection"; Tufts: model samouczący się do wykrywania nieoczekiwanych przedmiotów w kontenerach; Orange „Contraband AI"): kierunek anomalii bez ręcznego oznaczania jest realny, ale nie znalazłem gotowego produktu do pobrania.

## Przegląd podejść do detekcji anomalii na obrazach
| Podejście | Jak działa | Plusy | Minusy dla nas |
|---|---|---|---|
| **Różnica po rejestracji** (wyrównanie wzorca i obrazu, odjęcie, próg) | Dopasowuje parę obrazów i zaznacza piksele różniące się | Prosta, szybka, tłumaczalna, pasuje do par „przed/po" z zadania | Wrażliwa na przesunięcie/skalę/inną naczepę tego samego typu → fałszywe alarmy |
| **Autoenkoder** (uczony na czystych) | Uczy się odtwarzać „normalny" obraz; duży błąd odtworzenia = anomalia | Wymaga tylko obrazów czystych (pkt 5) | Rozmyte mapy; trudny dobór progu |
| **PaDiM** | Rozkład cech z wstępnie wytrenowanej sieci na każdą pozycję obrazu | Lekki; ok. 95% AUROC na MVTec AD (niezweryfikowane, źródła się różnią) | Zakłada stałą pozycję obiektu; pamięć rośnie z rozmiarem obrazu |
| **PatchCore** | Pamięć „normalnych" fragmentów cech; anomalia = fragment daleki od pamięci | Najlepszy wynik wśród metod bez oznaczeń (ok. 99% AUROC obrazowo, 98% na pikselach, MVTec AD); działa na kafelkach | Pamięć na zbiór fragmentów; trzeba ciąć obraz 50 MB na kafelki |
| **Segmentacja nadzorowana** (np. U-Net) | Uczy się z oznaczonych dodatków | Wysoka dokładność znanych przedmiotów | Wymaga oznaczeń; nie wykryje nowych skrytek |
| **Hybryda** (rejestracja + cechy + różnica) | Rejestracja usuwa przesunięcia, cechy oceniają resztę | Łączy tłumaczalność z odpornością | Więcej kroków do złożenia |

Wyniki PaDiM/PatchCore pochodzą z MVTec AD (obrazy przemysłowe) — to tylko kontekst, nie dowód jakości na RTG naczep. Wybór podejścia: patrz Rekomendacje.

## Macierz funkcji
„brak danych" = nie znalazłem jawnego źródła; wymagania z zadania oznaczone (zadanie, pkt).
| Zdolność | Nasz produkt (plan) | KAS dziś (papierosy) | Rapiscan | Nuctech |
|---|---|---|---|---|
| Wykrywa przedmioty bez oznaczeń (anomalie) | tak (porównanie z wzorcem) | nie (pkt 1) | częściowo (tor anomalii, źródło: Rapiscan) | brak danych |
| Dodatki niebędące konstrukcją (rdzeń testu, pkt 6) | tak | brak danych | brak danych | brak danych |
| Małe ilości w konstrukcji | do ustalenia z Arturem (pyt. 6) | słabo (pkt 1) | brak danych | brak danych |
| Zaznaczenie miejsca na obrazie | tak (pkt 3) | brak danych | brak danych | brak danych |
| Praca offline | tak (wymóg, pkt 9) | brak danych | brak danych | brak danych |
| BMP ~50 MB, partie, skalowanie (pkt 3) | tak (wymóg) | brak danych | brak danych | brak danych |
| Czas analizy < 1 min na obraz (pkt 7) | tak (wymóg) | brak danych | brak danych | brak danych |
| Pary i grupy obrazów (pkt 3, 7) | tak | brak danych | brak danych | brak danych |

## Możliwości wyróżnienia
1. **Anomalie zamiast katalogu przedmiotów** — wykrywa to, czego nikt nie oznaczył; trudne do skopiowania przez narzędzie „na papierosy".
2. **Mało fałszywych alarmów na czystych naczepach** — wprost mierzone przez jury (pkt 6); na czystych obrazach nic nie zaznaczamy (Artur, P3).
3. **Wynik zrozumiały dla operatora**: zaznaczony obszar + wzorzec obok, bez „czarnej skrzynki".
4. **Duże pliki, partie i szybkość** — analiza jednego obrazu < 1 min (pkt 7), kafelki, kompresja, skalowanie na większy zbiór.
5. **Działanie offline i przypisanie wyniku do miejsca i przedmiotu kontroli** (pkt 9) — gotowość do wdrożenia.

## Zagrożenia
1. **Producenci sprzętu** (Nuctech, Multicontrol) mogą dodać własne anomalie do swoich platform — odpowiedź: niezależność od dostawcy, otwarta integracja z repozytorium obrazów.
2. **Różnice między naczepami tego samego typu** będą wyglądać jak anomalie → fałszywe alarmy; ograniczyć wieloma wzorcami (grupy) i rejestracją.
3. **Brak danych KAS** (decyzje 08:09) — wyniki na własnym zbiorze syntetycznym nie dowodzą jakości na prawdziwych obrazach.

## Rekomendacje
- **Postawić na**: porównanie z wzorcem + zaznaczenie obszaru (dodatki niebędące konstrukcją), niska liczba fałszywych alarmów, praca offline, czas analizy < 1 min na obraz.
- **Nadrobić (wymóg wejścia)**: BMP, duże pliki, partie, raport z zaznaczeniami.
- **Pominąć**: klasyfikację towaru (papierosy, broń) — to robi już narzędzie KAS; my pokazujemy tylko „tego nie ma we wzorcu".
- **Propozycja techniczna (do decyzji Szefa/Programisty, nie Artura)**: start od różnicy po rejestracji pary (przy grupach wzorzec z wielu obrazów), liczonej na kafelkach; mocniejszy wariant opcjonalny: PatchCore na kafelkach. Ocena wg FP na czystych i FN na obrazach z dodatkami (pkt 6).

## Czego nie wiem o produkcie (lista do pytań do Artura — moment (a))
Pominięte jako rozstrzygnięte przez zadanie: praca offline, syntetyczne dane, działanie bez udziału człowieka, język ekranu, czas analizy < 1 min na obraz (pkt 7).
Rozstrzygnięte: P2 (użytkownik = operator RTG przy stanowisku, ogląda gotowy raport; „< 1 min" to czas analizy narzędzia, nie decyzji operatora), P3 (oba błędy liczą się razem; na czystych obrazach nic nie zaznaczać).

Produktowe, do Artura (jedno pytanie = jedna sprawa):
1. Jaki problem operatora jest największy dziś (drobne skrytki, zmęczenie, ilość obrazów)?
2. Co zyska operator, a co jego przełożony?
3. Co ma być wynikiem: same zaznaczenia na obrazie, raport do zapisania, czy ocena „puścić / kontrola"?
4. Raport ma dawać jedną ocenę na naczepę czy listę zaznaczonych miejsc (z ważnością)?
5. Czy operator może odrzucić zaznaczenie („to element konstrukcji") i czy to zapamiętujemy?
6. Czy przeróbki konstrukcji i uszkodzenia (pkt 1–2) mają być wykrywane, czy wystarczą „dodatki niebędące konstrukcją" (to mierzy test, pkt 6)? Rekomendacja: dodatki = rdzeń, przeróbki jako dodatek, jeśli zostanie czas.
7. Co uznajemy za „trafione" zaznaczenie: wystarczy, że dotyka dodatku, czy musi go dobrze obrysować?
8. Fałszywy alarm: liczymy każde zaznaczone miejsce na czystym obrazie, czy cały obraz z jakimkolwiek zaznaczeniem? A zaznaczenie obok dodatku na obrazie z dodatkiem?
9. Wejście: para (wzorzec + badany) czy grupa kilku obrazów naraz? Czy wzorzec wybiera system, czy operator?
10. Narzędzie pracuje na jednym obrazie czy na kolejce wielu naczep (partia)?
11. Jak wygląda pokaz (do 2 min): jedna naczepa czy seria?

Techniczne/organizacyjne (do Szefa, nie do Artura): wyrównanie obrazów w parze i przesunięcia (luka 6 w `docs/materialy.md`), czy kod uruchamia jury na własnych danych (luka 13), sprzęt dla limitu < 1 min (luka 10), format raportu i integracja z repozytorium (luka 11), licencja (luka 14).

## Źródła (wyszukiwanie 18.11.2026)
- [Rapiscan — technologia](https://rapiscan-ase.com/resource-center/technology)
- [Orange: Contraband AI](https://hellofuture.orange.com/en/contraband-ai-efficiently-detects-anomalies-in-shipping-containers/)
- [Survey: deep learning w obrazowaniu RTG](https://ar5iv.arxiv.org/html/2001.01293)
- [PaDiM](https://arxiv.org/pdf/2011.08785)
- [PatchCore — Towards Total Recall](https://openaccess.thecvf.com/content/CVPR2022/supplemental/Roth_Towards_Total_Recall_CVPR_2022_supplemental.pdf)
- [Optimizing PatchCore](https://arxiv.org/pdf/2307.10792)

<!-- skill: przeplywy-pm -->
<!-- skill: competitor-analysis -->
