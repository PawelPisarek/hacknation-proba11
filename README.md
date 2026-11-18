# hacknation-proba11
Próba 11 zespołu Hackathon (pomocnik)

## Uruchomienie (Python 3.10+)

```
pip install -r requirements.txt
python -m rtg porownaj wzorzec.bmp badany.bmp --raport wyniki   # JSON + PNG z zaznaczonymi obszarami
python -m rtg generuj dane/gen/test --ziarno 1                    # syntetyczny zbiór par .bmp + prawda.json
python -m rtg generuj dane/gen/duze --czyste 1 --dodatek 1 --szer 12000 --wys 4200   # pliki ~50 MB
python -m rtg ocena dane/gen/test                                 # FP/FN wg §6 zadania
python tests/test_dymny.py
```
Wynik bazowy: `docs/wynik_bazowy.md`. Próbka danych: `dane/probka/`.
