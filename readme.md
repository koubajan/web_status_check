# Paralelni Kontrola Webu

Tento jednoduchy skript v Pythonu slouzi k rychle a soubezne kontrole dostupnosti webovych stranek.

## Jak to funguje

Program nacte seznam URL adres ze souboru `urls.txt` a pomoci nekolika vlaken (pracovniku) soucasne overi stav kazde stranky. Je to rychlejsi...

## Jak pouzit

1.  **Nainstalujte potrebne knihovny:**
    ```bash
    pip install requests
    ```

2.  **Upravte soubor `urls.txt`:**
    Pridejte nebo odeberte webove adresy, ktere chcete kontrolovat. Kazda adresa musi byt na samostatnem radku.

3.  **Spustte skript:**
    ```bash
    python main.py
    ```

Vystup se zobrazi primo v terminalu a ukaze stavovy kod pro kazdou URL (napr. 200 pro uspech) nebo chybu, pokud stranka neni dostupna.
