"""
DONOR CLASS // Facebook Operations Specialist Module
Oversees Meta platform distribution, page-to-page following, and post publishing.
"""

from pathlib import Path
from .config import (
    FB_PAGE_NAME,
    FB_PAGE_ID,
    FB_PAGE_URL,
    FB_TARGET_OUTLETS,
    ALLOW_EMOJIS,
    MAX_COMMENT_SENTENCES,
    MIN_COMMENT_SENTENCES,
    STRICT_ANONYMITY_SIGNATURE,
    BASE_URL,
)
from .state_manager import StateManager


class FacebookOperator:
    """Manages the Facebook operations for DONOR CLASS."""

    def __init__(self):
        self.sm = StateManager()
        self._ensure_state_initialized()

    def _ensure_state_initialized(self):
        fb_ops = self.sm.state.setdefault("facebook_operations", {})
        fb_ops.setdefault("page_name", FB_PAGE_NAME)
        fb_ops.setdefault("page_id", FB_PAGE_ID)
        fb_ops.setdefault("page_url", FB_PAGE_URL)
        fb_ops.setdefault("followed_pages", [])
        fb_ops.setdefault("published_posts", [])
        self.sm.save()

    def get_target_outlets(self) -> list:
        """Returns the master list of high-reach media outlets to follow."""
        return FB_TARGET_OUTLETS

    def get_pending_follows(self) -> list:
        """Returns target outlets that have not yet been recorded as followed."""
        followed_urls = {
            f.get("url")
            for f in self.sm.state.get("facebook_operations", {}).get("followed_pages", [])
        }
        return [o for o in FB_TARGET_OUTLETS if o["url"] not in followed_urls]

    def record_follow(self, outlet_name: str, outlet_url: str):
        """Records a completed page follow in state."""
        self.sm.record_facebook_follow(outlet_name, outlet_url)

    def validate_post_copy(self, copy: str) -> tuple[bool, str]:
        """Ensures post copy adheres to safety constraints (zero emoji, length)."""
        if not ALLOW_EMOJIS:
            # Check for non-ascii emoji characters
            for char in copy:
                if ord(char) > 0x1F000:
                    return False, f"Emoji detected: {char}. Zero-emoji policy violated."
        
        sentences = [s.strip() for s in copy.replace("!", ".").replace("?", ".").split(".") if s.strip()]
        sentence_count = len(sentences)
        
        # Post text should be punchy and analytical
        if sentence_count < MIN_COMMENT_SENTENCES:
            return False, f"Post copy too short ({sentence_count} sentences). Minimum is {MIN_COMMENT_SENTENCES}."
        
        return True, "Valid"

    def record_post(self, title: str, post_type: str, copy: str, url: str = None, media_path: str = None):
        """Records a published post to state."""
        valid, msg = self.validate_post_copy(copy)
        if not valid:
            raise ValueError(f"Post failed safety validation: {msg}")
            
        post_data = {
            "title": title,
            "type": post_type,
            "copy": copy,
            "url": url or BASE_URL,
            "media_path": media_path,
        }
        self.sm.record_facebook_post(post_data)

    def get_overview(self) -> dict:
        """Returns operational status for Facebook."""
        fb_ops = self.sm.state.get("facebook_operations", {})
        return {
            "page_name": fb_ops.get("page_name"),
            "page_id": fb_ops.get("page_id"),
            "page_url": fb_ops.get("page_url"),
            "followed_count": len(fb_ops.get("followed_pages", [])),
            "total_targets": len(FB_TARGET_OUTLETS),
            "published_posts_count": len(fb_ops.get("published_posts", [])),
        }
