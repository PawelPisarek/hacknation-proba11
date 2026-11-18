# Materiały zadania (krok 0)

Źródło: `docs/zadanie.md` (KAS, wykrywanie anomalii na RTG środków przewozowych) i `docs/decyzje.md`.

## 1. Dane wejściowe (z treści zadania, pkt 7)
| Co | Wartość | Uwaga |
|---|---|---|
| Liczba obrazów | ~200 | pary/grupy „przed/po załadunku” |
| Format | `*.bmp` | |
| Rozmiar | ~50 MB/obraz, ~10 GB łącznie | wymaga przetwarzania partiami/kafelkami, kompresji |
| Dane | anonimizowane, symulacyjne | |
| Dostęp | pendrive na stoisku KAS | **my nie mamy** → syntetyczny zbiór (decyzje 08:09) |
| Status | dane chronione: zakaz udostępniania, kopiowania, użycia poza hackathonem | nie commitować do publicznego repo |
| Urządzenia źródłowe | Nuctech, Multicontrol | docelowa integracja z repozytorium obrazów |

## 2. Wymagania funkcjonalne
- Porównanie pary (wzorzec vs badany): podobieństwa i różnice (anomaly detection, segmentacja, porównania pikselowe).
- Wykrycie odstępstwa od „reguły” (pusty/wzorcowy środek vs z dodatkami).
- Raport z zaznaczonymi obszarami na obrazie.
- Obsługa `*.bmp`, duże pliki (~50 MB), kompresja, przetwarzanie partiami, skalowalność.
- Autonomia (bez interwencji człowieka); nauka na obrazach wzorcowych „prawidłowych” (pkt 5).
- Czas: < 1 min na obraz (pkt 7).

## 3. Sposób testowania (pkt 6)
- Zestaw obrazów „czystych”: żadnych alarmów; alarm = false positive (liczony poziom FP).
- Zestaw z „dodatkami” (nie-konstrukcyjnymi): model ma wskazać miejsce graficznie; brak wskazania = false negative (liczony poziom FN).
- Kryteria oceny: brak w treści (pkt 8 — zna Szef).

## 4. Wymagania formalne (pkt 4)
Tytuł + szczegółowy opis, repozytorium kodu, prezentacja PDF ≤ 10 slajdów. Opcjonalnie: zrzuty, linki do demo, grafiki.

## 5. Ograniczenia
- Docelowo działanie offline, bez chmury/silnika AI w internecie (pkt 9); na hackathonie narzędzia AI (też płatne) dozwolone do tworzenia kodu.
- Dane KAS chronione (patrz wyżej) — w repo tylko generator i małe syntetyczne próbki.
- Wyniki docelowo przypisywane do miejsca i przedmiotu kontroli (pkt 9).
- Obecne narzędzie KAS wykrywa papierosy; słabe przy małych ilościach w elementach konstrukcyjnych → ważne: detale, przeróbki, skrytki (pkt 1).

## 6. Luki (czego treść nie mówi)
1. Kryteria oceny (pkt 8 puste) — wagi FP/FN, jakość lokalizacji, UX, skalowalność.
2. Definicja trafienia lokalizacji: IoU? próg? wystarczy środek w ramce? Co z częściowym pokryciem.
3. Definicja FP: alarm na obraz czy liczba zaznaczonych regionów na obraz; czy alarm poza dodatkiem na obrazie z dodatkiem to FP.
4. Docelowe progi FP/FN (akceptowalny poziom).
5. Rozdzielczość/geometria/głębia bitowa BMP (mono/RGB, 8/16 bit), przekrój/ skala szarości; format pary: czy wzorzec i badany to ten sam pojazd, czy ten sam typ.
6. Czy obrazy w parze są zarejestrowane (wyrównane); skala/przesunięcie/obrót między „przed” a „po”.
7. Ile typów pojazdów (naczepa, kontener, autokar, wagon) i ile wzorców na typ; czy test obejmuje nieznane typy.
8. Typy i rozmiary „dodatków” w zbiorze testowym (papierosy, drobne skrytki?).
9. Czy „grupy” oznaczają >2 obrazów i jak porównywać (wzorzec z wielu?).
10. Sprzęt docelowy/testowy (CPU/GPU, RAM) dla limitu < 1 min.
11. Format raportu (obraz z nakładką, JSON, współrzędne?) i integracja z repozytorium.
12. Czy „uszkodzenia” (pkt 2) liczą się jako anomalie w testach.
13. Czy jury uruchamia nasz kod na swoich danych (tryb, środowisko), czy ocenia wyniki/prezentację.
14. Licencja/własność kodu przy ewentualnym wdrożeniu.

Liczba luk: **14**.

## 7. Publiczne źródła/zbiory zastępcze (wyszukane 18.11.2026; licencje i dostęp niezweryfikowane)
Wniosek: **brak otwartego zbioru realnych RTG naczep/ciężarówek par „pusty/załadowany”**. Publiczne zbiory to głównie bagażowe — inna energia promieniowania, nie nadają się wprost; służą co najwyżej do pretrainingu/wzorców dodatków.
- SIXray (bagaż, ~1,06 mln obr.) i PIDray (bagaż, ~47,7 tys., 12 klas), HiXray (na zapytanie), CLCXray — przegląd: https://arxiv.org/pdf/2507.17508 ; SIXray: https://arxiv.org/pdf/1901.00303.pdf
- CargoX — pierwszy publiczny benchmark cargo, ale syntetyczny (wklejone przedmioty w kadry cargo RTG); dostęp/licencja niepotwierdzone, szukać w pracy MFA-net.
- Przegląd analizy RTG cargo (Empty Cargo Verification, kontekst): https://arxiv.org/pdf/1608.01017
- Threat Image Projection w cargo (metoda dla naszego generatora syntetyki): https://discovery-pp.ucl.ac.uk/id/eprint/1568939/1/threat%20image%20projection%20%28TIP%29%20into%20X-ray%20images%20of%20cargo%20containers%20for%20training%20humans%20and%20machines.pdf
- CXR-AD (RTG komponentów przemysłowych, detekcja anomalii; tylko analogia): https://arxiv.org/pdf/2505.03412
- Roboflow „truck_loading” (modalność nieznana, prawdopodobnie zdjęcia, nie RTG): https://universe.roboflow.com/tolasing/truck_loading

Rekomendacja: własny generator syntetyczny (naczepa jako tło + rozproszone kształty „dodatków” metodą TIP, rozmiary ~50 MB BMP) z parami wzorzec/badany i maskami prawdy; do kafelkowania i metryk FP/FN ustalić własną definicję trafienia (luka 2–3) i opisać ją w `docs/decyzje.md`.
