import sys
import os

# Add project root to path so agents.py and app.py are importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
from mangum import Mangum

# Vercel Python runtime looks for 'handler' at the top level of this file
handler = Mangum(app, lifespan='off')

