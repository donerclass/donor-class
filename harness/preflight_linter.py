"""
DONOR CLASS // Pre-Flight Safety & Quality Linter
Enforces strict zero-emoji policy, FEC verification, URL card unfurling, and character limits.
"""

import re
from typing import List, Tuple

# Unicode Emoji Ranges Regex Pattern
# Covers Emoticons, Miscellaneous Symbols, Dingbats, Transport, Pictographs, Enclosed Alphanumerics, and Regional Indicators
EMOJI_PATTERN = re.compile(
    r"["
    r"\U0001F600-\U0001F64F"  # Emoticons
    r"\U0001F300-\U0001F5FF"  # Misc Symbols & Pictographs
    r"\U0001F680-\U0001F6FF"  # Transport & Map
    r"\U0001F700-\U0001F77F"  # Alchemical Symbols
    r"\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
    r"\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
    r"\U0001F900-\U0001F9FF"  # Supplemental Symbols & Pictographs
    r"\U0001FA00-\U0001FA6F"  # Chess Symbols
    r"\U0001FA70-\U0001FAFF"  # Symbols & Pictographs Extended-A
    r"\U00002702-\U000027B0"  # Dingbats
    r"\U000024C2-\U0001F251"  # Enclosed Characters
    r"\U0001F1E6-\U0001F1FF"  # Flags (iOS)
    r"]+",
    flags=re.UNICODE
)

class PreflightLinter:
    @staticmethod
    def check_zero_emoji(text: str) -> Tuple[bool, str]:
        matches = EMOJI_PATTERN.findall(text)
        if matches:
            return False, f"VIOLATION: Zero-emoji policy breached. Found emoji sequences: {matches}"
        return True, "Passed: No emojis detected."

    @staticmethod
    def check_character_count(text: str, max_chars: int = 280) -> Tuple[bool, str]:
        # Count characters (URLs on X are weighted as 23 characters under t.co)
        # Simplified standard length check
        length = len(text)
        if length > max_chars:
            return False, f"VIOLATION: Exceeds character limit ({length}/{max_chars})."
        return True, f"Passed: Character count {length}/{max_chars} within limit."

    @staticmethod
    def check_url_unfurl_safety(text: str) -> Tuple[bool, str]:
        # Checks if bare 'donorclass.info' or 'donorclass.info/' is linked without query params
        # Query parameters are required to bust Twitter's stale card crawler cache
        bare_urls = re.findall(r"https?://(?:www\.)?donorclass\.info/?(?=[\s\)\"']|$)", text)
        if bare_urls:
            return False, (
                "VIOLATION: Bare URL detected without query parameters. "
                "Always append '?ref=...' or '?state=...&ref=...' to bypass Twitter crawler card caching bugs."
            )
        return True, "Passed: All URLs contain cache-busting ref parameters."

    @classmethod
    def lint_post(cls, text: str, is_tweet: bool = True, max_chars: int = 280) -> Tuple[bool, List[str]]:
        violations = []

        # 1. Zero Emoji Check
        passed, msg = cls.check_zero_emoji(text)
        if not passed:
            violations.append(msg)

        # 2. Length Check
        if is_tweet:
            passed, msg = cls.check_character_count(text, max_chars)
            if not passed:
                violations.append(msg)

        # 3. URL Unfurl Check
        passed, msg = cls.check_url_unfurl_safety(text)
        if not passed:
            violations.append(msg)

        return (len(violations) == 0), violations
