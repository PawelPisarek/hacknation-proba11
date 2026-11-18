## Product Requirements Document: wyszukiwarka anomalii na obrazach RTG naczep

**Author**: Projektant · **Date**: 2026-11-18 · **Status**: Draft
Opiera się na: `docs/zadanie.md`, `docs/pm/01-competitive-analysis.md`, `docs/pm/02-discover.md`, `docs/decyzje.md` (P2–P19, wpisy 08:31–08:38). Układ techniczny dla Programisty: `docs/spec.md`.

### 1. Summary
Narzędzie samo porównuje obraz RTG naczepy z wzorcem (obrazem bez anomalii) i zaznacza ramkami miejsca, których nie ma we wzorcu. Operator widzi jeden obraz na całą szerokość, nad nim ocenę naczepy; partię obrazów liczy się bez człowieka, wynik to raport partii. Dane tylko syntetyczne.

### 2. Contacts
Artur (kształt produktu), Paweł (technika, wygląd, użyteczność). Boty: Projektant (spec), Programista (makieta, MVP), Analityk (recenzje), Prezenter (README, prezentacja).

### 3. Background
KAS używa narzędzia AI do papierosów; przy małych ilościach w elementach konstrukcyjnych zawodzi (zadanie, pkt 1). Zadanie pyta o autonomiczne porównanie obrazów, wskazanie dodatków i skalowalność (pliki ~50 MB, partie). Operator RTG ogląda wynik po prześwietleniu naczepy (P2, P5–P7). Konkurencja i podejścia: plik 01; start techniczny: różnica po rejestracji (propozycja), mocniejsza metoda tylko gdy pomiar tego wymaga (02).

### 4. Objective
- **Cel**: na czystych naczepach brak alarmu, na naczepach z dodatkiem — ramka na dodatku, czas analizy < 1 min na obraz.
- **Miary** (jak w `rtg/ocena.py`, liczone na obraz, osobno, bez sumowania):
  - **FP** = odsetek czystych obrazów z jakąkolwiek ramką; roboczo ≤ 10%.
  - **FN** = odsetek obrazów z dodatkiem, w których żadna ramka nie trafia w dodatek; roboczo ≤ 10%.
  - Progi 10% są założeniem bez źródła (decyzja Szefa 08:32).
  - **Trafienia dodatków** raportowane osobno w podziale: miejsce (konstrukcja / ładunek) × rozmiar (mały / duży) — pod P5 (małe rzeczy w konstrukcji).
- Zbiór pomiarowy: trudny (`--trudny`) i z pustym wzorcem (`--pusty-wzorzec`), nie tylko łatwy.

### 5. Market Segment(s)
Operator RTG SCS na granicy zewnętrznej UE (główny); jego przełożony (czyta raport partii i zapis wyniku). Ocena hackathonu: jury KAS, które uruchamia narzędzie na własnych parach (README + CLI).

### 6. Value Proposition(s)
**Operator.** Who: operator po prześwietleniu naczepy. Why: drobne ukryte rzeczy umykają (P5). What before: ogląda cały obraz sam. How: ramki z pewnością i numerem + ocena naczepy. What after: wie, gdzie patrzeć; zielona = zero zaznaczeń. Alternatives: obecne narzędzie na papierosy.
**Przełożony.** Why: mniej zbędnych kontroli fizycznych (P6). How: raport partii z liczbami (bez alarmu / z alarmem / ramek) i listą naczep, zapis do pliku.

### 7. Solution
**Co zobaczy i zrobi użytkownik (według Artura):**
1. **Główny ekran** (wariant 1, P14): jeden obraz na całą szerokość (naczepa długa i płaska). Dokładnie cztery elementy (08:38): ocena naczepy nad obrazem, obraz z ramkami, przełącznik „wzorzec / badany” (to samo miejsce, ta sama skala), przycisk raportu. Bez listy miejsc, zapisu, progu i przycisków nawigacji.
2. **Ocena**: „zielona” tylko gdy zero zaznaczeń; w przeciwnym razie „do sprawdzenia” i liczba miejsc (P9, P19).
3. **Ramka**: pewność i numer, bez opisu słownego (P16). Operator nie odrzuca ramek (P15). Próg odcinania słabych trafień jest jawnie pokazany **w raporcie z partii** (nie na głównym ekranie; P19, Szef 08:47).
4. **Raport partii** otwierany przyciskiem z ekranu (P17): liczby (czyste bez alarmu, obrazy z alarmem, liczba ramek), próg odcinania, oba zbiory (łatwy i trudny), lista naczep z oceną, **lista miejsc** i **zapis do pliku** — tylko tutaj. Gdy w folderze jest `prawda.json`, raport dokłada FP, FN i trafienia wg miejsca i rozmiaru.
5. **Wzorzec**: system wybiera go sam (P11); pod spodem model uczony na wielu czystych obrazach (pkt 5), na ekranie para.
6. **Partia bez człowieka**: CLI na folder, od początku (P7, P8, P12).

**Demo do 2 min (P13):** naczepa czysta (zielona, bez ramek) → naczepa z dodatkiem (do sprawdzenia, ramka z pewnością, przełącznik wzorzec/badany) → ok. 10 s raportu partii z liczbami.

**Poza zakresem:** przeróbki konstrukcji i uszkodzenia (tylko kierunek w prezentacji, P10); odrzucanie ramek; opis słowny miejsca; widok obok siebie; kolejka na ekranie głównym; archiwum; klasyfikacja towaru; dane KAS (pkt 7 zadania).

**Założenia i pytania otwarte:** Z1 i Z2 (najryzykowniejsze) czekają na potwierdzenie Artura; sprzęt dla limitu czasu (P4); zachowanie na prawdziwych obrazach nieznane.

### 8. Release
Kolejność (02, uporządkowana): (1) generator + ocena + tryb folderu z raportem partii; (2) wykrywanie: rejestracja, nauka z wielu czystych, ramki, próg; (3) ekran; (4) pokaz. Raport partii nie wypada nawet przy braku czasu.
**Kryteria akceptacji** — w `docs/spec.md`.

### Ryzyka
- **Wynik bazowy** (`docs/wynik_bazowy.md`): na zbiorze trudnym FP 100% (setki fałszywych ramek na rozjechanych żebrach i przesuniętych paletach) — cele FP ≤ 10% wymagają rejestracji nieliniowej, wyrównania pasów detektora i porównania ładunku inaczej niż piksel w piksel. Reguła: jeśli po tych poprawkach FP lub FN nadal > 10% na zbiorze trudnym lub z pustym wzorcem, przechodzimy na mocniejszą metodę (PatchCore/PaDiM).
- **Ujednolicenie zapisów z 02 (braki 1b, P18) — poprawione w samym pliku 02:** jedna wersja Z2, Z1/Z3/Z6 bez „sumy FP+FN”. Poniżej treść ujednolicona: Z2 — FP i FN ≤ 10% osobno, na zbiorze trudnym i z pustym wzorcem; reguła porażki Z2: którykolwiek błąd > 10% → mocniejsza metoda. Z1 — FN ≤ 10% oraz tabela trafień wg miejsca × rozmiar; reguła porażki Z1: FN > 10% lub „mały w konstrukcji” poniżej założonych 80% → czulsze progi, wpis w ryzykach. Z3 — nauka z wielu czystych jest wymaganiem; eksperyment wybiera tylko sposób, kryterium: niższe FP i FN przy tym samym zbiorze (bez sumy). Z6 — oba błędy równe (P3), bez hierarchii.
- Dane syntetyczne ≠ prawdziwe; progi 10% i 80% bez źródła.
- Próg odcinania to najważniejsza gałka dla liczb jury (P19); zbyt wysoki zwiększa FN.
- Ochrona danych: tylko obrazy syntetyczne w repo, slajdach, makiecie.

<!-- skill: przeplywy-pm -->
<!-- skill: create-prd -->
