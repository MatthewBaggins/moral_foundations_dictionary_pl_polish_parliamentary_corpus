import json

def load_json(path: str) -> list | dict:
    """Load the file into JSON in one line with context manager."""
    
    with open(path, encoding='utf-8') as f:
        j = json.load(f)
    return j

def dump_json(obj: list | dict, path: str) -> None:
    """Load data into a JSON file in one line with context manager."""
    
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(obj, f)

def load_dict(path: str) -> dict:
    with open(path, 'r', encoding='utf-8') as f:
        loaded = json.load(f)
    assert isinstance(loaded, dict)
    return loaded

def load_list(path: str) -> list:
    with open(path, 'r', encoding='utf-8') as f:
        loaded = json.load(f)
    assert isinstance(loaded, list)
    return loaded

