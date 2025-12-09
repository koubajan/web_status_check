import queue
import requests

def check_website(q, headers, timeout, logger=print):
    """
    A worker that takes a URL from the queue and checks its status.
    logger: A function to be called for logging messages (defaults to print).
    """
    while not q.empty():
        try:
            url = q.get_nowait()
        except queue.Empty:
            # The queue is empty, the thread can finish.
            break

        try:
            # Perform the HTTP request
            response = requests.get(url, headers=headers, timeout=timeout)
            msg = f"{url:<40} -> Status: {response.status_code}"
            logger(msg) # Send the message to the GUI or console
        except requests.exceptions.RequestException as e:
            msg = f"{url:<40} -> ERROR: {e.__class__.__name__}"
            logger(msg)
        finally:
            q.task_done()
