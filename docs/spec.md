# Spec — wyszukiwarka anomalii RTG (dla Programisty)

Źródła: `docs/pm/03-write-prd.md`, `docs/decyzje.md`, `docs/zadanie.md`. Wszystko w tekstach ekranu po polsku. Dane tylko syntetyczne.

## 1. Co zobaczy i zrobi użytkownik (według Artura)
Operator otwiera naczepę i widzi jeden obraz na całą szerokość z oceną na górze. Przełącza „wzorzec / badany”, czyta pewność przy ramkach, przyciskiem otwiera raport partii. Niczego nie odrzuca.

## 2. Ekrany makiety
### Ekran A — naczepa (główny)
Dokładnie cztery elementy (08:38):
1. **Linia oceny** nad obrazem: zielona „Czysta — 0 miejsc” albo bursztynowa „Do sprawdzenia — N miejsc”. Zielona **tylko** przy zerze zaznaczeń (P19).
2. **Obraz** na całą szerokość (~1000×360). Na badanym ramki z etykietą „#N · pewność” (numer + pewność), bez opisu słownego. Wzorzec — bez ramek.
3. **Przełącznik** „wzorzec | badany” nad obrazem: to samo miejsce, ta sama skala.
4. **Przycisk** „Raport z partii” → ekran B.
Nie ma: listy miejsc, zapisu, progu odcinania, przycisków „Poprzednia / Następna”, odrzucania ramek, widoku obok siebie. Do dema wybór naczepy robi makieta poza tymi czterema elementami (np. adres/parametr w URL lub dwa pliki), nie element ekranu.
**Dane udawane (makieta), każda liczba z podpisem zbioru:** naczepa 1 — czysta, zielona, 0 ramek (zbiór łatwy); naczepa 2 — z dodatkiem, „Do sprawdzenia — 2 miejsca”, ramki #1 94%, #2 71% (zbiór łatwy).
### Ekran B — raport partii
1. **Liczby u góry**: obrazy bez alarmu, obrazy z alarmem, liczba ramek, **próg odcinania** (jawnie, P19), czas/obraz.
2. **Dwa zbiory obok siebie: łatwy i trudny** (każda liczba podpisana nazwą zbioru). Gdy `prawda.json`: FP (x/y, %), FN (x/y, %) osobno, tabela trafień dodatków miejsce (konstrukcja / ładunek) × rozmiar (mały / duży).
3. **Lista naczep** z oceną, klik → ekran A.
4. **Lista miejsc** wybranej naczepy: #N, położenie, pewność.
5. **„Zapisz do pliku”** (JSON + HTML) — tylko tu. „Wróć do naczepy”.
**Dane udawane:** z `rtg ocena` na obu zbiorach, jeśli są; inaczej wartości przykładowe z podpisem „przykład, zbiór łatwy / trudny”. Wartość bazowa dziś (`docs/wynik_bazowy.md`): łatwy FP 0/20, FN 2/20; trudny FP 20/20, FN 4/20 — nie ukrywać.

### Definicje do pomiaru
- **Konstrukcja / ładunek**: strefa obrazu, w której generator umieścił dodatek — `miejsce` w `prawda.json`: „konstrukcja” = ramy, podwozie i pas dolny (`strefy["konstrukcja"]` w `rtg/generator.py`), „ladunek” = obszar palet.
- **Mały / duży**: `rozmiar` = „maly”, gdy pole bbox dodatku < 0,1% powierzchni obrazu (np. < 360 px² dla 1000×360), inaczej „duzy”. Próg to założenie robocze bez źródła; zapisuje go generator.
- `prawda.json`: pola `miejsce` (już jest) i `rozmiar` (do dopisania) przy każdym dodatku — ustalenie Szefa 08:46.

## 3. Pokaz (do 2 min)
Ekran A czysta (≈25 s) → ekran A z dodatkiem, przełącznik wzorzec/badany (≈45 s) → ekran B, liczby (≈10 s) + zdanie o kierunku (przeróbki konstrukcji, tylko w prezentacji).

## 4. Wejście i wyjście
- **Wejście**: pary `*.bmp` (wzorzec, badany) lub folder; wzorce czyste do nauki (pkt 5). Duże pliki ~50 MB, przetwarzanie partiami.
- **Wyjście na obraz**: PNG z ramkami + JSON (`ramki[]: bbox, pewność, numer`, `ocena`, `czas_s`, `prog`); na partię: zbiorczy HTML + JSON (liczby jak w ekranie B).
- Wzorzec wybiera system (najbliższy z wzorców czystych); model uczony na wielu czystych.

## 5. Komendy
- `python -m rtg generuj KATALOG [--czyste N --dodatek N --ziarno S --trudny --pusty-wzorzec]` — syntetyczny zbiór + `prawda.json`.
- `python -m rtg porownaj WZORZEC BADANY [--raport KATALOG]` — jedna para.
- `python -m rtg ocena KATALOG [--k K --json PLIK]` — FP/FN osobno.
- `python -m rtg porownaj --folder KATALOG` — tryb folderu bez człowieka, raport partii (ustalone, Szef 08:46). Gdy w folderze jest `prawda.json`, raport dokłada FP, FN i tabelę miejsce × rozmiar.

## 6. Miary
FP i FN **osobno**, na obraz, jak w `rtg/ocena.py`; roboczo każdy ≤ 10% (bez źródła). Trafienia dodatków wg miejsca × rozmiaru. Pomiar na zbiorach trudnym i z pustym wzorcem.

## 7. Testy akceptacji
1. `generuj --trudny` i `--pusty-wzorzec`, `ocena`: FP ≤ 10% i FN ≤ 10% osobno na każdym (Z2). Dziś niespełnione: FP 100% na trudnym.
2. Czysty obraz → „zielona”, 0 ramek; obraz z dodatkiem → „do sprawdzenia”, ≥ 1 ramka na dodatku.
3. Tabela trafień miejsce × rozmiar; komórka „mały w konstrukcji” ≥ 80% (Z1, założenie).
4. Nauka z wielu czystych: wybrany sposób ma FP i FN, każdy osobno, niższe o ≥ 20% względnie od najprostszego (Z3).
5. Czas analizy: < 1 min na obraz ~50 MB na zwykłym laptopie z CPU; ≥ 60 s → zmniejszenie skali i zapis założenia (Z5). Baza: 1,7 s liczenie, ~4 s z wczytaniem.
6. Próba z człowiekiem na makiecie (Artur/Paweł): „czy naczepa jest czysta i gdzie jest dodatek?” — poprawna odpowiedź w < 10 s bez wyjaśnień (Z4).
7. Ekran A zawiera dokładnie cztery elementy z sekcji 2; lista miejsc, zapis do pliku i próg tylko w ekranie B.
8. `porownaj --folder` z `prawda.json` → raport z FP, FN, tabelą; bez `prawda.json` → liczby bez alarmu / z alarmem / ramek.
9. Każda liczba w makiecie podpisana zbiorem (łatwy / trudny); raport partii pokazuje oba.
10. Uruchomienie z README przez osobę z zewnątrz; licencja MIT; w repo, makiecie i slajdach tylko dane syntetyczne.

## 8. Ryzyka i kryteria (z `/discover`)
Najryzykowniejsze założenia: Z1 (syntetyczne dodatki wystarczająco podobne do prawdziwych i trafiane, także małe w konstrukcji), Z2 (różnica po rejestracji daje mało alarmów na trudnym zbiorze). Reguły porażki i ujednolicenie zapisów — `docs/pm/03-write-prd.md`, sekcja Ryzyka. Zmiana metody (PatchCore/PaDiM) tylko gdy pomiar na zbiorze trudnym tego wymaga.

<!-- skill: przeplywy-pm -->
