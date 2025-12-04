import threading
import queue
import time
from utils import load_config, load_urls_from_file
from worker import check_website

def main():
    """
    Hlavni funkce pro spusteni paralelni kontroly webu.
    """
    # Nacteni konfigurace
    config = load_config()
    if not config:
        return

    # Nacteni URL ze souboru specifikovaneho v konfiguraci
    urls_to_check = load_urls_from_file(config["url_file"])
    if not urls_to_check:
        print("Nebyly nalezeny zadne URL ke kontrole. Program konci.")
        return

    print(f"Spoustim paralelni kontrolu {len(urls_to_check)} webovych stranek...\n")

    # Vytvoreni fronty a naplneni URL adresami
    url_queue = queue.Queue()
    for url in urls_to_check:
        url_queue.put(url)

    start_time = time.time()

    # --- Vytvoreni a spousteni vlaken ---
    threads = []
    for i in range(config["num_worker_threads"]):
        thread = threading.Thread(
            target=check_website,
            args=(url_queue, config["headers"], config["request_timeout"])
        )
        threads.append(thread)
        thread.start()

    # --- Cekani na dokonceni ---
    for thread in threads:
        thread.join()

    end_time = time.time()

    print("\n--- Hotovo ---")
    print(f"Celkovy cas kontroly: {end_time - start_time:.2f} sekund.")

if __name__ == "__main__":
    main()
