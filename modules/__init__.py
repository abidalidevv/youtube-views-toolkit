

def slugify(text: str) -> str:
    import re
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    return re.sub(r'[\s_-]+', '-', text)


def get_env(key: str, default: str = '') -> str:
    import os
    return os.environ.get(key, default)
