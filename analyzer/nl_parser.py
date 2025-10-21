import re

class NLParseError(ValueError):
    pass

def parse_nl_query(q: str) -> dict:
    """
    Very small heuristic parser. Returns parsed filters dict or raises NLParseError.
    Recognized outputs (keys): is_palindrome (bool), word_count (int),
    min_length (int), max_length (int), contains_character (single-char str)
    """
    if not q or not isinstance(q, str):
        raise NLParseError("query must be a non-empty string")

    s = q.lower().strip()
    filters = {}

    # single word / one word
    if re.search(r"\bsingle word\b", s) or re.search(r"\b1 word\b") or re.search(r"\bone word\b"):
        filters["word_count"] = 1

    # palindromic
    if re.search(r"\bpalindrom", s) or re.search(r"\bpalindrome\b", s):
        filters["is_palindrome"] = True

    # strings longer than N -> min_length = N+1
    m = re.search(r"longer than (\d+)", s)
    if m:
        filters["min_length"] = int(m.group(1)) + 1

    # strings at least N -> min_length = N
    m = re.search(r"at least (\d+)", s)
    if m:
        filters["min_length"] = int(m.group(1))

    # strings shorter than N -> max_length = N-1
    m = re.search(r"shorter than (\d+)", s)
    if m:
        filters["max_length"] = int(m.group(1)) - 1

    # contains letter X / containing the letter x
    m = re.search(r"contains(?:ing)? (?:the )?letter (\w)", s)
    if m:
        filters["contains_character"] = m.group(1)

    # "contain the first vowel" heuristic -> 'a'
    if "first vowel" in s:
        filters.setdefault("contains_character", "a")

    # "strings containing the letter z"
    m = re.search(r"containing the letter (\w)", s)
    if m:
        filters["contains_character"] = m.group(1)

    # if nothing parsed, error
    if not filters:
        raise NLParseError("Unable to parse natural language query")

    # validations: word_count must be positive int; contains_character single char
    if "word_count" in filters:
        try:
            filters["word_count"] = int(filters["word_count"])
            if filters["word_count"] < 1:
                raise NLParseError("word_count must be >= 1")
        except Exception:
            raise NLParseError("word_count is invalid")

    if "contains_character" in filters:
        ch = filters["contains_character"]
        if not isinstance(ch, str) or len(ch) != 1:
            raise NLParseError("contains_character must be a single character")
        filters["contains_character"] = ch.lower()

    return filters
