def load_text_file(path: str) -> str:
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    return text

def dump_text_file(text: str, path: str) -> None:
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)