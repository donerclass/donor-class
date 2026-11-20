"""
DONOR CLASS // Autonomous Operational Harness Configuration
Nonpartisan Campaign Finance Distribution & Intelligence Engine
"""

import os
from pathlib import Path

# Paths
HARNESS_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = HARNESS_DIR.parent
DATA_FILE = PROJECT_ROOT / "data" / "donor-dataset.js"
STATE_FILE = HARNESS_DIR / "state.json"
ASSETS_DIR = PROJECT_ROOT / "assets"
INFOGRAPHICS_DIR = ASSETS_DIR / "infographics"
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
DOCS_DIR = PROJECT_ROOT / "docs"

# Production Domain & URLs
BASE_URL = "https://donorclass.info"
CLOUDFLARE_PAGES_URL = "https://donor-class-civic.pages.dev"
ADSENSE_PUB_ID = "ca-pub-6657813406289371"

# Social Channel Identities
X_HANDLE = "donorclassinfo"
X_PROFILE_URL = "https://x.com/donorclassinfo"
REDDIT_USER = "DonorClassInfo"
REDDIT_PROFILE_URL = "https://www.reddit.com/user/DonorClassInfo/"

# Timezone Synchronization
TIMEZONE_PRIMARY = "Asia/Manila"      # User Local Routine (PHT, UTC+8)
TIMEZONE_SECONDARY = "America/New_York" # Target Audience Market (EST/EDT, UTC-5)

# Daily Schedule Milestones (PHT)
SCHEDULE_MORNING_BRIEF = "05:30"     # 5:30 AM PHT (4:30 PM EST previous day)
SCHEDULE_PRIME_DROP = "22:30"        # 10:30 PM PHT (9:30 AM EST prime US morning)
SCHEDULE_NIGHTLY_AUDIT = "04:30"     # 4:30 AM PHT (pre-brief synthesis)

# Safety Guardrails & Quotas
ALLOW_EMOJIS = False                 # Strict zero-emoji policy across all outputs
MAX_DAILY_NEWS_SNIPES = 5            # Rate-limit safety against social spam heuristics
MIN_JITTER_SECONDS = 15              # Anti-bot post delay minimum
MAX_JITTER_SECONDS = 45              # Anti-bot post delay maximum
STRICT_ANONYMITY_SIGNATURE = "Donor Class Team <contact@donorclass.info>"

# 50 States in 50 Days Ordered Schedule
STATE_SCHEDULE = [
    "TX", "CA", "FL", "NY", "PA", "IL", "OH", "GA", "NC", "MI",
    "NJ", "VA", "WA", "AZ", "TN", "MA", "IN", "MO", "MD", "WI",
    "CO", "MN", "SC", "AL", "LA", "KY", "OR", "OK", "CT", "UT",
    "IA", "NV", "AR", "MS", "KS", "NM", "NE", "ID", "WV", "HI",
    "NH", "ME", "MT", "RI", "DE", "SD", "ND", "AK", "VT", "WY"
]
