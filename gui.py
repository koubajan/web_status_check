import tkinter as tk
from tkinter import filedialog, scrolledtext
import threading
import queue
import time

from utils import load_config, load_urls_from_file
from worker import check_website

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Parallel Web Checker")
        self.root.geometry("700x500")

        self.filepath = ""

        # --- GUI Elements ---
        self.frame = tk.Frame(root, padx=10, pady=10)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.btn_open = tk.Button(self.frame, text="Select URL File", command=self.open_file)
        self.btn_open.pack(fill=tk.X)

        self.lbl_file = tk.Label(self.frame, text="No file selected", pady=5)
        self.lbl_file.pack()

        self.btn_start = tk.Button(self.frame, text="Start Checking", command=self.start_checking, state=tk.DISABLED)
        self.btn_start.pack(fill=tk.X)

        self.output_text = scrolledtext.ScrolledText(self.frame, wrap=tk.WORD, state=tk.DISABLED)
        self.output_text.pack(fill=tk.BOTH, expand=True, pady=10)

    def open_file(self):
        """Opens a dialog to select a file."""
        filepath = filedialog.askopenfilename(
            title="Select a URL file",
            filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
        )
        if filepath:
            self.filepath = filepath
            self.lbl_file.config(text=f"Selected: {filepath}")
            self.btn_start.config(state=tk.NORMAL)

    def log_message(self, message):
        """Safely writes a message to the text area from any thread."""
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, message + "\n")
        self.output_text.see(tk.END) # Automatically scrolls down
        self.output_text.config(state=tk.DISABLED)

    def start_checking(self):
        """Starts the checking process in a separate thread to prevent the GUI from freezing."""
        self.btn_start.config(state=tk.DISABLED)
        self.btn_open.config(state=tk.DISABLED)
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        self.output_text.config(state=tk.DISABLED)

        # Run the logic in a new thread
        thread = threading.Thread(target=self.run_checker_thread)
        thread.start()

    def run_checker_thread(self):
        """The main checking logic that runs in the background."""
        config = load_config()
        if not config:
            self.log_message("ERROR: Could not load config.json")
            self.reset_ui()
            return

        urls_to_check = load_urls_from_file(self.filepath)
        if not urls_to_check:
            self.log_message(f"ERROR: File '{self.filepath}' is empty or does not exist.")
            self.reset_ui()
            return

        self.log_message(f"Starting check for {len(urls_to_check)} websites...\n")

        url_queue = queue.Queue()
        for url in urls_to_check:
            url_queue.put(url)

        start_time = time.time()

        threads = []
        for _ in range(config["num_worker_threads"]):
            thread = threading.Thread(
                target=check_website,
                args=(url_queue, config["headers"], config["request_timeout"], self.log_message)
            )
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        end_time = time.time()
        self.log_message("\n--- Done ---")
        self.log_message(f"Total check time: {end_time - start_time:.2f} seconds.")
        self.reset_ui()

    def reset_ui(self):
        """Resets the UI buttons to their initial state."""
        self.btn_start.config(state=tk.NORMAL)
        self.btn_open.config(state=tk.NORMAL)
