"""bot package initializer.

Avoid importing heavy modules at package import time to prevent
unnecessary dependencies (like discord) from loading when importing
submodules such as bot.utils.database.
"""

# Export name for ease of discovery; consumers should import directly from
# bot.bot (e.g., `from bot.bot import CyberBot`).
__all__ = ['CyberBot']
