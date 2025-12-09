import tkinter as tk
from gui import App

def main():
    """
    Creates the main application window and runs the GUI.
    """
    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()
