# Spec — wyszukiwarka anomalii RTG (dla Programisty)

Źródła: `docs/pm/03-write-prd.md`, `docs/decyzje.md`, `docs/zadanie.md`. Wszystko w tekstach ekranu po polsku. Dane tylko syntetyczne.

## 1. Co zobaczy i zrobi użytkownik (według Artura)
Operator otwiera naczepę i widzi jeden obraz na całą szerokość z oceną na górze. Przełącza „wzorzec / badany”, czyta pewność przy ramkach, przyciskiem otwiera raport partii. Niczego nie odrzuca.

## 2. Ekrany makiety
### Ekran A — naczepa (główny)
Układ od góry:
1. **Linia oceny** (jedna): zielona „Czysta — 0 miejsc” albo bursztynowa „Do sprawdzenia — N miejsc”. Zielona **tylko** przy zerze zaznaczeń (P19).
2. **Pasek obrazu**: przełącznik „wzorzec | badany” (ta sama pozycja i skala, bez przeskoku) oraz podpis „Próg odcinania: k=4,0” (jawny; z jednej wartości — z raportu).
3. **Obraz** na całą szerokość (proporcje ~1000×360). Na badanym ramki z etykietą „#N · 87%” (numer + pewność), bez opisu słownego. Wzorzec — bez ramek.
4. **Przycisk** „Raport z partii” → ekran B.
Nic więcej: bez listy miejsc, bez zapisu, bez odrzucania ramek, bez widoku obok siebie.
**Dane udawane (makieta):** dwie naczepy z `dane/probka` lub generatora: (1) czysta — zielona, 0 ramek; (2) z dodatkiem — „Do sprawdzenia — 2 miejsca”, ramki #1 94%, #2 71%. Przełączanie między naczepami przyciskami „Poprzednia / Następna” w stopce (potrzebne do dema).
### Ekran B — raport partii
1. **Liczby u góry**: obrazy bez alarmu, obrazy z alarmem, liczba ramek, próg odcinania, czas/obraz.
2. Gdy `prawda.json`: FP (x/y, %), FN (x/y, %) osobno, tabela trafień dodatków miejsce (konstrukcja / ładunek) × rozmiar (mały / duży).
3. **Lista naczep** z oceną (zielona / do sprawdzenia, liczba miejsc), klik → ekran A.
4. **Lista miejsc** wybranej naczepy: #N, położenie (x, y, szer., wys.), pewność.
5. Przycisk „Zapisz do pliku” (JSON + HTML) — tylko tu. „Wróć do naczepy”.
**Dane udawane:** 20 czystych + 20 z dodatkiem, np. 20/0 bez alarmu na czystych oraz 18 z alarmem na dodatkach; liczby z `rtg ocena`, nie wymyślone ręcznie, jeśli są dostępne.

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
- **Do dodania** (propozycja Projektanta, wymaga zgody Szefa): tryb folderu z raportem partii (np. `porownaj --folder KATALOG`) bez człowieka; `ocena` ma dodać podział wg miejsca × rozmiaru (generator musi zapisywać w `prawda.json` pola `miejsce` i `rozmiar` dodatku).

## 6. Miary
FP i FN **osobno**, na obraz, jak w `rtg/ocena.py`; roboczo każdy ≤ 10% (bez źródła). Trafienia dodatków wg miejsca × rozmiaru. Pomiar na zbiorach trudnym i z pustym wzorcem.

## 7. Testy akceptacji
1. `generuj --trudny` i `--pusty-wzorzec`, `ocena`: FP ≤ 10% i FN ≤ 10% na każdym. (Wynik bazowy dziś: FP 100% na trudnym — nie spełnione.)
2. Czysty obraz → ocena „zielona”, 0 ramek; obraz z dodatkiem → „do sprawdzenia”, ≥ 1 ramka na dodatku.
3. Czas analizy < 1 min na obraz ~50 MB na zwykłym laptopie z CPU (wynik bazowy 1,7 s liczenie, ~4 s z wczytaniem).
4. Folder z `prawda.json` → raport partii z FP, FN i tabelą miejsce × rozmiar; bez `prawda.json` → same liczby bez alarmu / z alarmem / ramek.
5. Próg odcinania widoczny na ekranie A i w raporcie.
6. Ekran A zawiera dokładnie: ocenę, obraz z ramkami, przełącznik, przycisk raportu; lista miejsc i zapis do pliku tylko w ekranie B.
7. Narzędzie uruchamia osoba z zewnątrz z README (CLI na folder), licencja MIT.
8. W repo, makiecie i slajdach tylko obrazy syntetyczne.

## 8. Ryzyka i kryteria (z `/discover`)
Najryzykowniejsze założenia: Z1 (syntetyczne dodatki wystarczająco podobne do prawdziwych i trafiane, także małe w konstrukcji), Z2 (różnica po rejestracji daje mało alarmów na trudnym zbiorze). Reguły porażki i ujednolicenie zapisów — `docs/pm/03-write-prd.md`, sekcja Ryzyka. Zmiana metody (PatchCore/PaDiM) tylko gdy pomiar na zbiorze trudnym tego wymaga.

<!-- skill: przeplywy-pm -->
