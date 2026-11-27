import re


def clean_text(text: str) -> str:
    text = text.replace("\r\n", " ").replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def validate_text(text: str, min_words: int = 3, max_chars: int = 12000) -> None:
    if not text:
        raise ValueError("Text is empty.")

    word_count = len(text.split())
    if word_count < min_words:
        raise ValueError(f"Text is too short: {word_count} words. Minimum: {min_words}.")

    if len(text) > max_chars:
        raise ValueError(
            f"Text is too long for MVP: {len(text)} characters. Maximum: {max_chars}. "
            "Split it into smaller files or shorter sections."
        )
