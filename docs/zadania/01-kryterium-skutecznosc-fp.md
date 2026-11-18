# 01 — kryterium: skuteczność (FP/FN), waga 40%

**Co jest (08:20, docs/wynik_bazowy.md):** zbiór łatwy test FP 0/20, FN 2/20; zbiór trudny test (przesunięty ładunek,
rozciągnięcie, artefakty detektora) **FP 20/20, FN 4/20**, 419 fałszywych ramek; pusty wzorzec FP 20/20.
**Czego brakuje:** metoda piksel-w-piksel alarmuje na każdym realistycznym czystym obrazie — jury liczy FP na czystych.
**Poprawka (faza 2, strojenie):** próg k i minimalny rozmiar regionu dobrane na trudnym dev; tryb „ostrożny”
(raport tylko regionów z wysoką pewnością); w materiałach pokazać wynik na obu zbiorach uczciwie.
W fazie 1 Programista już poprawia metodę z treści zadania (dopasowanie nieliniowe, wyrównanie wierszy/kolumn).

**09:10 v1 (docs/wynik_bazowy.md):** trudny test FP 5/20 (25%), FN 2/20; łatwy test FN 3/20 (było 2); pusty wzorzec FP 20/20.
Nadal FP > 10% na trudnym i 100% przy pustym wzorcu — plan „wzorzec z wielu czystych” (Programista).

## 09:14 — po ujednoliceniu „mały” (8b0aef0)
Liczby FP/FN bez zmian. Małych dodatków w test tylko 15 (konstrukcja/małe: 2/2 trudny, 0/1 pusty wz.) — skuteczność na małych niemierzalna; zbiór z wymuszonymi małymi w toku.
