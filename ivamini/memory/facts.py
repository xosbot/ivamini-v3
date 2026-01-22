import json
from pathlib import Path

FACTS_PATH = Path(__file__).parent / "facts.json"

def load_facts() -> dict:
    if not FACTS_PATH.exists():
        return {}

    with open(FACTS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)
