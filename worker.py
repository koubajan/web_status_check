import queue
import requests

def check_website(q, headers, timeout):
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
            # Provedeme HTTP pozadavek s hlavickou a casovym limitem
            response = requests.get(url, headers=headers, timeout=timeout)
            print(f"{url:<40} -> Stav: {response.status_code}")
        except requests.exceptions.RequestException as e:
            # Zpracovani chyb (napr. neexistujici domena, timeout)
            print(f"{url:<40} -> CHYBA: {e.__class__.__name__}")
        finally:
            # Oznacime ukol jako hotovy
            q.task_done()
