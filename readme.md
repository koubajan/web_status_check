# Parallel Web Checker with GUI

This project is a Python application for fast and concurrent checking of website availability. It uses multithreading to efficiently verify a large number of URL addresses at once. The application now includes a simple Graphical User Interface (GUI).

## Features

*   **Parallel Processing:** Checks run in multiple threads simultaneously.
*   **Graphical Interface:** A simple window for file selection and result display.
*   **Configuration:** Settings for thread count and timeouts in `config.json`.
*   **Modularity:** The code is split into logical modules.

## Requirements

*   Python 3.x
*   `requests` library

Install dependencies:
```bash
pip install requests
```
*(Note: The `tkinter` library for the GUI is a standard part of Python and does not need to be installed separately.)*

## How to Use

1.  **Run the application:**
    ```bash
    python main.py
    ```

2.  **In the application:**
    *   Click the **"Select URL File"** button.
    *   Select a text file (e.g., the included `urls.txt`) containing one website address per line.
    *   Click **"Start Checking"**.
    *   Results will be displayed in the text area within the window.

## Project Structure

*   `main.py`: The entry point of the application.
*   `gui.py`: Contains the Graphical User Interface logic (Tkinter).
*   `worker.py`: Contains the logic for checking websites (worker threads).
*   `utils.py`: Helper functions for loading files and configuration.
*   `config.json`: Application settings (thread count, headers, timeout).
*   `urls.txt`: Sample file with a list of URLs.
