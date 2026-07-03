import sys
import os

# Add project root to path so agents.py and app.py are importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import handler  # noqa: F401 - Vercel Python runtime looks for 'handler'

