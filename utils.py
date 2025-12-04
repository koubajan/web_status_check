import json

def load_config(filename="config.json"):
    """Nacte konfiguraci ze souboru JSON."""
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"CHYBA: Konfiguracni soubor '{filename}' nebyl nalezen.")
        return None
    except json.JSONDecodeError:
        print(f"CHYBA: Konfiguracni soubor '{filename}' ma neplatny format.")
        return None

def load_urls_from_file(filename):
    """Nacte seznam URL ze souboru, ignoruje prazdne radky."""
    try:
        with open(filename, 'r') as f:
            urls = [line.strip() for line in f if line.strip()]
        return urls
    except FileNotFoundError:
        print(f"CHYBA: Soubor s URL '{filename}' nebyl nalezen.")
        return []
