"""Utility functions for string operations and formatting."""


def slugify(text: str) -> str:
    """Convert text into a URL-friendly slug."""
    import re
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    return re.sub(r"[-\s]+", "-", text)


def truncate(text: str, max_len: int = 100, suffix: str = "...") -> str:
    """Truncate text to a specified length."""
    if len(text) <= max_len:
        return text
    return text[: max_len - len(suffix)] + suffix
