# 01 — Analiza konkurencji i podejść (`/competitive-analysis`)

**Data**: 2026-11-18 · **Produkt**: narzędzie dla operatora RTG (KAS), które porównuje obraz naczepy/środka przewozowego z wzorcem i zaznacza anomalie (ukryty towar, przeróbki, skrytki).
**Źródła**: `docs/zadanie.md`, `docs/materialy.md`, `docs/decyzje.md`; wyszukiwanie w sieci 18.11 (linki na końcu). Liczby z materiałów producentów to deklaracje marketingowe, nie niezależne testy — oznaczone „(deklaracja)".

## Przegląd rynku
Wielkogabarytowe skanery RTG ładunków (Nuctech, Multicontrol, Smiths Detection, Rapiscan) są standardem na granicach. Oprogramowanie wspierające operatora dzieli się na dwie szkoły: (1) **detekcja znanych obiektów** (papierosy, broń — uczone na oznaczonych przykładach), (2) **detekcja anomalii** (odstępstwo od „normalnego" obrazu, bez znajomości zakazanego przedmiotu). KAS ma już narzędzie z grupy (1) (papierosy), które słabo radzi sobie z małymi ilościami ukrytymi w konstrukcji pojazdu (zadanie, pkt 1). Nasze rozwiązanie wchodzi w lukę grupy (2): porównanie z wzorcem + zaznaczenie różnicy, także dla przedmiotów, których nikt nie oznaczył.

## Konkurenci bezpośredni (rozwiązania dla operatora)
| Rozwiązanie | Pozycjonowanie | Mocne strony | Słabości / luka |
|---|---|---|---|
| Obecne narzędzie KAS (papierosy) | Detekcja papierosów w towarze i konstrukcji | Już wdrożone, znane operatorom | Słabe przy małych ilościach w konstrukcji; tylko jeden rodzaj towaru |
| Rapiscan (oprogramowanie ładunków) | Dwa tory: anomalie (intensywność, tekstura, kształt) i głębokie uczenie dla wskazanych towarów (broń, papierosy); deklaracja 96% wykryć przy 3% fałszywych alarmów (deklaracja, prezentacja CBP 2023) | Pełny pakiet ze sprzętem, doświadczenie | Dane i modele zamknięte, licencja ze sprzętem; brak niezależnych wyników |
| Nuctech (platforma inteligentnej inspekcji) | Warstwa AI na platformie producenta; walidacja wg norm lotniczych (dotyczy bagażu, nie ładunków) | Dostawca sprzętu KAS — najłatwiejsza integracja | Brak jawnych danych o ładunkach; zamknięty ekosystem |
| Smiths Detection | Algorytmy materiałowe/wybuchowe, certyfikacje | Marka, certyfikaty | Brak znalezionych danych o AI dla ładunków |
| Multicontrol | Sprzęt dostawcy KAS | Integracja z obecnym parkiem | Brak jawnych danych o AI |

## Konkurenci pośredni
- **Operator bez wsparcia** (ocena „na oko", 1 min na pojazd): zmęczenie, drobne zmiany konstrukcyjne umykają.
- **Kontrola fizyczna / psy / ważenie**: pewna, ale droga i wolna; nasz produkt ma pomóc wybrać, co kontrolować.
- **Prace badawcze** (ładunki, UCL+Rapiscan: „Assisted Inspection / Assisted Selection"; Tufts: model samouczący się do wykrywania nieoczekiwanych przedmiotów w kontenerach; Orange „Contraband AI"): pokazują, że kierunek anomalii bez ręcznego oznaczania jest realny, ale nie ma gotowego produktu na rynku do pobrania.

## Przegląd podejść do detekcji anomalii na obrazach (do wyboru przez Programistę)
| Podejście | Jak działa | Plusy | Minusy dla nas |
|---|---|---|---|
| **Różnica po rejestracji** (wyrównanie wzorca i obrazu, odjęcie, próg) | Dopasowuje parę obrazów i zaznacza piksele różniące się | Prosta, szybka, tłumaczalna operatorowi, działa na parach „przed/po" jak w zadaniu | Wrażliwa na przesunięcie/skalę/inną naczepę tego samego typu → fałszywe alarmy na detalach konstrukcji |
| **Autoenkoder** (uczony na czystych) | Uczy się odtwarzać „normalny" obraz; duży błąd odtworzenia = anomalia | Wymaga tylko obrazów czystych (jak w pkt 5 zadania) | Odtwarza też drobne anomalie; rozmyte mapy; trudny w doborze progu |
| **PaDiM** | Rozkład cech z wstępnie wytrenowanej sieci na każdą pozycję obrazu | Lekki, bez treningu głębokiego; ~95% AUROC na MVTec AD (do weryfikacji, źródła się różnią) | Zakłada ustaloną pozycję obiektu; pamięć rośnie z rozmiarem obrazu |
| **PatchCore** | Pamięć „normalnych" fragmentów cech; anomalia = fragment daleki od pamięci | Najlepszy wynik wśród metod bez oznaczeń (~99% AUROC obrazowo, 98% na pikselach, MVTec AD) i dobra lokalizacja; działa na kafelkach | Wymaga pamięci na zbiór fragmentów; trzeba ciąć obraz 50 MB na kafelki; MVTec to nie RTG |
| **Segmentacja nadzorowana** (np. U-Net) | Uczy się z oznaczonych dodatków | Wysoka dokładność znanych przedmiotów | Wymaga oznaczeń, których nie mamy; nie wykryje nowych skrytek |
| **Hybryda** (rejestracja + cechy + różnica) | Rejestracja usuwa przesunięcia, PatchCore ocenia resztę | Łączy tłumaczalność z odpornością | Więcej kroków do złożenia |

Wniosek techniczny (do rozstrzygnięcia przez Szefa/Programistę, nie przez Artura): dla syntetycznych par „czyste + dodatek" najpewniejszy start to różnica po rejestracji, jako mocniejszy wariant PatchCore na kafelkach; ewaluacja wg FP na czystych i FN na obrazach z dodatkami (zadanie, pkt 6). Wyniki z MVTec AD nie przenoszą się 1:1 na RTG naczep.

## Macierz funkcji
| Zdolność | Nasz produkt (plan) | KAS dziś (papierosy) | Rapiscan | Nuctech |
|---|---|---|---|---|
| Wykrywa nieznane przedmioty | tak (porównanie z wzorcem) | nie | częściowo (anomalie) | brak danych |
| Małe skrytki w konstrukcji | cel główny | słabo | brak danych | brak danych |
| Zaznaczenie miejsca na obrazie | tak | tak | tak | brak danych |
| Praca offline (bez chmury) | tak (wymóg zadania) | tak | tak | tak |
| Pliki BMP ~50 MB, przetwarzanie partiami | tak (wymóg zadania) | brak danych | brak danych | brak danych |
| Otwarty, możliwy do wdrożenia przez integratorów KAS | tak | — | licencja | licencja |

## Możliwości wyróżnienia
1. **Anomalie zamiast katalogu przedmiotów** — wykrywa to, czego nikt nie oznaczył; trudne do skopiowania przez narzędzie „na papierosy".
2. **Mało fałszywych alarmów na czystych naczepach** — to wprost mierzone przez jury; zaufanie operatora.
3. **Wynik, który operator rozumie**: zaznaczony obszar + wzorzec obok, bez „czarnej skrzynki".
4. **Duże pliki i partie** — kafelki, kompresja, skalowanie na większy zbiór.
5. **Działanie offline i przypisanie wyniku do miejsca i przedmiotu kontroli** (zadanie, pkt 9) — gotowość do wdrożenia.

## Zagrożenia
1. **Producenci sprzętu** (Nuctech, Multicontrol) mogą dodać własne anomalie do swoich platform — odpowiedź: niezależność od dostawcy, otwarta integracja z repozytorium obrazów.
2. **Różnice między naczepami tego samego typu** będą wyglądać jak anomalie → fałszywe alarmy; do ograniczenia wieloma wzorcami i rejestracją.
3. **Brak danych KAS** (decyzje 08:09) — wyniki na własnym zbiorze syntetycznym nie dowodzą jakości na prawdziwych obrazach.

## Rekomendacje
- **Postawić na**: porównanie z wzorcem + zaznaczenie obszaru, niska liczba fałszywych alarmów, praca offline.
- **Nadrobić (wymóg wejścia)**: bmp, duże pliki, partie, raport z zaznaczeniami.
- **Pominąć**: rozpoznawanie konkretnych towarów (papierosy) — to robi już narzędzie KAS.

## Czego nie wiem o produkcie (lista do pytań do Artura — moment (a))
Pominięte jako rozstrzygnięte przez zadanie: praca offline, syntetyczne dane, działanie bez udziału człowieka, język ekranu.
1. P2 — Kto używa narzędzia i w jakiej chwili pracy?
2. P3 — Fałszywy alarm czy przeoczenie: co gorsze?
3. Jaki problem operatora jest największy dziś (drobne skrytki, zmęczenie, pośpiech, ilość obrazów)?
4. Co zyska operator, a co jego przełożony (czas, mniej kontroli fizycznych, pewność)?
5. Co ma być wynikiem: samo zaznaczenie, raport do zapisania, czy ocena „puścić/kontrola"?
6. Czy ma być jedna ocena na całą naczepę, czy lista zaznaczonych miejsc z oceną ważności?
7. Czy operator może odrzucić zaznaczenie („to element konstrukcji") i czy to zapamiętujemy?
8. Czy narzędzie pracuje na jednym obrazie czy na kolejce wielu naczep naraz?
9. Czy wzorzec wybiera system, czy operator?
10. Jak wygląda pokaz (do 2 min): jedna naczepa czy seria?

## Źródła (wyszukiwanie 18.11.2026)
- [Rapiscan — technologia](https://rapiscan-ase.com/resource-center/technology)
- [Orange: Contraband AI](https://hellofuture.orange.com/en/contraband-ai-efficiently-detects-anomalies-in-shipping-containers/)
- [Survey: deep learning w obrazowaniu RTG](https://ar5iv.arxiv.org/html/2001.01293)
- [PaDiM](https://arxiv.org/pdf/2011.08785)
- [PatchCore — Towards Total Recall](https://openaccess.thecvf.com/content/CVPR2022/supplemental/Roth_Towards_Total_Recall_CVPR_2022_supplemental.pdf)
- [Optimizing PatchCore](https://arxiv.org/pdf/2307.10792)

<!-- skill: przeplywy-pm -->
<!-- skill: competitor-analysis -->
