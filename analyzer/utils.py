import hashlib
from collections import Counter

def analyze_string(value: str):
    value_stripped = value.strip()
    properties = {
        "length": len(value_stripped),
        "is_palindrome": value_stripped.lower() == value_stripped[::-1].lower(),
        "unique_characters": len(set(value_stripped)),
        "word_count": len(value_stripped.split()),
        "sha256_hash": hashlib.sha256(value_stripped.encode('utf-8')).hexdigest(),
        "character_frequency_map": dict(Counter(value_stripped))
    }
    return properties
