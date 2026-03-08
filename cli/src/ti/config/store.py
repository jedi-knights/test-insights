import json
from pathlib import Path

CONFIG_DIR = Path.home() / ".config" / "test-insights"
CONFIG_FILE = CONFIG_DIR / "config.json"


def load() -> dict:
    if not CONFIG_FILE.exists():
        return {}
    return json.loads(CONFIG_FILE.read_text())


def save(data: dict) -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(data, indent=2))


def get(key: str, default=None):
    return load().get(key, default)


def set_key(key: str, value) -> None:
    data = load()
    data[key] = value
    save(data)


def delete_key(key: str) -> None:
    data = load()
    data.pop(key, None)
    save(data)
