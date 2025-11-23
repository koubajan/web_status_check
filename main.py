import threading
import queue
import requests
import time

# Config
URL_FILE = "urls.txt"  # Soubor se seznamem URL adres
# Pocet soubezne pracujicich vlaken
NUM_WORKER_THREADS = 4

# Hlavicka, ktera napodobuje bezny prohlizec
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def load_urls_from_file(filename):
    """Nacte seznam URL ze souboru, ignoruje prazdne radky."""
    try:
        with open(filename, 'r') as f:
            # Odstrani prazdne znaky (jako \n) a preskoci prazdne radky
            urls = [line.strip() for line in f if line.strip()]
        return urls
    except FileNotFoundError:
        print(f"CHYBA: Soubor '{filename}' nebyl nalezen.")
        return []

def check_websites(q):
    """
    Pracovnik, ktery bere URL z fronty a kontroluje jejich stav.
    """
    while not q.empty():
        try:
            url = q.get_nowait()
        except queue.Empty:
            # Fronta je prazdna, vlakno konci
            break

        try:
            # Provedeme HTTP pozadavek s hlavickou a casovym limitem 5 sekund
            response = requests.get(url, headers=HEADERS, timeout=5)
            print(f"{url:<40} -> Stav: {response.status_code}")
        except requests.exceptions.RequestException as e:
            # Zpracovani chyb (napr. neexistujici domena, timeout)
            print(f"{url:<40} -> CHYBA: {e.__class__.__name__}")
        finally:
            # Oznacime ukol jako hotovy
            q.task_done()

if __name__ == "__main__":
    # Nacteni URL ze souboru
    urls_to_check = load_urls_from_file(URL_FILE)
    
    if not urls_to_check:
        print("Nebyly nalezeny zadne URL ke kontrole. Program konci.")
        exit()

    # Vytvoreni fronty a naplneni URL adresami
    url_queue = queue.Queue()
    for url in urls_to_check:
        url_queue.put(url)

    start_time = time.time()

    # Vytvoreni a spousteni vlaken
    threads = []
    for i in range(NUM_WORKER_THREADS):
        thread = threading.Thread(target=check_websites, args=(url_queue,))
        threads.append(thread)
        thread.start()

    # Pockame, az vsechna vlakna dokonci svou praci
    for thread in threads:
        thread.join()

    end_time = time.time()

    print(f"Hotovo kontola trvala {end_time - start_time:.2f} sekund.")
