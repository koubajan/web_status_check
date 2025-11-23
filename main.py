import threading
import queue
import requests
import time

# Config
# Seznam webovych stranek ke kontrole
URLS_TO_CHECK = [
    "https://www.google.com",
    "https://www.seznam.cz",
    "https://www.idnes.cz",
    "https://www.bazos.cz",
    "https://www.wikipedia.org",
    "https://www.github.com",
    "https://www.spsejecna.cz",
    "https://www.apple.com",
    "https://blablalbalsdwdapdpla.com", # Test neexistujici domeny
    "https://httpbin.org/status/404", # Test chyby 404 Not Found
    "https://httpbin.org/status/500", # Test chyby 500 Internal Server Error
]
# Pocet soubezne pracujicich vlaken
NUM_WORKER_THREADS = 8

# Hlavicka, ktera napodobuje bezny prohlizec
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

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
    # Vytvoreni fronty a naplneni URL adresami
    url_queue = queue.Queue()
    for url in URLS_TO_CHECK:
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
