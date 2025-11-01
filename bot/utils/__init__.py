import os
import sys

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from bot.utils.database import db
from bot.utils.config import Config

__all__ = ['db', 'Config']
