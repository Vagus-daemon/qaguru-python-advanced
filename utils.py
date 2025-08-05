import json

from pathlib import Path


def load_users_data():
    try:
        file_path = Path("users.json")
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"error": "File users.json not found"}
    except json.JSONDecodeError:
        return {"error": "Invalid JSON format in users.json"}
