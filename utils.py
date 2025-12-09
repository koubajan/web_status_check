import json

def load_config(filename="config.json"):
    """Loads configuration from a JSON file."""
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"ERROR: Configuration file '{filename}' not found.")
        return None
    except json.JSONDecodeError:
        print(f"ERROR: Configuration file '{filename}' has an invalid format.")
        return None

def load_urls_from_file(filename):
    """Loads a list of URLs from a file, ignoring empty lines."""
    try:
        with open(filename, 'r') as f:
            urls = [line.strip() for line in f if line.strip()]
        return urls
    except FileNotFoundError:
        print(f"ERROR: URL file '{filename}' not found.")
        return []
