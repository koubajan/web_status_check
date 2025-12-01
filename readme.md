## Parallel Website Checker

This simple Python script is used for **quickly and concurrently checking the availability of websites**.

-----

### How It Works

The program reads a list of URLs from the file **`urls.txt`** and simultaneously verifies the status of each page using several threads (workers). This makes the process much faster...

-----

### How to Use

1.  **Install the necessary libraries:**

    ```bash
    pip install requests
    ```

2.  **Edit the `urls.txt` file:** Add or remove the web addresses you want to check. Each address must be on a **separate line**.

3.  **Run the script:**

    ```bash
    python main.py
    ```

The output will be displayed directly in the terminal, showing the **status code** for each URL (e.g., **200 for success**) or an **error** if the page is unavailable.
