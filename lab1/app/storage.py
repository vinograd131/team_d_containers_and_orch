import json
import os
from pathlib import Path

DATA_DIR = Path(os.getenv("DATA_DIR", "data"))
HABITS_FILE = DATA_DIR / "habits.json"


def load_habits() -> list[dict]:
    if not HABITS_FILE.exists():
        return []
    with open(HABITS_FILE, encoding="utf-8") as f:
        return json.load(f)


def save_habits(habits: list[dict]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(HABITS_FILE, "w", encoding="utf-8") as f:
        json.dump(habits, f, ensure_ascii=False, indent=2)